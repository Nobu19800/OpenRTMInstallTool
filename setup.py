# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
import sys
from setuptools import setup
\

NAME = 'InstallTool'
LICENSE = 'GPL'
AUTHOR = ''
AUTHOR_EMAIL = ''
DESCRIPTION = ''
URL = ''

if sys.platform == 'win32':
    # Windows
    import py2exe, innosetup
    
    PY2EXE_OPTIONS = {'compressed': 1,
                      'optimize': 2,
                      'bundle_files': 3,
                      'includes': ["sip"],}
    
    INNOSETUP_OPTIONS = {'inno_script': innosetup.DEFAULT_ISS,
                         'bundle_vcr': True,
                         'zip': False,
                         }
    setup(
        name = NAME,
        version = 0,
        license = LICENSE,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        description = DESCRIPTION,
        url = URL,
        scripts = ['InstallTool.py'],
        windows=[{"script": "InstallTool.py"}],
        options = {'py2exe': PY2EXE_OPTIONS,
                   'innosetup': INNOSETUP_OPTIONS},
        zipfile = 'InstallTool.lib',
    )

elif sys.platform == 'darwin':
    # Mac
    OPTIONS = {
               "argv_emulation": False,
               "includes": ["sip", "BeautifulSoup", "html5lib", "jsm"],
               'iconfile': 'jsm.icns',
               }
    setup(
        name = NAME,
        version = VERSION,
        license = LICENSE,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        description = DESCRIPTION,
        url = URL,
        app = ['InstallTool.py'],
        options = {'py2app': OPTIONS},
        setup_requires=["py2app"],
    )