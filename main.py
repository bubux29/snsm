#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__version__ = '1.0.0'

from log import *
from SnsmMain import SnsmMain
import formation_db
import time

from config import CONF
import traceback
import pops

if __name__ == "__main__":
    try:
        import os
        try:
            os.makedirs(CONF.exception_path)
        except:
            pass
        info('DB', 'Connexion à la database')
        formation_db.init_db()
        formation_db.connect_to_db()
        SnsmMain().run()
        info('DB', 'Déconnexion de la database')
        formation_db.disconnect_db()
    except Exception as e:
        timestr = time.strftime('%Y%m%d-%H%M%S')
        with open(CONF.exception_path + '/' + timestr + '.exc', 'w') as f:
            traceback.print_exc(file=f)
