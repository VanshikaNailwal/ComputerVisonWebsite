# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all



# =============================
# DATA FILES
# =============================

datas = [

    # Backend source
    (
        'app',
        'app'
    ),


    # React build
    (
        'frontend_dist',
        'frontend_dist'
    ),


    # Alembic migrations
    (
        'migrations',
        'migrations'
    ),


    # setup_database.py
    (
        'scripts',
        'scripts'
    ),


    # Alembic config
    (
        'alembic.ini',
        '.'
    ),


    # Fixed production env
    (
        '.env',
        '.'
    )

]



binaries = []



# =============================
# HIDDEN IMPORTS
# =============================

hiddenimports = [

    'psycopg2',

    'cv2',

    'numpy',

    'torch',

    'torchvision',

    'ultralytics',

    'PIL',

    'yaml'

]




# =============================
# PACKAGE COLLECTOR
# =============================

def add_package(package):


    global datas

    global binaries

    global hiddenimports



    tmp_ret = collect_all(
        package
    )



    datas += tmp_ret[0]

    binaries += tmp_ret[1]

    hiddenimports += tmp_ret[2]






# =============================
# FASTAPI BACKEND
# =============================

add_package('fastapi')

add_package('starlette')

add_package('uvicorn')

add_package('httptools')

add_package('watchfiles')

add_package('websockets')



# =============================
# DATABASE
# =============================

add_package('sqlalchemy')

add_package('alembic')

add_package('psycopg2')



# =============================
# CONFIG
# =============================

add_package('pydantic')

add_package('pydantic_settings')

add_package('dotenv')



# =============================
# AUTH / SECURITY
# =============================

add_package('jose')

add_package('jwt')

add_package('passlib')

add_package('bcrypt')

add_package('cryptography')

add_package('rsa')

add_package('ecdsa')



# =============================
# EMAIL
# =============================

add_package('fastapi_mail')

add_package('aiosmtplib')

add_package('email_validator')

add_package('jinja2')



# =============================
# FORMS
# =============================

add_package('multipart')



# =============================
# COMPUTER VISION
# =============================

add_package('cv2')

add_package('numpy')

add_package('PIL')



# =============================
# YOLO
# =============================

add_package('torch')

add_package('torchvision')

add_package('ultralytics')

add_package('ultralytics_thop')



# =============================
# ML SUPPORT
# =============================

add_package('scipy')

add_package('matplotlib')

add_package('yaml')

add_package('requests')

add_package('psutil')

add_package('polars')

add_package('sympy')

add_package('networkx')






# =============================
# BUILD
# =============================

a = Analysis(

    [
        'run.py'
    ],


    pathex=[],


    binaries=binaries,


    datas=datas,


    hiddenimports=hiddenimports,


    hookspath=[],


    hooksconfig={},


    runtime_hooks=[],


    excludes=[],


    noarchive=False,


    optimize=0,

)




pyz = PYZ(
    a.pure
)




exe = EXE(

    pyz,

    a.scripts,

    [],

    exclude_binaries=True,

    name='HMELVision',

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    upx=True,

    console=True,

    disable_windowed_traceback=False,

    argv_emulation=False,

    target_arch=None,

    codesign_identity=None,

    entitlements_file=None,

)




coll = COLLECT(

    exe,

    a.binaries,

    a.datas,

    strip=False,

    upx=True,

    upx_exclude=[],

    name='VisionX',

)