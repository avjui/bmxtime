# setup.py
from distutils.core import setup
import py2exe
import os


setup(
        options = {'py2exe': {'bundle_files': 1, 'compressed': 1,}},
        zipfile = None,
        data_files=[('icons', ['icons\\bmx.png', 'icons\\exit.png', icons\\favicon.ico'])],
        name = 'BMXtime',
        version = 1.0.0 Beta,
        description = 'BMXtime is a small programm for time measure',
        windows=
          [
            {
                'script':'bmxtime.py',
                'name' : 'BMXtime',              
                'icon_resources': [(0, 'icons\\favicon.ico')],
            }   
          ]
     )
