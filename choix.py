#!/usr/bin/env python3
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty, StringProperty

class Choix(ToggleButton):
    pass

class ChoixUnique(BoxLayout):
    button_size_hint = ObjectProperty((1,1))
    button_pos_hint = ObjectProperty({})
    liste_choix = ListProperty([])
    group = StringProperty('')
    def __init__(self, liste_choix, *args, **kwargs):
        self.liste_choix = liste_choix
        super(ChoixUnique, self).__init__(*args, **kwargs)
        self.on_liste_choix(self.liste_choix)

    def on_liste_choix(self, liste):
        if not self: return
        self.liste_widgets = list()
        for choix in liste:
            c = Choix(text=choix, pos_hint=self.button_pos_hint,
                    size_hint=self.button_size_hint, group=self.group)
            self.liste_widgets.append(c)
            self.add_widget(c)

    def choix(self):
        for w in self.liste_widgets:
            if w.state == 'down':
                return w.text
        return ''

class TestApp(App):
    def build(self):
        l = ['Succ', 'Eche', 'Prout']
        c = ChoixUnique(size=(400,400), liste_choix=l, button_size_hint=(.3,.3))
        return c

if __name__ == '__main__':
    TestApp().run()
