#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from os.path import basename

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cwd_name = basename(os.getcwd())
os.sys.path.insert(1, parent_dir)
mod = __import__(cwd_name)
sys.modules[cwd_name] = mod
__package__ = cwd_name

from .authorization.sign_in import SignInHandler
from .authorization.sign_up import SignUpHandler
from .booking.doctorlist import DocterListHandler
from .booking.clinic_update_admin import Clinic_updater
from .booking.slotlist  import SlotListHandler
#from .tourist.tourqr_pass import PassQRHandler

# from change_password import ChangePasswordHandler

from .lib.lib import *
