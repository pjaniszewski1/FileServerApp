from os.path import join, dirname

from setuptools import setup, find_packages

import server

setup(
    name='FileServer',
    version=server.__version__,
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.6.0',
        'cchardet==2.4.1',
        'aiodns==2.0.0',
        'pycryptodome==3.9.4',
        'pytest==5.3.1',
        'pytest-aiohttp==0.3.0',
        'psycopg2==2.8.4',
        'SQLAlchemy==1.3.11',
        'uuid==1.30',
    ],
    entry_points={
        'console_scripts': ['fileserver = main:main']
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
