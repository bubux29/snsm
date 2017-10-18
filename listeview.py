import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

import formation_db

Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.3, .9, .6) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<ListeView>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: root.multiselect
        touch_multiselect: root.touch_multiselect
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            rv.liste_des_textes.append(rv.data[index]['text'])
            if 'elem' in rv.data[index] and rv.data[index]['elem']:
                rv.liste_des_elem.append(rv.data[index]['elem'])
        else:
            print("selection removed for {0}".format(rv.data[index]['text']))
            if rv.liste_des_textes.count(rv.data[index]['text']):
                rv.liste_des_textes.remove(rv.data[index]['text'])
                if 'elem' in rv.data[index] and rv.data[index]['elem']:
                    rv.liste_des_elem.remove(rv.data[index]['elem'])
        if rv.apply_callback:
            rv.apply_callback(rv.liste_des_textes, rv.liste_des_elem)


class ListeView(RecycleView):
    def __init__(self, selections, has_multi, change_callback=None, **kwargs):
        if has_multi:
            self.multiselect = True
            self.touch_multiselect = True
        else:
            self.multiselect = False
            self.touch_multiselect = False
        super(ListeView, self).__init__(**kwargs)
        self.data =  selections
        self.liste_des_textes = list()
        self.liste_des_elem = list()
        self.apply_callback = change_callback

class TestApp(App):
    def build(self):
        l = [{'text': cour.nom} for cour in formation_db.liste_cours_all()]
        return ListeView(l, True)

if __name__ == '__main__':
    TestApp().run()
