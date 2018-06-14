# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App

from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

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
        
<Question>:
    description: description
    valider_btn: valider_btn
    annuler_btn: annuler_btn
    size_hint: (1,1)
    pos_hint: {"top": 1, "center_x": .5}
    orientation: 'vertical'
    Label:
        id: description
        size: self.texture_size
        text_size: root.width, None
        valign: 'top'
        halign: 'left'
        #size_hint: 1, .9
        pos_hint: {'top': 1, 'center_x': .5, 'center_y': .8}
    BoxLayout:
        size_hint: .5, .1
        pos_hint: {'top': .1, 'center_x': .5}
        orientation: 'horizontal'
        Button:
            id: annuler_btn
            size_hint: .5, 1
            #pos_hint: {'top': .1, 'center_x': .1}
            text: root.annuler_txt
            on_release:
                root.annuler_()
        Button:
            id: valider_btn
            size_hint: .5, 1
            #pos_hint: {'top': .1, 'center_x': .5}
            text: root.valider_txt
            on_release:
                root.valider_()
''')

class Question(BoxLayout):
    valider = ObjectProperty(None)
    valider_txt = StringProperty('Valider')
    valider_btn = ObjectProperty(None)
    annuler = ObjectProperty(None)
    annuler_txt = StringProperty('Annuler')
    annuler_btn = ObjectProperty(None)
    text = StringProperty(None)
    description = ObjectProperty(None)
    in_popup = BooleanProperty(False)

    def annuler_(self):
        if self.annuler:
            self.annuler()
        if self.in_popup:
            self.parent.parent.parent.dismiss()

    def valider_(self):
        if self.valider:
            self.valider()
        if self.in_popup:
            self.parent.parent.parent.dismiss()

    def on_text(self, instance, value):
        if self.description:
            self.description.text = value
    def on_description(self, instance, value):
        if self.text:
            self.description.text = self.text
    def on_valider_txt(self, instance, value):
        if self.valider_btn:
            self.valider_btn.text = value
    def on_valider_btn(self, instance, value):
        self.valider_btn.text = self.valider_txt
    def on_annuler_txt(self, instance, value):
        if self.annuler_btn:
            self.annuler_btn.text = value
    def on_annuler_btn(self, instance, value):
        self.annuler_btn.text = self.annuler_txt

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

def question_pop(popup, title, text, on_valider, **kwargs):
    content = Question(text=text, valider=on_valider, in_popup=True, **kwargs)
    if popup == None:
        popup = Popup(title=title, size_hint=(.5, .5))
    popup.content = content
    popup.open()

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

def show(*args):
    print('coucou', args)

class TestApp(App):
    def build(self):
        #return pop_warn(None, "Attention les cons!!!")
        return question_pop(None, "Attention les cons!!!", 'Etes-vous sur de continuer bande de cons?!\nsinon taper 1', on_valider=show)
if __name__ == '__main__':
    TestApp().run()
