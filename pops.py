import kivy
kivy.require('1.10.0')

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App

from kivy.properties import ObjectProperty

Builder.load_string(
'''
<MenuComment>:
    comments_txt: comments
    valider_btn: valider
    orientation: 'vertical'
    size_hint: (1,1)
    pos_hint: {"top": 1, "center_x": .5}
    padding: 10
    spacing: 20
    Label:
        id: comments
        size_hint: .1,.1
        pos_hint: {"top": .9, "center_x": .5}
    Button:
        id: valider
        size_hint: None,.1
        pos_hint: {"top": .1, "center_x": .8}
        text: 'Valider'
''')

class MenuComment(BoxLayout):
    comments_txt = ObjectProperty(None)
    valider_btn = ObjectProperty(None)
    def __init__(self, popup=None, **kwargs):
        super(MenuComment, self).__init__(**kwargs)
        self.orientation = "vertical"
        #self.size_hint = (.5,.5)
        self.popup=popup

    def on_valider(self, inst):
        if self.popup != None:
            self.popup.dismiss()


def _pop_(popup, title, text):
    if popup == None:
        popup = Popup(title=title)
        content = MenuComment()
        content.valider_btn.bind(on_release=popup.dismiss)
        popup.content = content
        popup.size_hint = (0.5, 0.5)
    content.comments_txt.text=text
    popup.open()

def pop_warn(popup, text):
    _pop_(popup, "Attention", text)

def pop_ok(popup, text):
    _pop_(popup, "Validé", text)

class TestApp(App):
    def build(self):
        return pop_warn(None, "Attention les cons!!!")
if __name__ == '__main__':
    TestApp().run()
