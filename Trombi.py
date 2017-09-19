#!/usr/bin/env python3

import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

import formation_db

Builder.load_string('''
<SelectableBox>:
    #size: self.size
    #pos: self.pos
    photo: ''
    nom: ''
    orientation: 'vertical'
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.3, .9, .6) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.x, self.y
            size: self.width, self.height/2
    BoxLayout:
        #size_hint: .5,.5
        orientation: 'vertical'
        Image:
            allow_stretch: False
            #keep_ratio: True
            keep_ratio: False
            size_hint_y: None
            size_hint_x: None
            pos_hint: {'center_x': .5, 'top': .8}
            width: self.parent.width*.5
            height: self.parent.height*.5
            source: root.photo
        Label:
            text: root.nom
            pos_hint: {'center_x': .5, 'top': .2}

<ListeView>:
    viewclass: 'SelectableBox'
    SelectableRecycleBoxLayout:
        default_size: dp(150), dp(150)
        scroll_type: ['bars', 'content']
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


class SelectableBox(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableBox, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBox, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            rv.liste_des_index.append(index)
        else:
            print("selection removed for {0}".format(rv.data[index]))
            if index in rv.liste_des_index:
                rv.liste_des_index.remove(index)


class ListeView(RecycleView):
    def __init__(self, selections, has_multi, **kwargs):
        if has_multi:
            self.multiselect = True
            self.touch_multiselect = True
        else:
            self.multiselect = False
            self.touch_multiselect = False
        super(ListeView, self).__init__(**kwargs)
        self.data =  selections
        self.liste_des_index = list()


class TestApp(App):
    def build(self):
        l = [{'nom': eleves.__str__(), 'photo': eleves.photo_path} for eleves in formation_db.liste_eleves_all()]
        return ListeView(l, True)

if __name__ == '__main__':
    TestApp().run()
