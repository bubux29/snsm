#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__version__ = '1.0.0'

from log import *
from SnsmMain import SnsmMain
import formation_db

if __name__ == "__main__":
	info('DB', 'Connection à la database')
	formation_db.init_db()
	formation_db.connect_to_db()
	SnsmMain().run()
	info('DB', 'Déconnection de la database')
	formation_db.disconnect_db()
