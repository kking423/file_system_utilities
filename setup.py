import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


with open('./requirements.txt', 'r', encoding='utf-8') as fin:
    requires_list = [line.strip() for line in fin if line and line.strip()]


def read_version():
    filename = os.path.join(os.path.dirname(__file__), 'file_system_utilities', '__init__.py')
    with open(filename, mode="r", encoding='utf-8') as fin2:
        for line in fin2:
            if line and line.strip() and line.startswith('__version__'):
                return line.split('=')[1].strip().strip("'").strip('"')

    return "0.0.0.0"


setup(
    name="file_system_utilities",
    version=read_version(),
    url="https://github.com/kking423/file_system_utilities",
    license='MIT',

    author="Kyle King",
    author_email="kking423@gmail.com",

    description="A utility to help perform a recursive file search "
                "and return a dictionary with extended metadata",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",

    packages=find_packages(exclude=('tests', 'examples', 'readme_resources', 'build', 'dist',)),

    install_requires=requires_list,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
)
