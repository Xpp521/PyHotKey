from os.path import join, dirname
from setuptools import setup, find_packages

# Main package name
PACKAGE_NAME = 'PyHotKey'

# The package URL
PACKAGE_URL = 'https://github.com/Xpp521/PyHotKey'

# The runtime requirements
INSTALL_REQUIRES = ['pynput==1.7.7']

# Additional requirements used during setup
SETUP_REQUIRES = []

# Packages requires for different environments
EXTRAS_REQUIRES = {}

# Root directory
ROOT = dirname(__file__)

# Load module info
INFO = {}
with open(join(ROOT, PACKAGE_NAME, '_info.py')) as f:
    for line in f:
        if line.startswith('#'):
            continue
        data = line.strip().replace(' ', '').replace("'", '').split('=')
        if 2 == len(data):
            INFO[data[0]] = data[1]

# Load README.md
try:
    with open(join(ROOT, 'README.md')) as f:
        README = f.read()
except IOError:
    README = ''

# Load CHANGES.md
try:
    with open(join(ROOT, 'CHANGES.md')) as f:
        CHANGES = f.read()
except IOError:
    CHANGES = ''

setup(
    name=INFO.get('NAME'),
    version=INFO.get('VERSION'),
    description='A cross-platform keyboard module.',
    long_description=README + CHANGES,
    long_description_content_type='text/markdown',
    author=INFO.get('AUTHOR'),
    author_email=INFO.get('AUTHOR_EMAIL'),
    url=PACKAGE_URL,
    project_urls={
        'Documentation': 'https://github.com/Xpp521/PyHotKey',
        'Source': 'https://github.com/Xpp521/PyHotKey',
        'Tracker': 'https://github.com/Xpp521/PyHotKey/issues'
    },
    license='LGPLv3',
    keywords=['hotkey', 'keyboard', 'hot+key'],
    packages=find_packages(),
    # package_dir={'': join(ROOT, MAIN_PACKAGE_NAME)},
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows NT/2000',
        'Operating System :: POSIX',
        'License :: OSI Approved :: GNU Lesser General Public License v3 '
        '(LGPLv3)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring'
    ])
