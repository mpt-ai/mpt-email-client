import os
import re
from setuptools import find_packages, setup

package="mptemail"

def get_version():
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)
    
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mptemail',
    version=get_version(),
    url='https://github.com/mpt-ai/mpt-email-client',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A simple way to send email. for MPT',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Magnecomp PCL',
    author_email='contact@magnecomp.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

    ],
    install_requires=[
        'requests'
    ]
)