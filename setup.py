"""
    adbts
    ~~~~~

    Android Debug Bridge (ADB) Transports

    :copyright: (c) 2017 Andrew Hawker.
    :license: Apache 2.0, see LICENSE for more details.
"""
import ast
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version_regex = re.compile(r'__version__\s+=\s+(.*)')


def get_version():
    with open('adbts/__init__.py', 'r') as f:
        return str(ast.literal_eval(version_regex.search(f.read()).group(1)))


setup(
    name='adbts',
    version=get_version(),
    author='Andrew Hawker',
    author_email='andrew.r.hawker@gmail.com',
    url='https://github.com/adbpy/transports',
    license='Apache 2.0',
    description='Android Debug Bridge (ADB) Transports',
    long_description=__doc__,
    packages=['adbts'],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    )
)
