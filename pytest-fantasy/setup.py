# read the contents of your README file
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


version = "0.2.15"

requirements_list = [
    'fudge',
    'codecov',
    'flake8',
    'pytest',
    'pytest-pep8',
    'pytest-cov',
    'pytest-instafail',
    'pytest-mock',
    'pytest-logging',
    'pytest-mock',
    'pytest-watch',
    'pytest-xdist',
    'pytest-flask',
    'pytest-fantasy'
]

setup(
    name='pytest-fantasy',
    version=version,
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements_list,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wangwenpei/pytest-fantasy',
    download_url='https://github.com/wangwenpei/pytest-fantasy/tarball/master',
    license='MIT',
    author='WANG WENPEI',
    zip_safe=False,
    test_suite="tests",
    author_email='stormxx@1024.engineer',
    description='Pytest plugin for Flask Fantasy Framework',
    keywords='fantasy,flask',
)
