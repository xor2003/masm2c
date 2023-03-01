# -*- coding: utf-8 -*-
from pkg_resources import DistributionNotFound, get_distribution

import masm2c
import masm2c.cpp
import masm2c.op
import masm2c.parser
import masm2c.proc
import masm2c.Token

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "0.9.8"
finally:
    del get_distribution, DistributionNotFound
