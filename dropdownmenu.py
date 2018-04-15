# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

class DropDownMenu(Button):
    drop_list = ListProperty([])
    def __init__(self, height=20, **kwargs):
        self.size_hint_y=None
        self.height=height
        super(DropDownMenu, self).__init__(**kwargs)
        self.dropdown = DropDown()
        for u in self.drop_list:
            btn = Button(text=u, size_hint_y=None, height=height)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.bind(on_release=self.dropdown.open)

class TestApp(App):
    def build(self):
        l = ['tutu', 'toto', 'bonjour', 'oui', 'non', 'hehe']
        return DropDownMenu(text='hoho', drop_list=l, size_hint_y=None, right=.5)

if __name__ == '__main__':
    TestApp().run()
