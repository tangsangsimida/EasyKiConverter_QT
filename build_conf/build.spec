# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
import sys

# 动态确定资源路径
# 在PyInstaller环境中使用不同的方法获取当前目录
if getattr(sys, 'frozen', False):
    # 如果是PyInstaller打包的环境
    current_dir = os.path.dirname(sys.executable)
else:
    # 如果是正常Python环境
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

resources_dir = os.path.join(current_dir, '..', 'src', 'ui', 'pyqt6', 'resources')

# 构建资源文件列表
icon_files = []
icon_extensions = ['.ico', '.icns', '.png', '.svg']
for ext in icon_extensions:
    icon_path = os.path.join(resources_dir, f'app_icon{ext}')
    if os.path.exists(icon_path):
        # 确保在Windows上使用正确的路径分隔符
        icon_files.append((icon_path, 'resources/'))

# 确定图标文件路径用于EXE构建
icon_path = None
if sys.platform.startswith('win'):
    icon_path = os.path.join(resources_dir, 'app_icon.ico')
elif sys.platform.startswith('darwin'):
    icon_path = os.path.join(resources_dir, 'app_icon.icns')
else:
    # Linux平台通常不使用图标文件，或者使用PNG格式
    icon_path = os.path.join(resources_dir, 'app_icon.png')
    # 如果PNG文件不存在，则不使用图标
    if not os.path.exists(icon_path):
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
    # Windows x86架构需要指定target_arch
    target_arch='x86' if sys.platform.startswith('win') and 'x86' in sys.argv else None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path
)