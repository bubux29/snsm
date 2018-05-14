import peewee
import playhouse
from models.dbDefs import FieldType

_peewee_handled_types=[
peewee.CharField,
peewee.ForeignKeyField,
playhouse.fields.ManyToManyField,
peewee.TextField,
peewee.DateTimeField,
peewee.BooleanField,
]

_peewee_types_dict=dict(
E_CharField=peewee.CharField,
E_LinkField=peewee.ForeignKeyField,
E_MultiLinkField=playhouse.fields.ManyToManyField,
E_TextField=peewee.TextField,
E_DateField=peewee.DateTimeField,
E_BoolField=peewee.BooleanField
)
