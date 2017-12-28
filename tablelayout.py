import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ListProperty

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

class TableCell(Widget):
    name = StringProperty('unk')
    text = StringProperty('unk')
    pass

class TableRow(GridLayout):
    def __init__(self, dic, **kwargs):
        self.dic = dic
        self.size_hint_y=None
        self.size_hint_x=None
        super(TableRow, self).__init__(**kwargs)
        keys=self.dic.keys()
        self.cols = len(keys)
        cells = list()
        for key in keys:
            lab = self.dic[key]
            cells.append(self.dic[key])
            self.add_widget(lab)

class TableGrid(BoxLayout):
    data = ListProperty([])
    def __init__(self, **kwargs):
        self.orientation = 'vertical'
        self.rows = list()
        self.bind(minimum_height=self.setter('height'))
        self.bind(minimum_width=self.setter('width'))
        self.size_hint_x = None
        self.size_hint_y = None
        super(TableGrid, self).__init__(**kwargs)
        keys = self.data[0].keys()
        for elem in self.data:
            # On parcourt les cellules pour trouver la plus haute et on récupère
            # sa hauteur
            maxheight = max(elem.values(), key=lambda x: x.height).height
            row = TableRow(dic=elem, height=maxheight, width=self.width)
            self.rows.append(row)
            self.add_widget(row)

class TableView(ScrollView):
    data = ListProperty([])
    table = ObjectProperty(None)
    topheight = NumericProperty(20)

    def sorting(self, instance):
        key = instance.text
        ordered_rows = sorted(self.tg.rows, key=lambda row: row.dic[key].text)

        if not instance.revert:
            ordered_rows = reversed(ordered_rows)
        instance.revert = not instance.revert
        self.tg.clear_widgets()
        for row in ordered_rows:
            self.tg.add_widget(row)

    def __init__(self, **kwargs):
        super(TableView, self).__init__(**kwargs)
        if len(self.data) == 0:
            return
        tb = TableTop(cells=self.data[0], height=self.topheight,
                                          on_release=self.sorting)
        self.table.add_widget(tb)
        total_width = sum([ c.width for c in self.data[0].values() ])
        self.tg = TableGrid(data=self.data, width=total_width, height=30)
        self.table.add_widget(self.tg)

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
        return TableView(data=l, width=600, height=300)

if __name__ == '__main__':
    TestApp().run()
