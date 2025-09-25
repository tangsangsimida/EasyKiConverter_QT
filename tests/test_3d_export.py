#!/usr/bin/env python3
# 测试3D模型导出流程

import sys
sys.path.insert(0, '/home/dennis/Desktop/workspace/github_projects/EasyKiConverter/src')

from core.easyeda.parameters_easyeda import Ee3dModel, Ee3dModelBase
from core.kicad.export_kicad_3d_model import Exporter3dModelKicad

# 创建一个测试3D模型
test_model = Ee3dModel(
    name="TEST_MODEL",
    uuid="test-uuid-12345",
    translation=Ee3dModelBase(x=0, y=0, z=0),
    rotation=Ee3dModelBase(x=0, y=0, z=0),
    raw_obj="""# Simple test OBJ
mtllib test.mtl
usemtl test_material
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 1.0 1.0 0.0
v 0.0 1.0 0.0
f 1 2 3 4
""",
    step=b"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION((''), '2;1');
FILE_NAME('test.step', '2023-01-01T00:00:00', (''), (''), '', '', '');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
ENDSEC;
END-ISO-10303-21;
"""
)

print("=== 测试3D模型导出 ===")
print(f"模型名称: {test_model.name}")
print(f"UUID: {test_model.uuid}")
print(f"有OBJ数据: {'是' if test_model.raw_obj else '否'}")
print(f"有STEP数据: {'是' if test_model.step else '否'}")

# 创建导出器
exporter = Exporter3dModelKicad(model_3d=test_model)

print(f"\n导出器输出: {exporter.output}")
print(f"导出器STEP输出: {'有' if exporter.output_step else '无'}")

# 测试导出
test_lib_path = "/tmp/test_lib"
import os
print(f"\n导出到: {test_lib_path}")

try:
    exporter.export(lib_path=test_lib_path)
    print("✅ 导出成功")
    
    # 检查生成的文件
    shapes_dir = f"{test_lib_path}.3dshapes"
    print(f"3D shapes目录: {shapes_dir}")
    
    if os.path.exists(shapes_dir):
        files = os.listdir(shapes_dir)
        print(f"生成的文件: {files}")
        for file in files:
            file_path = os.path.join(shapes_dir, file)
            size = os.path.getsize(file_path)
            print(f"  {file}: {size} bytes")
    else:
        print("❌ 3D shapes目录不存在")
        
except Exception as e:
    print(f"❌ 导出失败: {e}")
    import traceback
    traceback.print_exc()

# 检查目录是否存在
print(f"\n目录检查:")
print(f"测试目录存在: {'是' if os.path.exists('/tmp') else '否'}")
print(f"工作目录: {os.getcwd()}")