#!/usr/bin/env python

import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'src'))
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

execfile(join(dirname(__file__), 'src', 'JiaseLibrary', 'version.py'))

DESCRIPTION = 'JiaseLibrary is a interface testing library for Jiase system'


setup(name         = 'robotframework-jiaselibrary',
      version      = VERSION,
      description  = 'Interface testing library for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Yang kangning, Yin jia',
      author_email = '<yangkangning@nongfadai.com>',
      url          = 'https://github.com/robotframework/Selenium2Library',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation',
      platforms    = 'any',
      classifiers  = [
                        "Development Status :: 5 - Production/Stable",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python",
                        "Topic :: Software Development :: Testing"
                     ],
      py_modules=['ez_setup'],
      package_dir  = {'' : 'src'},
      packages     = ['JiaseLibrary','JiaseLibrary.keywords','JiaseLibrary.utils'],
      package_data ={'JiaseLibrary':['config/*.cfg']},
      include_package_data = True,
      )
