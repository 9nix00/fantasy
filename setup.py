from os import path

from setuptools import find_packages, setup

version = "0.4.2"

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

with open(path.join(this_directory, 'requirements.txt')) as f:
    requirements_list = f.readlines()

setup(
    name='flask-fantasy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements_list,
    version=version,
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/9nix00/fantasy',
    download_url='https://github.com/9nix00/fantasy/archive/v0.4.2.tar.gz',
    license='MIT',
    author='WANG WENPEI',
    entry_points={"pytest11": ["pytest_fantasy = fantasy_pytest.fixtures"]},
    zip_safe=False,
    test_suite="tests",
    author_email='stormxx@1024.engineer',
    description='A lazy web-framework based on Flask',
    keywords='fantasy,flask',
    classifiers=["Framework :: Pytest"],
)
