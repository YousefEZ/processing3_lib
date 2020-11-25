from containers import container
from colours import *

def random_function(number):
    global root
    global argument 
    
    argument[0] = number+1
    root.setting('entry_1', TEXT=str(number))

def setup():
    global root
    global argument

    size(800, 800)
    root = container(800, 800)
    root.setting('WINDOW', BACKGROUND_COLOUR=SILVER)
    
    argument = [2]
    
    button1_coords = (50,50)
    button1_size = (125, 25)
    
    root.add_button('button_1', 'Hello World',  button1_coords ,  button1_size, random_function, argument, random_function, [52])
    root.add_button('button_2', '^', (25,25), (20, 20))
    root.add_label('label_1', 'HELLO', (300,300), (100, 100))
    
    Readonly = True
    root.add_entry('entry_1', (400,200), (125, 25), Readonly)
    
    root.setting('label_1', BOX=True, COLOUR={'TEXT':YELLOW, 'BOX':BLACK}, FONT_SIZE=20)
    root.setting('button_1', COLOUR={'NORMAL':WHITE, 'TEXT': PURPLE}, CLICK={'BOX':3, 'TEXT':1})
    root.setting('button_1', POSITION=(1,1))
    
    argument[0] = 3
    
    root.display() # use root.withdraw() to remove all elements.
    
    
def draw():
    global root
    
    root.check_mouse((mouseX,mouseY))
    #root.refresh_window()
    
def mousePressed():
    global root
    root.press_window(mouseButton, (mouseX, mouseY))

def mouseReleased():
    global root
    root.release_window()

def keyTyped():
    global root
    root.enter_key(key)
