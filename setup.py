# -*- coding: utf-8 -*-

from distutils.core import setup
import os


def read_file(fname):
    if os.path.isfile("README.md"):
        file_path = os.path.join(os.path.dirname(__file__), fname)
        return open(file_path).read()
    else:
        return "A django Middleware that will help to set cache-control header on the views."

setup(
    name="django-smartcc",
    version="0.1.2",
    description="",
    author='Lorenzo Setale ( http://who.is.lorenzo.setale.me/? )',
    author_email="koalalorenzo@gmail.com",
    url="https://github.com/koalalorenzo/django-smartcc",

    license="GPL v2",
    packages=["smart_cache_control"],
    long_description=read_file("README.md"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)
