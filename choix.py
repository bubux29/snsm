#!/usr/bin/env python3
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty, StringProperty

from random import _urandom

class Choix(ToggleButton):
    pass

class ChoixUnique(BoxLayout):
    button_size_hint = ObjectProperty((1,1))
    button_pos_hint = ObjectProperty({})
    liste_choix = ListProperty([])
    prechoix = ObjectProperty(None)
    def __init__(self, liste_choix, *args, **kwargs):
        self.liste_choix = liste_choix
        self.liste_widgets = list()
        self.group = str(_urandom(64))
        super(ChoixUnique, self).__init__(*args, **kwargs)
        self.on_liste_choix(self.liste_choix)
        self.on_prechoix(None, None)

    def on_liste_choix(self, liste):
        if not self: return
        for choix in liste:
            c = Choix(text=choix, pos_hint=self.button_pos_hint,
                    size_hint=self.button_size_hint, group=self.group)
            self.liste_widgets.append(c)
            self.add_widget(c)

    def on_prechoix(self, instance, value):
        for c in self.liste_widgets:
            if self.prechoix == c.text:
                c.state = 'down'

    def text(self):
        for w in self.liste_widgets:
            if w.state == 'down':
                return w.text
        return ''

class TestApp(App):
    def build(self):
        w = BoxLayout(orientation='vertical')
        l = ['Succ', 'Eche', 'Prout']
        c = ChoixUnique(size=(400,400), prechoix='Prout', liste_choix=l, button_size_hint=(.3,.3))
        w.add_widget(c)
        c = ChoixUnique(size=(400,400), prechoix='Succ', liste_choix=l, button_size_hint=(.3,.3))
        w.add_widget(c)
        return w

if __name__ == '__main__':
    TestApp().run()
