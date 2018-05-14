from enum import Enum

class FieldType(Enum):
    E_CharField = 1
    E_TextField = 2
    E_DateField = 3
    E_BoolField = 4
    E_LinkField  = 5
    E_MultiLinkField  = 6
    E_TestResField = 7
    E_ImageField = 8

FieldsDescription = (
  (FieldType.E_CharField, 'TextEntry'),
  (FieldType.E_TextField, 'TextArea'),
  (FieldType.E_DateField, 'Date'),
  (FieldType.E_BoolField, 'Check'),
  (FieldType.E_LinkField, 'Foreign'),
  (FieldType.E_MultiLinkField, 'ManyToMany'),
  (FieldType.E_TestResField, 'TextArea'),
  (FieldType.E_ImageField, 'Image'),
)

