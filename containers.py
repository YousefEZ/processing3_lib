from exceptions import *
from widgets import *
from colours import *


class Container:
    def __init__(self, container_width, container_height):
        self.__buttons = {}
        self.__labels = {}
        self.__entries = {}
        self.__width = container_width
        self.__height = container_height
        self.__background_colour = SILVER
        self.__display = False
    
    def display(self):
        self.__display = True
        self.refresh_window()
    
    def withdraw(self):
        self.release_window()
        self.deactivate_widgets()
        self.__display = False
        self.refresh_window()
    
    def check_mouse(self, position):
        if not self.__display:
            return
        
        for button_key in self.__buttons.keys():
            self.__buttons[button_key].hover(position)
        for entry_key in self.__entries.keys():
            self.__entries[entry_key].hover(position)
        
        self.refresh_window()
    
    def refresh_window(self):
        
        clear()
        background(self.__background_colour[0],self.__background_colour[1],self.__background_colour[2])
        
        if not self.__display:
            return
        
        for button_key in self.__buttons.keys():
            self.__buttons[button_key].animate()
        for label_key in self.__labels.keys():
            self.__labels[label_key].animate()
        for entry_key in self.__entries.keys():
            self.__entries[entry_key].animate()
    
    def widget_key_taken(self, key_name):
        if key_name == "WINDOW" or key_name in self.__buttons.keys() or key_name in self.__labels.keys() or \
                key_name in self.__entries.keys():

            return True
        return False
    
    def activate_widget(self, key_name):
        if key_name not in self.__entries.keys():
            raise WidgetNonExistentException()
        
        self.deactivate_widgets()
        self.__entries[key_name].activate_entry()
    
    def deactivate_widgets(self):
        for entry in self.__entries.keys():
            self.__entries[entry].deactivate_entry()

    def press_window(self, direction, mouse_position):
        for button in self.__buttons.keys():
            if self.__buttons[button].on_position(mouse_position):
                self.__buttons[button].activate_function(direction)
        
        for entry in self.__entries.keys():
            if self.__entries[entry].on_position(mouse_position):
                self.activate_widget(entry)
        
        self.refresh_window()
    
    def release_window(self):
        
        for button in self.__buttons.keys():
            self.__buttons[button].release_button()
        self.refresh_window()
    
    def enter_key(self, key_code):
        if not self.__display:
            return
        
        for entry in self.__entries.keys():
            self.__entries[entry].supply_data(key_code)
    
    def add_button(self, widget_key, button_text, coords, widget_size,
                   left_function=None, left_args=(), right_function=None, right_args=()):

        if self.widget_key_taken(widget_key):
            raise WidgetNameTakenException()
        
        self.__buttons[widget_key] = Button(widget_key, button_text, coords, widget_size,
                                            left_function, left_args, right_function, right_args)
    
    def add_label(self, widget_key, label_text, coords, widget_size):
        if self.widget_key_taken(widget_key):
            raise WidgetNameTakenException()
        
        self.__labels[widget_key] = Label(widget_key, coords, widget_size, label_text)
    
    def add_entry(self, widget_key, coords, widget_size, readonly=False, length_limit=0):
        if self.widget_key_taken(widget_key):
            raise WidgetNameTakenException()
        
        self.__entries[widget_key] = Entry(widget_key, coords, widget_size, length_limit, readonly)

    def setting(self, widget_key, **kwargs):
        if widget_key == "WINDOW":
            self.window_set_setting(kwargs)
        elif widget_key in self.__buttons.keys():
            self.button_set_settings(widget_key, kwargs)
        elif widget_key in self.__labels.keys():
            self.label_set_settings(widget_key, kwargs)
        elif widget_key in self.__entries.keys():
            self.entry_set_settings(widget_key, kwargs)
        else:
            raise WidgetNonExistentException()
        
        if self.__display:
            self.refresh_window()
    
    def window_set_setting(self, setting):
        different_settings = ['BACKGROUND_COLOUR']
        
        for setting_key in setting.keys():
            if setting_key not in different_settings:
                raise UnrecognisedStateException()
        
        if "BACKGROUND_COLOUR" in setting.keys():
            self.__background_colour = setting["BACKGROUND_COLOUR"]

    def button_set_settings(self, widget_key, setting):

        different_settings = ['COLOUR', 'SIZE', 'CLICK', 'FONT_SIZE', 'POSITION', 'TEXT']
        
        for setting_key in setting.keys():
            if setting_key not in different_settings:
                raise UnrecognisedStateException()

        if "SIZE" in setting.keys():
            self.__buttons[widget_key].set_size(setting["SIZE"])
        
        if "FONT_SIZE" in setting.keys():
            self.__buttons[widget_key].set_fontsize(setting["FONT_SIZE"])
        
        if "POSITION" in setting.keys():
            self.__buttons[widget_key].set_position(setting["POSITION"])
        
        if "TEXT" in setting.keys():
            self.__buttons[widget_key].set_text(setting["TEXT"])
        
        if "COLOUR" in setting.keys():
            self.__buttons[widget_key].set_colour(setting["COLOUR"])
        
        if "CLICK" in setting.keys():
            self.__buttons[widget_key].set_click_adjustment(setting["CLICK"])
    
    def label_set_settings(self, widget_key, setting):
        different_settings = ['COLOUR', 'SIZE', 'BOX', 'FONT_SIZE', 'POSITION', 'TEXT']
        
        for setting_key in setting.keys():
            if setting_key not in different_settings:
                raise UnrecognisedStateException()
        
        if "SIZE" in setting.keys():
            self.__labels[widget_key].set_size(setting["SIZE"])
        
        if "FONT_SIZE" in setting.keys():
            self.__labels[widget_key].set_fontsize(setting["FONT_SIZE"])
        
        if "POSITION" in setting.keys():
            self.__labels[widget_key].set_position(setting["POSITION"])
        
        if "TEXT" in setting.keys():
            self.__labels[widget_key].set_text(setting["TEXT"])
        
        if "COLOUR" in setting.keys():
            self.__labels[widget_key].set_colour(setting["COLOUR"])
        
        if "BOX" in setting.keys():
            self.__labels[widget_key].set_box(setting["BOX"])
    
    def entry_set_settings(self, widget_key, setting):
        different_settings = ['TEXT', 'COLOUR', 'SIZE', 'FONT_SIZE', 'POSITION']
        
        for setting_key in setting.keys():
            if setting_key not in different_settings:
                raise UnrecognisedStateException()
        
        if "SIZE" in setting.keys():
            self.__entries[widget_key].set_size(setting["SIZE"])
            
        if "TEXT" in setting.keys():
            self.__entries[widget_key].set_text(setting["TEXT"])
        
        if "FONT_SIZE" in setting.keys():
            self.__entries[widget_key].set_fontsize(setting["FONT_SIZE"])
        
        if "POSITION" in setting.keys():
            self.__entries[widget_key].set_position(setting["POSITION"])
        
        if "COLOUR" in setting.keys():
            self.__entries[widget_key].set_colour(setting["COLOUR"])
