#!/usr/bin/env python3

import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

import os

Builder.load_string(
'''
<FilePreview>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            nom_fichier_selectionne: nom_fichier_selectionne
            titre: titre
            BoxLayout:
                orientation: 'vertical'
                Label:
                    id: titre
                    text: root.curdir
                    size_hint_y: .1
                FileChooserListView:
                    id: liste_fichiers
                    size_hint: (1, 1)
                    path: root.curdir
                    filters: root.filters
                    on_path: titre.text = self.path
                    on_selection:
                        if self.selection: image.source = self.selection[0]
                        if self.selection: nom_fichier_selectionne.text = self.selection[0]
            BoxLayout:
                orientation: 'vertical'
                Label:
                    size_hint_y: .1
                    id: nom_fichier_selectionne
                BoxLayout:
                    Image:
                        id: image
        BoxLayout:
            orientation: 'horizontal'
            size_hint: (.5, .1)
            Button:
                text: 'Annuler'
                on_release: root.annuler()
            Button:
                text: 'Sélectionner'
                on_release:
                    root.valider(liste_fichiers.selection)
''')

def dirname(path):
    split = path.split('/')
    if split:
        dirname = '/'.join(split[:-1])
        basename = split[-1]
    else:
        dirname = '.'
        basename = '*'
    return os.path.abspath(dirname), basename.split(',')

class FilePreview(FloatLayout):
    titre = ObjectProperty()
    nom_fichier_selectionne = ObjectProperty()
    path_image = StringProperty()
    image = ObjectProperty()
    valider = ObjectProperty(None)
    annuler = ObjectProperty(print)
    def __init__ (self, dir_with_filter = '.', **kwargs):
        self.curdir, self.filters = dirname(dir_with_filter)
        super(FilePreview, self).__init__(**kwargs)

class TestApp(App):
    def build(self):
        return FilePreview('pics/*.jpg', size = (400,400), valider=print)

if __name__ == '__main__':
    TestApp().run()
