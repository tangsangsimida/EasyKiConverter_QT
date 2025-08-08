import argparse
import logging
import os
import re
import sys
from textwrap import dedent
from typing import List

from easyeda.easyeda_api import EasyedaApi
from easyeda.easyeda_importer import (
    Easyeda3dModelImporter,
    EasyedaFootprintImporter,
    EasyedaSymbolImporter,
)
from easyeda.parameters_easyeda import EeSymbol
from helpers import (
    add_component_in_symbol_lib_file,
    get_local_config,
    id_already_in_symbol_lib,
    set_logger,
    update_component_in_symbol_lib_file,
)
from kicad.export_kicad_3d_model import Exporter3dModelKicad
from kicad.export_kicad_footprint import ExporterFootprintKicad
from kicad.export_kicad_symbol import ExporterSymbolKicad
from kicad.parameters_kicad_symbol import KicadVersion


def get_parser() -> argparse.ArgumentParser:
    """
    创建并配置命令行参数解析器
    Create and configure command line argument parser
    
    返回:
    Returns:
        argparse.ArgumentParser: 配置好的参数解析器 / Configured argument parser
    """

    parser = argparse.ArgumentParser(
        description=(
            "A Python script that convert any electronic components from LCSC or"
            " EasyEDA to a Kicad library"
        )
    )

    parser.add_argument("--lcsc_id", help="LCSC id", required=True, type=str)

    parser.add_argument(
        "--symbol", help="Get symbol of this id", required=False, action="store_true"
    )

    parser.add_argument(
        "--footprint",
        help="Get footprint of this id",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "--3d",
        help="Get the 3d model of this id",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "--full",
        help="Get the symbol, footprint and 3d model of this id",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "--output",
        required=False,
        metavar="file.kicad_sym",
        help="Output file",
        type=str,
    )

    parser.add_argument(
        "--overwrite",
        required=False,
        help=(
            "overwrite symbol and footprint lib if there is already a component with"
            " this lcsc_id"
        ),
        action="store_true",
    )

    parser.add_argument(
        "--v5",
        required=False,
        help="Convert library in legacy format for KiCad 5.x",
        action="store_true",
    )

    parser.add_argument(
        "--project-relative",
        required=False,
        help="Sets the 3D file path stored relative to the project",
        action="store_true",
    )

    parser.add_argument(
        "--debug",
        help="set the logging level to debug",
        required=False,
        default=False,
        action="store_true",
    )

    return parser


def valid_arguments(arguments: dict) -> bool:
    """
    验证和处理命令行参数，确保参数有效性并创建必要的输出目录
    Validate and process command line arguments, ensure parameter validity and create necessary output directories
    
    参数:
    Args:
        arguments (dict): 命令行参数字典 / Command line arguments dictionary
        
    返回:
    Returns:
        bool: 参数有效返回True，无效返回False / True if parameters are valid, False otherwise
    """

    if not arguments["lcsc_id"].startswith("C"):
        logging.error("lcsc_id should start by C....")
        return False

    if arguments["full"]:
        arguments["symbol"], arguments["footprint"], arguments["3d"] = True, True, True

    if not any([arguments["symbol"], arguments["footprint"], arguments["3d"]]):
        logging.error(
            "Missing action arguments\n"
            "  easyeda2kicad --lcsc_id=C2040 --footprint\n"
            "  easyeda2kicad --lcsc_id=C2040 --symbol"
        )
        return False

    kicad_version = KicadVersion.v5 if arguments.get("v5") else KicadVersion.v6
    arguments["kicad_version"] = kicad_version

    if arguments["project_relative"] and not arguments["output"]:
        logging.error(
            "A project specific library path should be given with --output option when"
            " using --project-relative option\nFor example: easyeda2kicad"
            " --lcsc_id=C2040 --full"
            " --output=C:/Users/your_username/Documents/Kicad/6.0/projects/my_project"
            " --project-relative"
        )
        return False

    if arguments["output"]:
        output_path = arguments["output"]
        if not os.path.isabs(output_path):
            output_path = os.path.join(os.getcwd(), output_path)

        base_folder = os.path.dirname(output_path)
        lib_name = os.path.splitext(os.path.basename(output_path))[0]

        if not os.path.isdir(base_folder):
            os.makedirs(base_folder, exist_ok=True)
    else:
        default_folder = os.path.join(
            os.path.expanduser("~"),
            "Documents",
            "Kicad",
            "easyeda2kicad",
        )
        if not os.path.isdir(default_folder):
            os.makedirs(default_folder, exist_ok=True)

        base_folder = default_folder
        lib_name = "easyeda2kicad"
        arguments["use_default_folder"] = True

    arguments["output"] = f"{base_folder}/{lib_name}"

    # Create new footprint folder if it does not exist
    if not os.path.isdir(f"{arguments['output']}.pretty"):
        os.mkdir(f"{arguments['output']}.pretty")
        logging.info(f"Create {lib_name}.pretty footprint folder in {base_folder}")

    # Create new 3d model folder if don't exist
    if not os.path.isdir(f"{arguments['output']}.3dshapes"):
        os.mkdir(f"{arguments['output']}.3dshapes")
        logging.info(f"Create {lib_name}.3dshapes 3D model folder in {base_folder}")

    lib_extension = "kicad_sym" if kicad_version == KicadVersion.v6 else "lib"
    if not os.path.isfile(f"{arguments['output']}.{lib_extension}"):
        with open(
            file=f"{arguments['output']}.{lib_extension}", mode="w+", encoding="utf-8"
        ) as my_lib:
            my_lib.write(
                dedent(
                    '''\
                (kicad_symbol_lib
                  (version 20211014)
                  (generator https://github.com/uPesy/easyeda2kicad.py)
                )'''
                )
                if kicad_version == KicadVersion.v6
                else "EESchema-LIBRARY Version 2.4\n#encoding utf-8\n"
            )
        logging.info(f"Create {lib_name}.{lib_extension} symbol lib in {base_folder}")

    return True


def main() -> None:
    """
    主函数 - 执行EasyEDA到KiCad的完整转换流程
    Main function - Execute complete EasyEDA to KiCad conversion workflow
    
    工作流程:
    Workflow:
        1. 解析命令行参数 / Parse command line arguments
        2. 设置日志系统 / Setup logging system
        3. 验证参数有效性 / Validate parameter validity
        4. 从EasyEDA API获取组件数据 / Fetch component data from EasyEDA API
        5. 根据用户选择转换符号、封装和3D模型 / Convert symbol, footprint and 3D model based on user selection
        6. 保存到KiCad库文件 / Save to KiCad library files
    """

    args = get_parser().parse_args()
    arguments = vars(args)

    set_logger(log_file="", log_level=logging.DEBUG if arguments["debug"] else logging.INFO)

    if not valid_arguments(arguments):
        sys.exit(1)

    logging.info(f"LCSC Part number: {arguments['lcsc_id']}")

    easyeda_api = EasyedaApi()

    component_data = easyeda_api.get_cad_data_of_component(lcsc_id=arguments["lcsc_id"])
    if not component_data:
        logging.error(f"Failed to retrieve component data for LCSC ID: {arguments['lcsc_id']}")
        sys.exit(1)

    if arguments["symbol"]:
        logging.info("Symbol conversion ...")
        symbol_importer = EasyedaSymbolImporter(easyeda_cp_cad_data=component_data)
        symbol_data = symbol_importer.get_symbol()
        if not symbol_data:
            logging.error("No symbol found for this component")
        else:
            symbol_exporter = ExporterSymbolKicad(
                symbol=symbol_data, kicad_version=arguments["kicad_version"]
            )
            kicad_symbol_str = symbol_exporter.export(footprint_lib_name=os.path.basename(arguments["output"]))
            
            lib_extension = "kicad_sym" if arguments["kicad_version"] == KicadVersion.v6 else "lib"
            symbol_lib_path = f"{arguments['output']}.{lib_extension}"
            
            logging.info(f"Symbol saved to {symbol_lib_path}")
            if not id_already_in_symbol_lib(
                lib_path=symbol_lib_path,
                component_name=symbol_data.info.name,
                kicad_version=arguments["kicad_version"],
            ):
                add_component_in_symbol_lib_file(
                    lib_path=symbol_lib_path,
                    component_content=kicad_symbol_str,
                    kicad_version=arguments["kicad_version"],
                )
            elif arguments["overwrite"]:
                update_component_in_symbol_lib_file(
                    lib_path=symbol_lib_path,
                    component_name=symbol_data.info.name,
                    component_content=kicad_symbol_str,
                    kicad_version=arguments["kicad_version"],
                )

    if arguments["footprint"]:
        logging.info("Footprint conversion ...")
        footprint_importer = EasyedaFootprintImporter(easyeda_cp_cad_data=component_data)
        footprint_data = footprint_importer.get_footprint()
        if not footprint_data:
            logging.error("No footprint found for this component")
        else:
            footprint_exporter = ExporterFootprintKicad(footprint=footprint_data)
            footprint_dir = arguments["output"] + ".pretty"
            os.makedirs(footprint_dir, exist_ok=True)
            footprint_filename = os.path.join(
                footprint_dir, f"{footprint_data.info.name}.kicad_mod"
            )
            model_3d_path = "easyeda2kicad"
            footprint_exporter.export(
                footprint_full_path=footprint_filename, 
                model_3d_path=model_3d_path
            )
            logging.info(f"Footprint saved to {footprint_filename}")

    if arguments["3d"]:
        logging.info("3D model conversion ...")
        model_3d_importer = Easyeda3dModelImporter(
            easyeda_cp_cad_data=component_data, 
            download_raw_3d_model=True
        )
        model_3d = model_3d_importer.create_3d_model()
        if not model_3d:
            logging.error("No 3D model found for this component")
        else:
            model_3d_exporter = Exporter3dModelKicad(model_3d=model_3d)
            model_3d_exporter.export(lib_path=arguments["output"])


if __name__ == "__main__":
    main()