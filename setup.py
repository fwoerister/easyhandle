from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='easyhandle',
    version='0.0.5',
    description='A lightweight python package for accessing handle services',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Florian Woerister',
    author_email='florian.woerister@tuwien.ac.at',

    classifiers=[
        'Development Status :: 4 - Beta',

        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        'Programming Language :: Python :: 3',
    ],

    url='https://github.com/fwoerister/easyhandle',
    packages=['easyhandle'],
    keywords='''handle.net client python''',
    license='AGPLv3+'
)
