# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['uma.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('gui', 'gui'),
        ('database', 'database'),
        ('core', 'core'),
        ('assets', 'assets'),
        ('setup', 'setup'),
        ('metadata.py', '.'),
    ],
    hiddenimports=[
        'webbrowser', 'json', 'sqlite3', 'configparser',
        'tkinter', 'tkinter.ttk', 'tkinter.messagebox',
        'matplotlib', 'matplotlib.backends.backend_tkagg',
        'numpy', 'PIL',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='uma-tt-db',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)