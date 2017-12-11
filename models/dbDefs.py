from enum import Enum

class FieldType(Enum):
    E_CharField = 1
    E_TextField = 2
    E_DateField = 3
    E_BoolField = 4
    E_LinkField  = 5
    E_TestResField = 6

FieldsDescription = (
  (FieldType.E_CharField, 'TextEntry'),
  (FieldType.E_TextField, 'TextArea'),
  (FieldType.E_DateField, 'Date'),
  (FieldType.E_BoolField, 'Check'),
  (FieldType.E_LinkField, 'Foreign'),
  (FieldType.E_TestResField, 'TextArea'),
)

