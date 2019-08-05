# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import hy, j2do
import os.path

a = Analysis(['src\\craft.py'],
             pathex=['src', 'X:\\Projects\\Craft'],
             binaries=[],
             datas=[
				 ('stdlib', 'stdlib'),
				 ('LICENSE.txt', '.'),
				 ('README.md', '.'),
				 (os.path.dirname(hy.__file__), 'hy'),
				 (os.path.dirname(j2do.__file__), 'j2do'),
				 ('src', '.'),  # https://stackoverflow.com/questions/40646744/inspect-module-issues-in-pyinstaller-frozen-app
			 ],
             hiddenimports=['pathlib', 'yaml', 'jinja2', 'docopt', 'colorama'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='craft',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='craft')
