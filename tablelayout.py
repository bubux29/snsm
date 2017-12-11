import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

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
    def __init__(self, keys, width, height, on_release, **kwargs):
        self.orientation = 'horizontal'
        super(TableTop, self).__init__(**kwargs)
        for k in keys:
            b = Button(text=k, width=width, height=height,
                      size_hint_x=None, size_hint_y=None, on_release=on_release)
            # c'est un bouton spécial!!
            b.revert = True
            self.add_widget(b)

class TableCell(Label):
    pass

class TableRow(GridLayout):
    def __init__(self, width, height, dic, **kwargs):
        keys=dic.keys()
        self.cols = len(keys)
        self.size_hint_y=None
        self.size_hint_x=None
        self.height=height
        self.dic = dic
        super(TableRow, self).__init__(**kwargs)
        cells = list()
        for key in keys:
            lab = TableCell(text=dic[key], width=width,
                            height=height, size_hint_y=None, size_hint_x=None)
            cells.append(dic[key])
            self.add_widget(lab)

class TableGrid(BoxLayout):
    def __init__(self, diclist, width, height, **kwargs):
        self.orientation = 'vertical'
        keys = diclist[0].keys()
        self.rows = list()
        self.rowdic = diclist
        self.bind(minimum_height=self.setter('height'))
        self.size_hint_x=None
        self.size_hint_y = None
        super(TableGrid, self).__init__(**kwargs)
        for elem in diclist:
            row = TableRow(dic=elem, width=width, height=height)
            self.rows.append(row)
            self.add_widget(row)

class TableView(BoxLayout):
    def on_release(self, instance):
        key = instance.text
        #to_sort = [dic[key] for dic in self.data]
        #print(sorted(to_sort))
        ordered_rows = sorted(self.tg.rows, key=lambda row: row.dic[key])

        if instance.revert:
            ordered_rows = reversed(ordered_rows)
        instance.revert = not instance.revert
        self.tg.clear_widgets()
        for row in ordered_rows:
            self.tg.add_widget(row)

    def __init__(self, dic, window_height, window_width, **kwargs):
        self.orientation = 'vertical'
        self.data = dic
        col_width = '200dp'
        super(TableView, self).__init__(**kwargs)
        self.add_widget(TableTop(dic[0].keys(), width=col_width, height=20, on_release=self.on_release))
        sc = ScrollView(size_hint_y=None, size_hint_x=None,
                        height=window_height, width=window_width)
        self.add_widget(sc)
        self.tg = TableGrid(dic, width=col_width, height=30)
        sc.add_widget(self.tg)

class TestApp(App):
    def build(self):
        l = [{'nom': eleve.__str__(), 'tel': eleve.telephone, 'photo': eleve.photo_path}
             for eleve in formation_db.liste_eleves_all()]
        return TableView(l, '200dp', '800dp')

if __name__ == '__main__':
    TestApp().run()
