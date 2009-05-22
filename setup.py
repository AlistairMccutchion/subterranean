from distutils.core import setup, Extension
try:
    import py2exe
except:
    pass

import sys
import glob
import os
import shutil
import pygame


data = [
    '*.txt',
    'data/*',
    ]
    
for d in glob.glob('data/*'):
    if '_wav' not in d:
        data.append('%s/*'%d)
        
print data

src = [
    '*.py',
    '*.c',
    '*.h',
    '*.i',
    ]

#extra_files = [ (glob.glob(os.path.join('win_includes','*.dll'))),
#                                 (glob.glob(os.path.join('win_includes','*.pyc')))   
#    ]

# List of all modules to automatically exclude from distribution  build# This gets rid of extra modules that aren't necessary for proper functioning of app# You should only put things in this list if you know exactly what you DON'T need
# This has the benefit of drastically reducing the size of your dist
 
MODULE_EXCLUDES =[
'email',
'AppKit',
'Foundation',
'bdb',
'difflib',
'tcl',
'Tkinter',
'Tkconstants',
'curses',
'distutils',
'setuptools',
'urllib',
'urllib2',
'urlparse',
'BaseHTTPServer',
'_LWPCookieJar',
'_MozillaCookieJar',
'ftplib',
'gopherlib',
'_ssl',
'htmllib',
'httplib',
'mimetools',
'mimetypes',
'rfc822',
'tty',
'webbrowser',
'socket',
'hashlib',
'base64',
'compiler',
'pydoc']

includes =[
'pygame',
#'pygame.mixer.sound'
]

cmd = sys.argv[1]

if cmd in ('sdist'):
    f = open("MANIFEST.in","w")
    for l in data: f.write("include "+l+"\n")
    for l in src: f.write("include "+l+"\n")
    f.close()


if cmd in ('sdist','build'):
    setup(
        name='Subterranean',
        version='0.1',
        description='Project Subterranean',
        url='http://github.com/kallepersson/subterranean/tree/master',
        
        )

if cmd in ('py2exe',):
    setup(
        options={'py2exe':{
            'dist_dir':'dist',
            'dll_excludes':['_dotblas.pyd','_numpy.pyd'],
            'optimize': 2,
            'compressed': 1,
# bundle_files throws a .dll error. Would otherwise reduce clutter
# and lower filesize.
            'bundle_files': 2,
            'ignores': ['tcl','AppKit','Numeric','Foundation'],
            'excludes': MODULE_EXCLUDES,
            'includes': includes,
            }},
        windows=[{
            'script':'main.py',
            #'icon_resources':[(1,'icon.ico')],
            }],
        zipfile = None,
        #data_files = extra_files
        )

if cmd in ('build',):
    for fname in glob.glob("build/lib*/*.so"):
        shutil.copy(fname,os.path.basename(fname))

    for fname in glob.glob("build/lib*/*.pyd"):
        shutil.copy(fname,os.path.basename(fname))

if cmd in ('py2exe',):
    for gname in data:
        for fname in glob.glob(gname):
            dname = os.path.join('dist',os.path.dirname(fname))
            try:
                os.mkdir(dname)
            except:
                'mkdir failed: '+dname
            if not os.path.isdir(fname):
                shutil.copy(fname,dname)