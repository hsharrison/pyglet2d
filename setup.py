# -*- encoding: utf8 -*-
import glob
import io
import re
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()

# Read version.
namespace = {}
exec(read('src/pyglet2d.py').splitlines()[0], namespace)

setup(
    name="pyglet2d",
    version=namespace['__version__'],
    license="BSD",

    description="2D shape primitives for pyglet.",
    long_description="%s\n%s" % (read("README.rst"), re.sub(":obj:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst"))),

    author="Henry S. Harrison",
    author_email="henry.schafer.harrison@gmail.com",
    url="https://github.com/hsharrison/pyglet2d",

    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,

    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
    ],
    keywords=[
        # eg: "keyword1", "keyword2", "keyword3",
    ],

    install_requires=[
        'numpy',
        'Polygon3',
        #'pyglet',  Must be commented out for CI to work, until pyglet 1.2 is released.
    ],
    extras_require={
        # eg: 'rst': ["docutils>=0.11"],
    },

)
