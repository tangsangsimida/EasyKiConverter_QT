# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE

import os
import sys

# 从环境变量获取构建架构
BUILD_ARCH = os.environ.get('BUILD_ARCH', 'x64')

# 动态确定资源路径
# 在PyInstaller环境中使用不同的方法获取当前目录
if getattr(sys, 'frozen', False):
    # 如果是PyInstaller打包的环境
    current_dir = os.path.dirname(sys.executable)
else:
    # 如果是正常Python环境
    # 获取当前工作目录作为基准
    current_dir = os.getcwd()

resources_dir = os.path.join(current_dir, 'src', 'ui', 'pyqt6', 'resources')

# 构建资源文件列表
icon_files = []
icon_extensions = ['.ico', '.icns', '.png', '.svg']
for ext in icon_extensions:
    icon_path = os.path.join(resources_dir, f'app_icon{ext}')
    if os.path.exists(icon_path):
        # 确保在Windows上使用正确的路径分隔符
        icon_files.append((icon_path, 'resources/'))

import os

# 确定图标文件路径用于EXE构建
# 使用绝对路径确保PyInstaller能找到图标文件
current_dir = os.getcwd()
icon_path = os.path.join(current_dir, 'src', 'ui', 'pyqt6', 'resources', 'app_icon.ico')

# 检查图标文件是否存在
if os.path.exists(icon_path):
    print(f"使用图标文件: {icon_path}")
else:
    print(f"警告: 图标文件不存在 {icon_path}")
    icon_path = None

a = Analysis(
    ['../src/ui/pyqt6/main.py'],
    pathex=['.', '../src'],
    binaries=[],
    datas=icon_files,
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtNetwork',
        'PyQt6.QtOpenGL',
        'PyQt6.QtOpenGLWidgets',
        'pandas',
        'pandas._libs',
        'pandas._libs.tslibs',
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.nattype',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.skiplist',
        'pandas.io',
        'pandas.io.common',
        'pandas.io.parsers',
        'pandas.io.parsers.readers',
        'pandas._config.config',
        'openpyxl',
        'openpyxl.workbook',
        'openpyxl.workbook.workbook',
        'openpyxl.worksheet',
        'openpyxl.worksheet.worksheet',
        'requests',
        'requests.adapters',
        'requests.auth',
        'requests.cookies',
        'requests.exceptions',
        'requests.hooks',
        'requests.models',
        'requests.sessions',
        'requests.status_codes',
        'requests.structures',
        'requests.utils',
        'pydantic',
        'pydantic_core',
        'pydantic.main',
        'pydantic.types',
        'pydantic.fields',
        'numpy',
        'numpy._core',
        'numpy._core._multiarray_umath',
        'numpy._core.multiarray',
        'numpy._core.umath',
        'numpy._core.numeric',
        'numpy.linalg',
        'numpy.linalg._umath_linalg',
        'numpy.linalg.lapack_lite',
        'numpy.random',
        'numpy.random._pickle',
        'numpy.random.common',
        'numpy.random.bounded_integers',
        'numpy.random.entropy',
        'numpy.random.bit_generator',
        'certifi',
        'urllib3',
        'urllib3.connection',
        'urllib3.connectionpool',
        'urllib3.contrib',
        'urllib3.contrib.pyopenssl',
        'urllib3.exceptions',
        'urllib3.fields',
        'urllib3.filepost',
        'urllib3.packages',
        'urllib3.packages.ssl_match_hostname',
        'urllib3.poolmanager',
        'urllib3.request',
        'urllib3.response',
        'urllib3.util',
        'urllib3.util.connection',
        'urllib3.util.request',
        'urllib3.util.response',
        'urllib3.util.retry',
        'urllib3.util.ssl_',
        'urllib3.util.timeout',
        'urllib3.util.url',
        'charset_normalizer',
        'idna',
        'python_dateutil',
        'python_dateutil.parser',
        'pytz',
        'tzdata',
        'et_xmlfile',
        'six',
        'annotated_types',
        'typing_extensions',
        'typing_inspection'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'jinja2',
        'werkzeug',
        'blinker',
        'click',
        'markupsafe'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EasyKiConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    # 使用环境变量设置target_arch
    target_arch='x86' if BUILD_ARCH == 'x86' else None,
    # macOS通用二进制支持
    universal2=True if sys.platform.startswith('darwin') else False,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path
)