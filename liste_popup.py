#!/usr/bin/env python3

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup

class PopupList(TextInput):
    def __init__(self, selections, titre, apres_reponse, *args, **kwargs):
        super(PopupList, self).__init__(*args, **kwargs)
        self.apres_reponse = apres_reponse
        self.selections = selections
        self.reponse = -1
        self.listeBoutons = ListeBoutons(selections, self.reponse)
        self.popup = Popup(content=self.listeBoutons,
                           on_dismiss=self.update_value, title=titre)
        self.popup.size_hint = (.9,.9)
        self.listeBoutons.parent_popup = self.popup

        self.bind(focus=self.show_popup)

    def show_popup(self, inst, val):
        self.listeBoutons.size = self.popup.size
        if val:
            # On laisse béton les éventuelles appui clavier
            Window.release_all_keyboards()
            self.popup.open()

    def update_value(self, instance):
        self.text = self.selections[self.reponse]
        self.focus = False
        # on appelle la fonction passé par le client avec l'index de la 
        # sélection
        if self.apres_reponse:
            self.apres_reponse(self.reponse)

class ListeBoutons(BoxLayout):

    def __init__(self, selections, reponse_index, **kwargs):
        super(ListeBoutons, self).__init__(**kwargs)
        self.orientation = 'vertical'
        #self.size = (Window.width*.8, Window.height*.8)
        #self.size_hint = (None, None)
        self.pos_hint = {"top": 1, "right": .5}#, "center_x": .5}
        sc = ScrollView(size_hint=(None, None), size=self.size,
                        pos_hint={'top': 1, 'center_x': .5}, do_scroll_x=False)

        self.add_widget(sc)
        bit = GridLayout(cols=1, size=self.size, size_hint=(None,None))
        bit.bind(minimum_height=bit.setter('height'))
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
