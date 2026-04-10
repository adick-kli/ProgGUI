# -*- coding: utf-8 -*-
# src/app/pages/__init__.py
"""Pages Package."""

from .page_home import PageHome
from .page_settings import PageSettings
from .page_devices import PageDevices
from .page_jtag import PageJTAG
from .page_bootloader import PageBootloader

__all__ = ['PageHome', 'PageSettings', 'PageDevices', 'PageJTAG', 'PageBootloader']