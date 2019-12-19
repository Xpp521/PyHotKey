from os.path import join, dirname
from setuptools import setup, find_packages

# The name of the package on PyPi
PYPI_PACKAGE_NAME = 'PyHotKey'

# The name of the main Python package
MAIN_PACKAGE_NAME = 'PyHotKey'

# The package URL
PACKAGE_URL = 'https://github.com/Xpp521/PyHotKey'

# The runtime requirements
RUNTIME_PACKAGES = ['pynput>=1.4.5']

# Additional requirements used during setup
SETUP_PACKAGES = []

# Packages requires for different environments
EXTRA_PACKAGES = {}

ROOT = dirname(__file__)

# Load author and version message
INFO = {}
with open(join(ROOT, MAIN_PACKAGE_NAME, '_info.py')) as f:
    for line in f:
        data = line.rstrip().replace(' ', '').replace("'", '').split('=')
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
    name=PYPI_PACKAGE_NAME,
    version=INFO.get('VERSION'),
    description='A cross-platform hot key module.',
    long_description=README + CHANGES,
    long_description_content_type='text/markdown',
    author=INFO.get('AUTHOR'),
    author_email=INFO.get('AUTHOR_EMAIL'),
    url=PACKAGE_URL,
    project_urls={'Documentation': 'https://github.com/Xpp521/PyHotKey/wiki',
                  'Source': 'https://github.com/Xpp521/PyHotKey',
                  'Tracker': 'https://github.com/Xpp521/PyHotKey/issues'},
    license='LGPLv3',
    keywords=['hotkey', 'hot', 'key'],
    packages=find_packages(),
    # package_dir={'': join(ROOT, MAIN_PACKAGE_NAME)},
    install_requires=RUNTIME_PACKAGES,
    setup_requires=SETUP_PACKAGES,
    extras_require=EXTRA_PACKAGES,
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
