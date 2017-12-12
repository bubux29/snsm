import sys
import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import BooleanProperty

from models.dbDefs import FieldType
from models.dbHelper import whatType

from inspect import getmembers
from collections import OrderedDict

from tablelayout import TableCell

class CharViewCell(TableCell, Label):
    def __init__(self, obj, height=40, **kwargs):
        self.size_hint_y = None
        self.size_hint_x = None
        self.height=height
        self.shorten = True
        if obj:
            self.text = obj
        else:
            self.text = ''
        self.halign = 'center'
        self.valign = 'center'
        super(CharViewCell, self).__init__(**kwargs)
        self.text_size = (self.width, None)

class TextViewCell(CharViewCell):
    pass

class BoolViewCell(TableCell, Label):
    is_true = BooleanProperty(False)
    def __init__(self, obj, height=40, **kwargs):
        self.size_hint_y = None
        self.size_hint_x = None
        self.width = 10
        self.height=height
        self.shorten = True
        self.is_true = obj
        super(CharViewCell, self).__init__(**kwargs)
        self.text_size = (self.width, None)
        if self.is_true == True:
            self.text = 'V'
        else:
            self.text = 'X'

class LinkViewCell(CharViewCell):
    def __init__(self, obj, height=40, **kwargs):
        self.size_hint_y = None
        self.size_hint_x = None
        self.halign = 'center'
        self.valign = 'center'
        self.height=height
        self.shorten = True
        self.text = obj.__str__()
        super(CharViewCell, self).__init__(**kwargs)
        self.text_size = (self.width, None)

viewWidgetDict=dict(
E_CharField=CharViewCell,
E_TextField=TextViewCell,
E_DateField=CharViewCell,
E_BoolField=BoolViewCell,
E_LinkField=LinkViewCell,
)

class StdCellView:
    def factory(celltype, obj, **kwargs):
        try:
            classe = viewWidgetDict[celltype] 
            return classe(obj, **kwargs)
        except Exception as e:
            raise(e)

def getmember(obj, name):
    try:
        return [member for _name, member in getmembers(obj) 
                       if name == _name][0]
    except Exception as e:
        raise(e)

def getmembertype(classe, name):
    return type(getmember(classe, name))

def cells(elem):
    classe = type(elem)
    cells = OrderedDict()
    try:
        for e,w in classe.affichage:
            # On ne peut pas facilement récupérer le type à partir de:
            # elem.nom_champ
            # alors que depuis:
            # classe(elem).nom_champ
            # c'est possible :-)
            typ = whatType(getmembertype(classe,e))
            val = getmember(elem, e)
            cell = StdCellView.factory(typ, val, width=w, name=e)
            cells[e] = cell
    except Exception as e:
        tope, value, traceback = sys.exc_info()
        print('Gloups:', e)
        print(traceback)
    return cells

# Exemple
class TestApp(App):
    def build(self):
        #l = [cells(e) for e in Eleve.select()]
        l = [cells(r) for r in Resultat.select()]
        #exit(1)
        return TableView(data=l, window_height='400dp', window_width='800dp')

if __name__ == '__main__':
    from models.Trombi import Eleve
    from models.Cours import Resultat
    from tablelayout import TableView
    TestApp().run()
