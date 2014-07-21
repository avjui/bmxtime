# -*- coding: utf-8 -*-
"""manifest fixes NT-theming and including MSVC runtime issue"""

"""
# Recipe from
http://wiki.wxpython.org/Py2exe%20with%20Python2.6
"""

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="asInvoker"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.21022.8"
            processorArchitecture="x86"
            publicKeyToken="1fc8b3b9a1e18e3b">
      </assemblyIdentity>
    </dependentAssembly>
  </dependency>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
  </dependency>
</assembly>
"""

from distutils.core import setup
import py2exe
import os


dll_excludes = [
    'w9xpopen.exe',
    'MSVCP90.dll' # reason see link to wxPython-wiki above
]


setup(
        options = {'py2exe': {
                        #'bundle_files': 1,
                        'compressed': 1,
                        'dll_excludes' : dll_excludes,
                        #'packages':['connection', 'database', 'driverlist'],
                        }
                   },
        zipfile = None,
        data_files=[('icons', ['icons\\bmx.png', 'icons\\exit.png', 'icons\\favicon.ico'])],
        name = 'BMXtime',
        version = '1.0.0 Beta',
        description = 'BMXtime is a small programm for time measure',
        windows=
          [
            {
                'script':'bmxtime.py',
                'name' : 'BMXtime',              
                'icon_resources': [(0, 'icons\\favicon.ico')],
                'other_resources': [(24, 1, manifest)],
            }   
          ]
     )
