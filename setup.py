import os
from setuptools import setup

import mobiledetect

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pymobiledetect",
    version = mobiledetect.__version__,
    author = "Bas van Oostveen",
    author_email = "v.oostveen@gmail.com",
    description = "Detect mobile and tablet browsers",
    license = "AGPL",
    keywords = "mobile tabled detect browser",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['mobiledetect', 'mobiledetect.test'],
    test_suite='nose.collector',
    long_description=read('README'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Software Development :: Libraries",
    ],
)

