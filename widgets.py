from exceptions import *
from charsets import *
from threading import Thread

DEFAULT_FONTSIZE = 11


class Widget:
    def __init__(self, name, coords, widget_size):
        self.__widget_name = name
        self.__coords = coords
        self.__width = widget_size[0]
        self.__height = widget_size[1]
    
    def on_position(self, position):
        if (self.__coords[0] <= position[0] <= self.__coords[0] + self.__width) and \
                (self.__coords[1] <= position[1] <= self.__coords[1] + self.__height):
            return True
        return False
    
    def set_size(self, widget_size):
        self.__width = widget_size[0]
        self.__height = widget_size[1]
    
    def set_position(self, coords):
        self.__coords = coords
    
    def get_coords(self):
        return self.__coords
    
    def get_width(self):
        return self.__width
    
    def get_height(self):
        return self.__height


class Button(Widget):
    def __init__(self, name, button_text, coords, widget_size, left_function=None, left_arg_list=(),
                 right_function=None, right_arg_list=()):
    
        Widget.__init__(self, name, coords, widget_size)
        
        self.__button_text = button_text
        self.__left_function = left_function
        self.__right_function = right_function
        self.__leftargs = left_arg_list
        self.__rightargs = right_arg_list
        
        self.__hovering = False
        self.__pressed = 0
        self.__colours = {'NORMAL': (255, 255, 255), 
                          'LEFT': (150, 150, 150), 
                          'RIGHT': (150, 150, 150), 
                          'HOVER': (175, 175, 175), 
                          'TEXT': (0, 0, 0)}
        
        self.__fontsize = DEFAULT_FONTSIZE
        self.__animation_adjustment = {'TEXT': 1, 'BOX': 3}
        self.__function = Thread()
    
    def set_colour(self, state):
        different_settings = ['NORMAL', 'LEFT', 'RIGHT', 'HOVER', 'TEXT']
        
        for setting in state.keys():
            if setting not in different_settings:
                raise UnrecognisedStateException()
            self.__colours[setting] = state[setting]

    def set_fontsize(self, fontsize):
        self.__fontsize = fontsize

    def set_text(self, new_text):  
        self.__button_text = new_text
        
    def set_click_adjustment(self, state):
        for setting in state.keys():
            self.__animation_adjustment[setting] = state[setting]

    # Animation
    
    def draw_button(self, colour):
        coords_adjustment, textsize_adjustment = 0, 0

        if self.__pressed == 1 or self.__pressed == 2:
            coords_adjustment = self.__animation_adjustment['BOX']
            textsize_adjustment = -1 * self.__animation_adjustment['TEXT']

        fill(colour[0], colour[1], colour[2])
        rect(self.get_coords()[0]+coords_adjustment, self.get_coords()[1]+coords_adjustment,
             self.get_width()-(coords_adjustment*2), self.get_height()-(coords_adjustment*2))
        
        fill(self.__colours['TEXT'][0], self.__colours['TEXT'][1], self.__colours['TEXT'][2])
        textAlign(CENTER, CENTER)
        textSize(self.__fontsize+textsize_adjustment)
        text(self.__button_text, self.get_coords()[0], self.get_coords()[1], self.get_width(), self.get_height())

    def hover(self, position):
        self.__hovering = self.on_position(position)
    
    def animate(self):
        if self.__pressed == 1:
            self.draw_button(self.__colours['LEFT'])
        elif self.__pressed == 2:
            self.draw_button(self.__colours['RIGHT'])
        elif self.__hovering:
            self.draw_button(self.__colours['HOVER'])
        else:
            self.draw_button(self.__colours['NORMAL'])
    
    def activate_function(self, direction):
        if direction == LEFT:
            self.__pressed = 1
            self.call_left_function()
        elif direction == RIGHT:
            self.__pressed = 2
            self.call_right_function()
    
    def release_button(self):
        self.__pressed = 0

    def call_left_function(self):
        self.call_function(self.__left_function, self.__leftargs)

    def call_right_function(self):
        self.call_function(self.__right_function, self.__rightargs)

    def call_function(self, function, argument_list):
        if function is not None and not self.__function.is_alive():
            self.__function = Thread(target=function, args=argument_list)
            self.__function.start()
            self.__function.join()


class Label(Widget):
    def __init__(self, name, coords, widget_size, label_text):
        Widget.__init__(self, name, coords, widget_size)
        self.__label_text = label_text
        self.__fontsize = DEFAULT_FONTSIZE
        self.__box = False
        self.__colours = {'BOX': (255, 255, 255), 'TEXT': (50, 50, 50)}
    
    def animate(self):
        if self.__box:
            fill(self.__colours['BOX'][0], self.__colours['BOX'][1], self.__colours['BOX'][2])
            rect(self.get_coords()[0], self.get_coords()[1], self.get_width(), self.get_height())
            
        fill(self.__colours['TEXT'][0], self.__colours['TEXT'][1], self.__colours['TEXT'][2])
        textAlign(CENTER, CENTER)
        textSize(self.__fontsize)
        text(self.__label_text, self.get_coords()[0], self.get_coords()[1], self.get_width(), self.get_height())
    
    def set_text(self, new_text):
        self.__label_text = new_text
    
    def set_colour(self, state):
        different_settings = ['TEXT', 'BOX']
        
        for setting in state.keys():
            if setting not in different_settings:
                raise UnrecognisedStateException()
            
            self.__colours[setting] = state[setting]
    
    def set_box(self, state):
        self.__box = state
    
    def set_fontsize(self, fontsize):
        self.__fontsize = fontsize


class Entry(Widget):
    def __init__(self, name, coords, widget_size, length_limit=0, readonly=False, character_set=ALL_CHAR):
        Widget.__init__(self, name, coords, widget_size)

        self.__readonly = readonly
        self.__active = False
        self.__text = ""
        self.__fontsize = DEFAULT_FONTSIZE
        self.__charset = character_set
        self.__colours = {'TEXT': (0, 0, 0), 'BOX': (255, 255, 255)}
        self.__length_limit = length_limit
    
    def hover(self, position):
        if self.on_position(position):
            cursor(TEXT)
        else:
            cursor(ARROW)
    
    def activate_entry(self):
        self.__active = True
    
    def deactivate_entry(self):
        self.__active = False
    
    def get_text(self):
        return self.__text
    
    def set_text(self, new_text):
        self.__text = new_text
    
    def supply_data(self, key_code):
        
        if self.__active and not self.__readonly and key_code in self.__charset:
            self.__text += key_code
        elif self.__active and not self.__readonly:
            new_text = ""
            for character in range(len(self.__text)-1):
                new_text += self.__text[character]
            self.__text = new_text
        
        self.animate()

    def animate(self):
        fill(self.__colours['BOX'][0], self.__colours['BOX'][1], self.__colours['BOX'][2])
        rect(self.get_coords()[0], self.get_coords()[1], self.get_width(), self.get_height())
        
        textSize(self.__fontsize)
        fill(self.__colours['TEXT'][0], self.__colours['TEXT'][1], self.__colours['TEXT'][2])
        text(self.__text, self.get_coords()[0], self.get_coords()[1], self.get_width(), self.get_height())
    
    def set_colour(self, state):
        different_settings = ['TEXT', 'BOX']
        
        for setting in state.keys():
            if setting not in different_settings:
                raise UnrecognisedStateException()
            
            self.__colours[setting] = state[setting]
    
    def set_fontsize(self, fontsize):
        self.__fontsize = fontsize
    
    def set_charset(self, charset):
        self.__charset = charset
