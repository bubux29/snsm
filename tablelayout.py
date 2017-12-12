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

from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ListProperty, DictProperty

from collections import OrderedDict
import formation_db

Builder.load_string('''
<TopButton@Button>
    size: root.size
    canvas:
        Rotate:
            angle: 2
            
''')
class TopButton(Button):
    pass

class TableTop(BoxLayout):
    cells = ObjectProperty(None)
    def __init__(self, on_release, **kwargs):
        self.orientation = 'horizontal'
        super(TableTop, self).__init__(**kwargs)
        for c in self.cells.values():
            b = Button(text=c.name, width=c.width, height=self.height,
                      size_hint_x=None, size_hint_y=None, on_release=on_release)
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
        self.size_hint_x = None
        self.size_hint_y = None
        super(TableGrid, self).__init__(**kwargs)
        keys = self.data[0].keys()
        for elem in self.data:
            # On parcourt les cellules pour trouver la plus haute et on récupère
            # sa hauteur
            maxheight = max(elem.values(), key=lambda x: x.height).height
            row = TableRow(dic=elem, height=maxheight)
            self.rows.append(row)
            self.add_widget(row)

class TableView(BoxLayout):
    window_height = StringProperty('')
    window_width = StringProperty('')
    data = ListProperty([])
    def on_release(self, instance):
        key = instance.text
        #to_sort = [dic[key] for dic in self.data]
        #print(sorted(to_sort))
        ordered_rows = sorted(self.tg.rows, key=lambda row: row.dic[key].text)

        if not instance.revert:
            ordered_rows = reversed(ordered_rows)
        instance.revert = not instance.revert
        self.tg.clear_widgets()
        for row in ordered_rows:
            self.tg.add_widget(row)

    def __init__(self, **kwargs):
        self.orientation = 'vertical'
        super(TableView, self).__init__(**kwargs)
        #self.add_widget(TableTop(dic[0].keys(), width=col_width, height=20, on_release=self.on_release))
        self.add_widget(TableTop(cells=self.data[0],
                                 height=20, on_release=self.on_release))
        sc = ScrollView(size_hint_y=None, size_hint_x=None,
                        height=self.window_height, width=self.window_width)
        self.add_widget(sc)
        self.tg = TableGrid(data=self.data, width=self.width, height=30)
        sc.add_widget(self.tg)

class TestApp(App):
    class Cell(TableCell, Label):
        def __init__(self, **kwargs):
            self.size_hint_y = None
            self.size_hint_x = None
            self.size = self.texture_size
            self.height=40
            self.shorten = True
            super(TestApp.Cell, self).__init__(**kwargs)
            self.text_size = (self.width, None)
    def build(self):
        l = [OrderedDict({
           'nom': TestApp.Cell(name='nom', text=eleve.__str__(), width=180),
           'tel': TestApp.Cell(name='tel', text=eleve.telephone, width=150),
           'photo': TestApp.Cell(name='photo', text=eleve.photo_path, width=150)
           })
             for eleve in formation_db.liste_eleves_all()]
        return TableView(data=l, window_height='200dp', window_width='800dp')

if __name__ == '__main__':
    TestApp().run()
