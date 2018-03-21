import os

from setuptools import find_packages, setup


def get_version(version_tuple):
    """Return the version tuple as a string, e.g. for (0, 10, 7),
    return '0.10.7'.
    """
    return '.'.join(map(str, version_tuple))


# Dirty hack to get version number from fantasy/__init__.py - we
# can't import it as it depends on Flask and Flask isn't installed until
# user explicit install it. this idea is inspiring from flask-mongoengine
init = os.path.join(os.path.dirname(__file__), 'fantasy', '__init__.py')
version_line = list(filter(lambda l: l.startswith('version_info ='),
                           open(init)))[0]
version = get_version(eval(version_line.split('=')[-1]))

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
