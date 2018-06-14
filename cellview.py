# -*- coding: utf-8 -*-
import sys
import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ListProperty

from models.dbDefs import FieldType
from models.dbHelper import whatType

from tablelayout import TableView

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
    def on_width(self, instance, value):
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

class ImageViewCell(TableCell, Image):
    def __init__(self, obj, height=40, **kwargs):
        self.size_hint_y = None
        self.size_hint_x = None
        self.halign = 'center'
        self.valign = 'center'
        self.height=height
        if obj:
            self.source = obj
        super(ImageViewCell, self).__init__(**kwargs)

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

class MultiLinkViewCell(CharViewCell):
    def __init__(self, obj, height=40, **kwargs):
        self.size_hint_y = None
        self.size_hint_x = None
        self.halign = 'center'
        self.valign = 'center'
        self.height=height
        self.shorten = True
        # Here we have an object that is a query to db
        # including list
        #self.text = obj.__str__()
        l = [ o.__str__() for o in obj ]
        s = ','.join(l)
        self.text = s
        super(CharViewCell, self).__init__(**kwargs)
        self.text_size = (self.width, None)

viewWidgetDict=dict(
E_CharField=CharViewCell,
E_TextField=TextViewCell,
E_DateField=CharViewCell,
E_BoolField=BoolViewCell,
E_LinkField=LinkViewCell,
E_ImageField=ImageViewCell,
E_MultiLinkField=MultiLinkViewCell,
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
        whole = [member for _name, member in getmembers(obj) 
                       if name == _name]
        if whole:
            return whole[0]
    except Exception as e:
        raise(e)
    return None

def getmembertype(classe, name):
    return type(getmember(classe, name))

def cells(elem, cells=None):
    classe = type(elem)
    if not cells:
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
            cell.hidden = elem
            cells[e] = cell
    except Exception as e:
        tope, value, traceback = sys.exc_info()
        print('Gloups:', e)
        print(traceback)
    return cells

class ListView(TableView):
    def __init__(self, data):
        # Pour sûr qu'il y a une technique python pour faire ça en une ligne...
        self.data = list()
        for d in data:
            c = CharViewCell(d.__str__())
            c.hidden = d
            self.data.append({'text': c})
        super(ListView, self).__init__(has_top=False)

    # Special case: if there is only one case
    # we can expand them to the width of the boxlayout
    # we are in...
    def on_width(self, instance, value):
        for dictcell in self.data:
            value = list(dictcell.values())[0]
            value.width = self.width

    def set_selected(self, list_elem):
        for r in self.tg.rows:
            e = r[0].hidden
            if e in list_elem:
                r.set_selection(is_selected=True)
    def get_selected(self):
        return [ r[0].hidden for r in self.tg.selection_list ]

# Exemple
class TestApp(App):
    def build(self):
        #l = [cells(e) for e in Eleve.select()]
        l = [cells(r) for r in Resultat.select()]
        #exit(1)
        return TableView(data=l, height='400dp', width='800dp')

if __name__ == '__main__':
    from models.Trombi import Eleve
    from models.Cours import Resultat
    TestApp().run()
