import os
from setuptools import setup

import mobiledetect

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Hack to prevent stupid TypeError: 'NoneType' object is not callable error on
# exit of python setup.py test # in multiprocessing/util.py _exit_function when
# running python setup.py test (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass

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

