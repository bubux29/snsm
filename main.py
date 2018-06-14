#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__version__ = '1.0.0'

from log import *
from SnsmMain import SnsmMain
import formation_db

import locale
def getpreferredencoding(do_s = True):
    return 'utf-8'
locale.getpreferredencoding = getpreferredencoding

if __name__ == "__main__":
	info('DB', 'Connection a la database')
	formation_db.init_db()
	formation_db.connect_to_db()
	SnsmMain().run()
	info('DB', 'Deconnection de la database')
	formation_db.disconnect_db()
