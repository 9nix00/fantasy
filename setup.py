from setuptools import find_packages, setup

version = "0.2.13"

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

with open(path.join(this_directory, 'requirements.txt')) as f:
    requirements_list = [v.strip() for v in f.readlines() if
                         v.strip() and v.strip()[0] != '#']

setup(
    name='flask-fantasy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements_list,
    version=version,
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/wangwenpei/fantasy',
    download_url='https://github.com/wangwenpei/fantasy/tarball/master',
    license='MIT',
    author='WANG WENPEI',
    zip_safe=False,
    test_suite="tests",
    author_email='stormxx@1024.engineer',
    description='A bootstrap tool for Flask APP',
    keywords='fantasy,flask',
)
