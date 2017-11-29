import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import RecycleLayoutManagerBehavior, LayoutSelectionBehavior, RecycleDataViewBehavior

from kivy.properties import ObjectProperty
import formation_db

#import traceback
        #for line in traceback.format_stack():
            #print(line.strip())

Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.3, .9, .6) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<ListeView>:
    sl: sl
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        id: sl
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: root.multiselect
        touch_multiselect: root.touch_multiselect
''')

def dictIndexOf(dic, value):
    return list(dic.values()).index(value)

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. ''' 
    _formerly_selected_views = None
    _selected_views = None
    def __init__(self, **kwargs):
        self._formerly_selected_views = list()
        self._selected_views = list()
        super(SelectableRecycleBoxLayout, self).__init__(**kwargs)

    def apply_selection(self, index, view, is_selected):
        super(SelectableRecycleBoxLayout, self).apply_selection(index, view, is_selected)

    # On doit maintenir la liste des éléments sélectionnés
    def select_node(self, node):
        view = self.recycleview.view_adapter.get_visible_view(node)
        if view and not self._selected_views.count(view.text): 
            self._selected_views.append(view.text)
        super(SelectableRecycleBoxLayout, self).select_node(node)
    def deselect_node(self, node):
        try:
            self._selected_views.remove(self.recycleview.view_adapter.get_visible_view(node).text)
        except:
            pass
        super(SelectableRecycleBoxLayout, self).deselect_node(node)

    def clear_selected_views(self):
        views = self.recycleview.view_adapter.views
        to_remove = self._selected_views[:]
        for vtext in to_remove:
            node = [v.index for v in views.values() if v.text == vtext]
            if node:
                self.deselect_node(node[0])

    # Quand on met à jour rv.data, on chamboule complétement la liste des
    # views, il faut donc vider la liste pour qu'elle soit ensuite recréer
    # quand on met à jour views
    def unselect_views(self):
        to_remove = self.selected_nodes[:]
        for n in to_remove:
            # il ne faut pas passer par la case: retrait de la view de la liste
            super(SelectableRecycleBoxLayout, self).deselect_node(n)
    def reselect_views(self):
        views = self.recycleview.view_adapter.views
        to_select = self._selected_views[:]
        for vtext in to_select:
            node = [v.index for v in views.values() if v.text == vtext]
            if node:
                self.select_node(node[0])

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed ({0}) to {0}".format(index,rv.data[index]['text']))
            if not rv.liste_des_textes.count(rv.data[index]['text']):
                rv.liste_des_textes.append(rv.data[index]['text'])
                if 'elem' in rv.data[index] and rv.data[index]['elem']:
                    rv.liste_des_elem.append(rv.data[index]['elem'])
        else:
            #for line in traceback.format_stack():
                #print(line.strip())
            print("selection removed for {0}".format(rv.data[index]['text']))
            if rv.liste_des_textes.count(rv.data[index]['text']):
                rv.liste_des_textes.remove(rv.data[index]['text'])
                if rv.liste_des_textes.count(rv.data[index]['text']) >= 1:
                    print("il faut retirer plus le text")
                if 'elem' in rv.data[index] and rv.data[index]['elem']:
                    print("il faut retirer le elem")
                    rv.liste_des_elem.remove(rv.data[index]['elem'])
        if rv.apply_callback:
            rv.apply_callback(rv.liste_des_textes, rv.liste_des_elem)

class ListeView(RecycleView,RecycleLayoutManagerBehavior):
    sl = ObjectProperty(None)

    def __init__(self, selections, has_multi, change_callback=None, **kwargs):
        if has_multi:
            self.multiselect = True
            self.touch_multiselect = True
        else:
            self.multiselect = False
            self.touch_multiselect = True #False
        super(ListeView, self).__init__(**kwargs)
        self.data = selections
        self.liste_des_textes = list()
        self.liste_des_elem = list()
        self.apply_callback = change_callback

    def refresh_from_data(self, *largs, **kwargs):
        #print("on me refraichit?!")
        super(RecycleView, self).refresh_from_data(*largs, **kwargs)
        self.data_has_changed=True
        #print("Done")

    def refresh_views(self, *largs):
        #print("on me refraichit la vue?!")
        super(RecycleView, self).refresh_views(*largs)
        self.sl.reselect_views()
        if self.data_has_changed == True:
            self.data_has_changed = False
        
    def setDataDict(self, selection):
        # On vide la liste des séléctions
        del self.liste_des_textes[:]
        del self.liste_des_elem[:]
        self.sl.unselect_views()
        self.data = selection

    def clear_selection(self):
        self.sl.clear_selected_views()

class ListeViewWithSearch(BoxLayout):
    def tri_par_text(self, textinput, text):
        dic = sorted([{'text': elem['text'], 'elem': elem['elem']}
                      for elem in self.dic
                      if text in elem['text'].lower()], key=lambda x: x['text'])
        self.liste_view.setDataDict(dic)

    def __init__(self, orientation, selections, has_multi, change_callback=None, **kwargs):
        self.dic = selections
        self.liste_view = ListeView(selections, has_multi, change_callback, **kwargs)
        ti = TextInput(size_hint=(1,.1), multiline=False)
        ti.bind(text=self.tri_par_text)
        super(ListeViewWithSearch, self).__init__(**kwargs)
        self.add_widget(ti)
        self.add_widget(self.liste_view)

class TestApp(App):
    def build(self):
        l = [{'text': cour.nom} for cour in formation_db.liste_cours_all()]
        return ListeView(l, True)

if __name__ == '__main__':
    TestApp().run()
