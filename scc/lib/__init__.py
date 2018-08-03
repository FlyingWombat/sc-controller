#!/usr/bin/env python3

from __future__ import absolute_import
import sys

#This will import System python enum.py if PyVer > 3.0
#Otherwise will import Python 2 compatible enum.py,
#modified from https://github.com/certik/enum34

pyver = float('%s.%s' % sys.version_info[:2])

if pyver >= 3.0:
    from enum import Enum, IntEnum, unique
else:
    from .enum2 import Enum, IntEnum, unique

