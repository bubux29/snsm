#!/usr/bin/env python3

from pops import Texte
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty


class TexteEntree(TextInput):
    popup = ObjectProperty(None)
    title = StringProperty('')
    texte = ObjectProperty(None)

    def on_open(self, instance):
        self.texte.textinput.focus = True

    def on_dismiss(self, instance):
        self.bind(on_focus=self.on_focus)

    def on_focus(self, instance, value):
        if not self.popup:
            self.popup = Popup(title=self.title, size_hint=(.5,.5), pos_hint={'top': 1})
        if not self.texte:
            self.texte = Texte(text=self.text, valider=self.on_valider, in_popup=True, multiline=self.multiline)
            self.popup.bind(on_open=self.on_open, on_dismiss=self.on_dismiss)
        if self.popup._window is not None:
            return
        self.popup.content = self.texte
        self.popup.open()

    def on_valider(self, text):
        self.text = text
        self.popup.dismiss()

class TestApp(App):
    def build(self):
        return TexteEntree()

if __name__ == '__main__':
    TestApp().run()
