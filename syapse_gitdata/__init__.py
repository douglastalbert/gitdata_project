# -*- coding: utf-8 -*-

"""Top-level package for syapse_gitdata."""

from pkg_resources import get_distribution, DistributionNotFound
from .syapse_gitdata import *


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = "0.1.0.dev0+missinggit"
