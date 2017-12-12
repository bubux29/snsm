import models.dbDefs
# Aujourd'hui on fait du peewee
DB='peewee'

if DB=='peewee':
    from models.peeweehelper import _peewee_handled_types, _peewee_types_dict
    handled_db_types=_peewee_handled_types
    handled_db_dict=_peewee_types_dict

def whatType(classe):
    return [c for c, v in handled_db_dict.items() if v == classe][0]

def isType(ty):
    return handled_db_types.count(ty)
