from setuptools import find_packages, setup

version = "0.2.6"

setup(
    name='flask-fantasy',
    version=version,
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/wangwenpei/fantasy',
    download_url='https://github.com/wangwenpei/fantasy/tarball/master',
    license='MIT',
    author='WANG WENPEI',
    zip_safe=False,
    test_suite="tests",
    author_email='wangwenpei@nextoa.com',
    description='A bootstrap tool for Flask APP',
    keywords='fantasy,flask',
)
