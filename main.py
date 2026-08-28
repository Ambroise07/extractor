 
"""
 
 2. MPP3Extractor  button
 3. YOUTUBEExtractor button (in next release)
 4. ABOUT button

"""

import tkinter
from plugins import *
from functools import partial

#---------------------------------------------------------------------------------------------------------------------#
# class Menu definition - 24/08/2026
#---------------------------------------------------------------------------------------------------------------------#

class Menu(tkinter.Frame):

  def __init__(self, app:tkinter.Tk | tkinter.Frame, **args):

    super().__init__(app)

    # app attribute
    self.app = app 
    self.selected_text_color = 'white'
    self.selected_bg_color = 'black' 
    
    self.not_selected_text_color = 'black'
    self.not_selected_bg_color = self.master['bg']
    
    # title of the widget
    title_master = tkinter.Frame(self)
    title_master.pack(side="top",fill='x')

    title_label = tkinter.Label(master=title_master, text="Menu", font='Ubuntu 18 bold')
    title_label.pack(side='left', padx=('.01c', 0))

    # items
    items_names : list = ['texte', 'sons', 'vidoes']
    self.items: list = []

    items_master = tkinter.Frame(self)
    items_master.pack(expand=True, fill="both", side="bottom")


    for name in items_names:
      item = tkinter.Button(master=items_master, text=name, font='Ubuntu 13 normal')
      item.pack(expand=True, fill='x')
      item.config(command= partial(self.item_callback, name))
      item['bd'] = 2
      item['width'] = 10
      item['relief'] = 'solid'
      self.items.append(item)



  def item_callback(self, item_name:str):
    """_call when item with name ITEM_NAME is clicked._

    Args:
        item_name (str): _the text of the button clicked._
    """
    # first put the item selected in it color 
    # then add the screen of the selected item
    self.set_selected_item(item_name)
    self.app.set_screen(item_name)



  def set_selected_item(self, item_name):
    """_set in black the selected item_

    Args:
        item_name (_str_): _the name of the item selected_
    """
    item_selected: list = [item for item in self.items if item['text'] == item_name]
    item_not_selected: list = [item for item in self.items if item['bg'] == 'black']

    if len(item_selected):
      item = item_selected[0]
      item['fg'] = self.selected_text_color
      item['bg'] = self.selected_bg_color 


    if len(item_not_selected):
      item = item_not_selected[0]
      item['fg'] = self.not_selected_text_color
      item['bg'] = self.not_selected_bg_color 


#-------------------------------------------------------------------------------------------------------------#
# class Main definition - 24/08/2026
#-------------------------------------------------------------------------------------------------------------#

class Main(tkinter.Frame):

  def __init__(self, app:tkinter.Tk | tkinter.Frame, **args):
    super().__init__(app)


  def update(self, screen:tkinter.Frame) -> None:
    """_replace all widgets inside this by the SCREEN widget, the widget SCREEN manage itself it position._

    Args:
        screen (tkinter.Frame): _the widget which will be used to replace the old_

    Raises:
        TypeError: _if screen is not an instance of tkinter.Frame_
    """
     
    current_screen = [ screen for screen in self.children.values() ]
    
    if len(current_screen): current_screen.pop().destroy()

    screen_instance = screen(self)
    self.master.update() 





#-----------------------------------------------------------------------------------------------------------#
# Application class definition - 23/08/2026
#-----------------------------------------------------------------------------------------------------------#

class Application(tkinter.Tk):
  
  """ 
  this class will be used in the next version of 
  the software.

  """

  def __init__(self, **args):

    """
    _:TODO when display the menu, the window 
    should be center on the screen. --ok _
      
    """
    super().__init__()

    self.title('Extracteur - Document & media')

    " size of the user screen"
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    "offset - use to compute the value of the window size."
    offset = (screen_height // 4)

    "the avaible screens"
    self.screens = {
      'texte': TextExtractorInterface,
      'sons':None,
      'youtube':None,
      'about':None
    }

    width, height = 300, 300

    # center the window on the screen (later) done
    x =  int((abs( screen_width - width )) / 2)
    y =  int((abs( screen_height - height )) / 2)
    self.geometry(f'{width}x{height}+{x}+{y}')

    "main widget"
    menu = Menu(self)
    menu.pack(side="left", expand=True, fill="y", pady=('1c', 0), padx=('1c', 0)) 


    #mainloop
    self.mainloop()


  def set_screen(self, screen_name:str):
    """_set the new screen_

    Args:
        screen_name (str): _the name of the new screen_
    """
    screen : tkinter.Frame | None = self.screens.get(screen_name.lower(), None) 

    if screen is not None:
      self.show_screen(screen)
      return 

    raise TypeError('Screen should be an instance of tkinter.Frame')


  def show_screen(self, screen:tkinter.Frame):
    """ show the widget toplevel with the content name screen """
    #print('screen passe: ', repr(screen))
    master = tkinter.Toplevel(self)
    master.geometry("800x650")
    screen_instance  = screen(master)
    
    master.mainloop()  
    


if __name__ =='__main__':
    Application()
