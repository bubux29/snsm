#!/usr/bin/env python3

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup

from kivy.properties import NumericProperty, ReferenceListProperty

class PopupList(TextInput):
    hint_x = NumericProperty(0.9)
    hint_y = NumericProperty(0.9)
    hint_xy = ReferenceListProperty(hint_x, hint_y)
    #def __init__(self, selections, titre, apres_reponse, *args, **kwargs):
        #super(PopupList, self).__init__(*args, **kwargs)
    def init(self, selections, titre, apres_reponse):
        self.titre = titre
        self.apres_reponse = apres_reponse
        self.selections = selections
        self.listeBoutons = ListeBoutons(selections)
        self.popup = Popup(content=self.listeBoutons,
                           on_dismiss=self.update_value, title=titre)
        self.listeBoutons.parent_popup = self.popup

        self.bind(focus=self.show_popup)

    def show_popup(self, inst, val):
        self.popup.size_hint = self.hint_xy
        #self.listeBoutons.size = self.popup.size
        if val:
            # On laisse béton les éventuelles appui clavier
            Window.release_all_keyboards()
            self.popup.open()

    def update_value(self, instance):
        self.text = self.selections[self.listeBoutons.reponse_index]
        self.focus = False
        # on appelle la fonction passé par le client avec l'index de la 
        # sélection
        if self.apres_reponse:
            self.apres_reponse(self.listeBoutons.reponse_index)

class ListeBoutons(BoxLayout):
    def __init__(self, selections, **kwargs):
        kwargs['orientation'] = 'vertical'
        super(ListeBoutons, self).__init__(**kwargs)
        self.reponse_index = -1

        sc = ScrollView(do_scroll_x=False, size_hint=(.9,.9), pos_hint={'center_x': .5})
        self.add_widget(sc)

        bit = BoxLayout(orientation='vertical')
        sc.add_widget(bit)
        index = 0
        for text in selections:
            button = Button(text=str(text),
                    color=(1,1,1,1),
                    font_size=20, size_hint=(1,0.1),
                    markup=True)
            bit.add_widget(button)
            button.bind(on_press=self.bouton_presse)
            button.index = index
            index += 1
    def bouton_presse(self, instance):
        self.reponse_index = instance.index
        if self.parent_popup:
            self.parent_popup.dismiss()
        
