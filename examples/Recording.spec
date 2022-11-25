# -*- mode: python ; coding: utf-8 -*-
from os import getcwd
from os.path import join

# Root directory
ROOT = getcwd()

block_cipher = None

extra_files = [
    (join(ROOT, 'check.png'), '.',),
    (join(ROOT, 'down-arrow.png'), '.'),
    (join(ROOT, 'Recording.qss'), '.'),
]

a = Analysis(
    ['Recording.py'],
    pathex=[],
    binaries=[],
    datas=extra_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Recording',
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
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Recording',
)
