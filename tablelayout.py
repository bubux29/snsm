# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ListProperty, BooleanProperty

import re
from collections import OrderedDict
import formation_db

Builder.load_string('''
<TableView@ScrollView>:
    table: table
    size_hint: None, None
    pos_hint: {'center_x': .5, 'center_y': .5}

    GridLayout:
        cols: 1
        padding: 5
        spacing: 5
        height: self.minimum_height
        width: self.minimum_width
        size_hint: None, None
        id: table
<TableCell>:
    canvas.before:
        Color:
            rgba: (.0, .3, .9, .6) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    on_press:
        self.selected = not self.selected
''')

class TopButton(Button):
    pass

class TableTop(BoxLayout):
    cells = ObjectProperty(None)
    def __init__(self, on_release, **kwargs):
        self.orientation = 'horizontal'
        self.size_hint = (None, None)
        super(TableTop, self).__init__(**kwargs)
        for c in self.cells.values():
            b = Button(text=c.name, width=c.width, height=self.height,
                      size_hint_x=None, size_hint_y=None, on_release=on_release,
                      text_size = (self.width, None), halign = 'center',
                      shorten=True)
            # c'est un bouton spécial!!
            b.revert = True
            self.add_widget(b)

class TableSearch(BoxLayout):
    cells = ObjectProperty(None)

    def __init__(self, on_textsearch, **kwargs):
        self.orientation = 'horizontal'
        self.size_hint = (None, None)
        self.on_textsearch = on_textsearch
        super(TableSearch, self).__init__(**kwargs)
        for c in self.cells.values():
            b = TextInput(width=c.width, height=self.height,
                      size_hint_x=None, size_hint_y=None, multiline=False)
            b.bind(text=self.search)
            b.column = c.name
            self.add_widget(b)

    def search(self, instance, value):
        if self.on_textsearch:
            self.on_textsearch(instance.column, value)


class TableCell(ButtonBehavior, Widget):
    name = StringProperty('unk')
    text = StringProperty('unk')
    selected = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(TableCell, self).__init__(**kwargs)

class TableRow(GridLayout):

    def __init__(self, dic, selection_list, on_row_selection, **kwargs):
        self.dic = dic
        self.root_selection_list = selection_list
        self.on_row_selection = on_row_selection
        self.size_hint_y=None
        self.size_hint_x=None
        super(TableRow, self).__init__(**kwargs)
        keys=self.dic.keys()
        self.cols = len(keys)
        self.cells = list()
        for key in keys:
            lab = self.dic[key]
            self.cells.append(lab)
            self.add_widget(lab)
            lab.bind(on_press=self.on_sel)

    def matching_cells(self, matching_dic):
        return [cell for cell in self.cells if cell.name in matching_dic and cell.text == matching_dic[cell.name]]

    def has_elem_in(self, matching_dic):
        return len(self.matching_cells(matching_dic))

    def on_sel(self, instance):
        is_selected = not instance.selected
        self.set_selection(instance, is_selected)
        if self.on_row_selection:
            self.on_row_selection(instance, is_selected)

    def set_selection(self, instance = None, is_selected = True):
        if is_selected:
            self.root_selection_list.append(self)
        else:
            try:
                self.root_selection_list.remove(self)
            except:
                pass
        for cell in self.cells:
            if instance == cell:
                pass
            else:
                cell.selected = is_selected
    def keys(self):
        return self.dic.keys()

    def __len__(self):
        return self.cols

    def __getitem__(self, key):
        if type(key) == int:
            return self.cells[key]
        else:
            return self.dic[key]
    def __setitem__(self, key, value):
        self.dic[key] = value
    def __delitem__(self, key):
        return self.dic.remove(key)
    def __iter__(self):
        for k in self.dic.values():
            yield k
    def __contains__(self, item):
        if item in self.dic:
            return True
        else:
            return False

class TableGrid(BoxLayout):
    data = ListProperty([])
    selection_list = ListProperty([])
    def __init__(self, on_row_selection=None, **kwargs):
        self.orientation = 'vertical'
        self.rows = list()
        self.bind(minimum_height=self.setter('height'))
        self.bind(minimum_width=self.setter('width'))
        self.size_hint_x = None
        self.size_hint_y = None
        super(TableGrid, self).__init__(**kwargs)
        self.late_sort = (None, None)
        keys = self.data[0].keys()
        for elem in self.data:
            # On parcourt les cellules pour trouver la plus haute et on récupère
            # sa hauteur
            maxheight = max(elem.values(), key=lambda x: x.height).height
            row = TableRow(dic=elem, on_row_selection=on_row_selection, height=maxheight, width=self.width, selection_list=self.selection_list)
            self.rows.append(row)
            self.add_widget(row)
        # On se garde la liste complète pour la recherche
        self.whole_rows = self.rows[:]

    def select(self, selection_dic):
        for row in self.rows:
            if row.has_elem_in(selection_dic):
                row.cells[0].selected = True

    def sorting(self, instance):
        key = instance.text
        ordered_rows = sorted(self.rows, key=lambda row: row.dic[key].text)

        if not instance.revert:
            ordered_rows = reversed(ordered_rows)
        instance.revert = not instance.revert
        self.update_rows(ordered_rows)
        self.late_sort = ( key, instance.revert )

    def searching(self, key, value_to_search):
        # Y a-t-il eu avant un tri
        if self.late_sort[0]:
            rows = sorted ([ row for row in self.whole_rows
                    if re.search( value_to_search, row[key], re.M|re.I) ])
        else:
            rows = [ row for row in self.whole_rows
                    if re.search( value_to_search, row[key].text, re.M|re.I) ]
        self.update_rows(rows)

    def update_rows(self, rows):
        self.clear_widgets()
        for row in rows:
            self.add_widget(row)


class TableView(ScrollView):
    data = ListProperty([])
    table = ObjectProperty(None)
    tg = ObjectProperty(None)
    topheight = NumericProperty(20)

    def __init__(self, has_top=True, has_search=False, **kwargs):
        super(TableView, self).__init__(**kwargs)
        if len(self.data) == 0:
            return
        total_width = sum([ c.width for c in self.data[0].values() ])
        self.tg = TableGrid(data=self.data, width=total_width, height=30)
        if has_top:
            tb = TableTop(cells=self.data[0], height=self.topheight,
                                              on_release=self.tg.sorting)
            self.table.add_widget(tb)
        if has_search:
            ts = TableSearch(on_textsearch=self.tg.searching, cells=self.data[0], height=self.topheight + 12)
            self.table.add_widget(ts)
        self.table.add_widget(self.tg)

#    def __len__(self):
#        if self.tg:
#            return len(self.tg.rows)
#        else:
#            return 0
#
#    def __getitem__(self, key):
#        if type(key) == int:
#            return self.tg.rows[key]
#    def __setitem__(self, key, value):
#        self.tg.rows[key] = value
#    def __delitem__(self, key):
#        return self.tg.rows.remove(key)
#    def __iter__(self):
#        for r in self.tg.rows:
#            yield r
#    def __contains__(self, item):
#        if item in self.tg.rows:
#            return True
#        else:
#            return False

    def get_selected(self):
        return self.tg.selection_list

#    def set_selected(self, name_list):
#        self.tg.select(name_list)

class TestApp(App):
    class Cell(TableCell, Label):
        def __init__(self, **kwargs):
            self.size_hint_y = None
            self.size_hint_x = None
            self.size = self.texture_size
            self.height=40
            self.halign = 'center'
            self.shorten = True
            super(TestApp.Cell, self).__init__(**kwargs)
            self.text_size = (self.width, None)
    def build(self):
        l = [OrderedDict({
           'nom': TestApp.Cell(name='nom', text=eleve.__str__(), width=180),
           'tel': TestApp.Cell(name='tel', text=eleve.telephone, width=250),
           'photo': TestApp.Cell(name='photo', text=eleve.photo_path, width=150),
           'pudu' : TestApp.Cell(name='pudu', text='oh oui', width=300)
           })
             for eleve in formation_db.liste_eleves_all()]
        return TableView(data=l, has_search=True, width=600, height=300)

if __name__ == '__main__':
    TestApp().run()
