""""
display the progress bar

the root widget should have backend_bots
which is a queue object.

"""
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import Message, askokcancel
from tkinter.scrolledtext import ScrolledText

from collections.abc import Callable
from pathlib import Path

import logic 




class InputesUI(tkinter.Frame):

  def __init__(self, frame:tkinter.Frame | tkinter.Tk,  src_ext:list[str], dest_ext:list[str], **args):

    """Widget to Get files paths.
       the first input is for  the file source
       and the last for the destination one.
       
       src_ext: the format of the file source
       dest_ext: the format of the destination file

       frame should has src_file and dest_file attributes    

    Raises:
        TypeError: _description_
    """

    if not isinstance(frame, (tkinter.Frame,tkinter.Tk)):
      raise TypeError('the master of this widget should be tkinter.Frame')

    if not (isinstance(src_ext, list) and isinstance(dest_ext, list)):
          raise TypeError('the src_ext and dest_ext should be str.')

    self.src_ext, self.dest_ext = src_ext, dest_ext
    super().__init__(master=frame)

    # inputes data
    self.frame = frame
    self.src = tkinter.StringVar()
    self.src.set(' chemin du fichier .pdf ou .docx')

    self.dest = tkinter.StringVar()
    self.dest.set(' chemin du fichier .text')



    #-------------------------------------------------------------------------------------------------#
    # widget definitions
    #-------------------------------------------------------------------------------------------------#

    # source master 
    src_master = tkinter.Frame(master=self)
    src_master.pack(padx=('1c', 0), pady=('1c', 0), expand=True, fill="x")

    # source inpute
    self.src_input = tkinter.Entry(master=src_master, textvariable=self.src, width=30)
    self.src_input.pack(side="left")

    # source button
    src_button = tkinter.Button(master=src_master, text='choisir', command=self.choose_src)
    src_button.pack(side="right", padx=(0, '1c'))


    # destination master 
    dest_master = tkinter.Frame(master=self)
    dest_master.pack(padx=('1c', 0), pady=('1c', 0), expand=True, fill="x")
    
    # destination inpute
    self.dest_input = tkinter.Entry(master=dest_master, textvariable=self.dest, width=30)
    self.dest_input.pack(side="left")
    
    # destination button
    dest_button = tkinter.Button(master=dest_master, text='choisir', command=self.choose_dest)
    dest_button.pack(side="right", padx=(0, '1c'))

    self.pack(expand=True, fill="both")


  #--------------------------------------------------------------------------------------------------------------#
  # methods definitions 
  #--------------------------------------------------------------------------------------------------------------#

  def check_extension(self, file:str, ext:str):
    """
    check if file endwith ext 
    
    Args:
      file:str
      ext: str

    Return:
      Boolean

    """

    if not (isinstance(file, str) and isinstance(ext, str)):
      raise TypeError("file and ext should be strings") 

    return file.endswith(ext)


  def choose_src(self):
    """ open the files dialogue to choose a pdf or docx file

    Args:
        none

    Return:
        str | None

    """

    type = [('Fichier pdf ou docx', '*.pdf *.docx')] 
    file_path = filedialog.askopenfilename(title="selectionner le fichier source",
                                    filetypes=type)
    # check extension here
    ext = [ True for ext in self.src_ext
            if self.check_extension(file_path, ext) ]

    if not ext:
      self.frame.src_file = "fichier source au format incorrecte."
      return None

    self.src.set(f' {file_path}') 
    self.frame.src_file = file_path

    return file_path



  def choose_dest(self):
    """ open the files dialogue to choose a txt file
    
      Args:
          none
    
      Return:
          str | None
    
    """
    
    type = [('Fichier text', '*.txt')] 
    file_path = filedialog.askopenfilename(title="selectionner le fichier de destination",
                                        filetypes=type)


    # check extension here
    ext = [ True for ext in self.dest_ext
              if self.check_extension(file_path, ext) ]
    
    if not ext:
      self.frame.dest_file = "fichier de destination au format incorrecte."
      return None
    
    self.dest.set(f'{file_path}')
    self.frame.dest_file = file_path

    return file_path






#--------------------------------------------------------------------------------------------------------------#
# the ProgressUI class definition
#--------------------------------------------------------------------------------------------------------------#


class ProgressUI:

  def __init__(self, root:tkinter.Tk|tkinter.Frame):

    """Display a progress bar for show the extraction processing.

    Args:
        root: _the container this widget should be tkinter.Tk or tkinter.Frame_ 
        root::methods 
             process_steps : generator called when  for processing task. 
             cancel_task : callback called when task should be cancel.
             finish_task : called when task root.process_steps is done
    """


    # get root and ensure that it has the cancel and open_file method
    if not (hasattr(root, 'cancel_task') and hasattr(root, 'finish_task')):
      raise AttributeError("root should have a cancel_op and finish_op method")
    
    # check if process_steps is in good format
    if not (hasattr(root, 'perform_task') and isinstance(root.perform_task, Callable)):
      raise AttributeError("root should have an process steps generator") 
    
    # bindings self with its attributes
    self.root = root


    # main master the current task
    main_master = tkinter.Frame(master=root)
    main_master.pack(side="top", expand=True, fill="both", 
                    pady=("1c", "1c"), padx=('1c', '1c'))

    #title master
    title_master = tkinter.Frame(master=main_master)
    title_master.pack(fill="x")

    self.step_ui_info =  tkinter.StringVar()
    self.step_ui_info.set("Extration en cours...")

    # title label
    title_label = tkinter.Label(master=title_master, textvariable=self.step_ui_info)
    title_label.configure(font="Arial 16 bold")
    title_label.pack(side="left")

    #description master
    desc_master = tkinter.Frame(master=main_master)
    desc_master.pack(fill="x")

    #desc content
    desc_cont = tkinter.Label(master=desc_master, textvariable=root.status)
    desc_cont.pack(side="left")


    # progressbar master
    progressbar_master = tkinter.Frame(master=main_master)
    progressbar_master.pack(expand=True, fill="x")

    
    # progressbar
    progressbar = ttk.Progressbar(master=progressbar_master,
                                      mode="determinate",
                                      maximum=root.max_val)
    progressbar.pack(fill="x")


    # buttons master
    buttons_master = tkinter.Frame(master=main_master)
    buttons_master.pack(expand=True, fill="x")



    # open button
    self.cancel_or_open_button = tkinter.Button(master=buttons_master, 
                                      text="annuler", command=self.callback)
    self.cancel_or_open_button.pack(side="right")

    

    # set attribute of self
    self.progressbar = progressbar
    self.title_label = title_label
    self.main_master = main_master

    
    # run the execution of task
    self.execute_task()


    
  def callback(self):
    """
    cancel the oparation perfom by root.
    
    """
    # cancel the task 
    if self.cancel_or_open_button['text'] == 'annuler':
      self.root.cancel_task()
      return
    
    self.root.finish_task()
    


  def run_process(self):

    self.step_ui_info.set('Traitement en cours...')
    self.execute_task()


  def display_completed(self):
    """
    affiche "accomplit" dans la progressbar_master
    """
    self.step_ui_info.set("Opération terminée !")
    self.cancel_or_open_button.configure(text='ouvrire')
    self.cancel_or_open_button['command'] = self.root.finish_task
    self.root.update()

    
  def execute_task(self):
    """
    execute the oparation and update the 
    progressbar.
    in the case that op_step is none, the operation
    is permode by root.execute_op which should be an iterator.
    
    """
    
    if not self.root.perform_task:
      raise ValueError('the task perform callback is required')

    " task_performed start to zero, so i compare it to -1 to the if-statment"
    task_performed = self.root.perform_task()
    self.progressbar['value'] : int =  task_performed if task_performed is not None else 0

    "update the progressbar if task is uncompleted or remove it."
    if self.progressbar['value'] != self.root.max_val:
      self.root.after(300, self.execute_task)

    else:
      self.root.status.set("vous pouvez ouvrir le fichier.")
      self.display_completed()

  def destroy(self):
    self.main_master.destroy()
    


#---------------------------------------------------------------------------------------------------------------#
# the EXtractorapp class definition
#---------------------------------------------------------------------------------------------------------------#

class TextExtractor(tkinter.Frame):

  def __init__(self,  root:tkinter.Tk, **args):
    """_when text is being extracted, it's stored in a file call temp.txt 
        temp.txt path can be access in temp attribute._

    Args:
        root (tkinter.Tk): _description_
    """
    super().__init__(root)

    #-------------------------------------------------------------------------------------------------------#
    # class properties
    # ------------------------------------------------------------------------------------------------------#
    "this value is the size of the pdf or docx text to extract"
    "this property is update when the extractor is created, it value is give by the extractor"
    self._max_val = 100

    "these attributes is update by the inputui widget"
    self.src_file = None
    self.dest_file = None

    "the path of the temp file, this allow, the clean up, when cancel button is pressed"
    "whithout update the destination file"
    self.temp = Path(__file__).parent.resolve() / 'temp.txt'
    self.temp.touch(exist_ok=True)
      

    "this attribute value is give by the extractor "
    self._src_title = ''


    # input widget
    self.input = InputesUI(frame=self, src_ext=['.pdf', '.docx'], dest_ext=['.txt'])
        
        
    # submit button master
    self.separator = tkinter.Frame(master=self, background="#000")
    self.separator.pack(expand=True, fill='x', padx=('1c', '1c'))
            
    # submit button master
    submit_master = tkinter.Frame(master=self, padx=('1c', '1c'))
    submit_master.pack(expand=True, fill='x')
        
        
    # submit button
    self.submit_button = tkinter.Button(master=submit_master, text="valider", command=self.show_progressui)
    self.submit_button.pack(side='right', pady=(0, 0))
        
    # description master
    dest_master = tkinter.Frame(master=self)
    dest_master.pack(side="bottom", expand=True, fill='both')
    self.dest_master = dest_master
   

    # show app
    self.pack(side='top', expand=True, fill='both')

  #-------------------------------------------------------------------------------------------------------------#
  # properties setters, getters and deleters
  #-------------------------------------------------------------------------------------------------------------#

  @property
  def max_val(self):
    """_return the size of the source docs_
    """
    return self._max_val

  @max_val.setter
  def max_val(self, value):
    msg = """_can't update this field it readonly_"""
    raise PermissionError(msg)


  @max_val.deleter
  def max_val(self):
    msg = """_can't delete this field it readonly_"""
    raise PermissionError(msg)


  @property
  def src_title(self):
    """_return the size of the source docs_
    """
    return self._metadata

  @src_title.setter
  def src_title(self, value):
    msg = """_can't update this field it readonly_"""
    raise PermissionError(msg)


  @src_title.deleter
  def src_title(self):
    msg = """_can't delete this field it readonly_"""
    raise PermissionError(msg)



  #------------------------------------------------------------------------------------------------------------#
  # methods definitions
  #------------------------------------------------------------------------------------------------------------#

  def show_progressui(self, **args):
    """
    _display the progressui widget and it options_
    
    """
    # the logic instancies
    
    'the extractor apis should have async_extract_text wich return a generator'

    if not (self.src_file and self.dest_file ):
      Message(message='les données ne sont pas correctement fournies.').show()
      return 

    match self.src_file.endswith('.pdf'):
      case True:
        extractor = logic.PDFExtractor(src=self.src_file, 
                                           dest=self.temp, callback=self.perform_task)
        
        steps = extractor.async_extract_text()
        

      case False:
        extractor = logic.DOCXExtractor(src=self.src_file, 
                                                 dest=self.temp_file, callback=self.perform_task)
              
        steps = extractor.async_extract_text()

      case _:
        # display popup to show that this is issue into the software
        pass

    "this steps is called by self.perform_task to update the progressui"
    self.steps = steps 

    "set the maximun value of the progress bar"
    self._max_val = len(extractor.pages)

    # status of the progression
    self.status = tkinter.StringVar()
    self.status.set(f"extraction de texte dans 0 pages en cours...")

    # remove the input and the separator when a task is performing.
    self.input.destroy()
    self.separator.destroy()
    self.submit_button.destroy()
    
    # progressui 
    self.progressui = ProgressUI(self)



  def perform_task(self, *args):
    """_generator that process the extraction_
    """
    try:
      current_step = next(self.steps)
      self.status.set(f"extraction de texte à la page {current_step}.")
      return current_step

    except StopIteration:
      return self._max_val

    except Exception as e:
      self.progressui.destroy()
      self.undo()


  def finish_task(self, *args):
    """
    _called when extration is completed 
    this display the text widget, after his set text store in 
    self.cloud into self.dest file_

    """ 

    content: str = '' 
    with open(self.temp, 'r', encoding='utf-8', errors='ignore') as file:
      content = ''.join(file.readlines())

    with open(self.dest_file, 'w', encoding='utf-8', errors='ignore') as file:
      file.write(content)

    # clear the screen and add the scrolltext widget
    self.progressui.destroy()

    self.master.text_content = content
    self.master.create_text_widget()



  def cancel_task(self, *args):
    """
    _call when task is canceled display the cancel widget and remove all 
      text store self.cloud_

    """
    # call the backend to delete the task
    can_cancel = askokcancel(title="confirmation d'annulation", message="Voulez-vous annuler l'extraction en cours ?")
    
    if can_cancel:
      # this break the call of process
      self.steps = None


  def undo(self):
    """_set the input widget_
    """
    self.master.create_extraction_app()
    


class TextExtractorInterface(tkinter.Tk):

  def __init__(self, *args) -> None:
    super().__init__()


    # store text of the screen 
    self.text_content = ''

    # title
    self.title('Extracteurs - documents et youtube')
    
    #size
    self.geometry("800x650")

    # all widgets avaibles
    self.widgets = {
      'TextExtractor':self.create_extraction_app,
      'ScrolledText':ScrolledText,
    }

    # instantiate the extractionapp
    self.create_extraction_app()

    # show widget
    self.mainloop()



  def create_extraction_app(self):
    """_ display the extraction application_
    """
    # remove the text extractor widget
    key = [k for k in self.children.keys()]
    if len(key): self.children[key[0]].destroy()

    # show extractapp
    TextExtractor(self)
    


  def create_text_widget(self):
      """_ display the text widget_
      """

      # remove the text extractor widget
      key = [k for k in self.children.keys()]
      if len(key): self.children[key[0]].destroy()


      # show text widget
      if self.text_content:
        text_widget = ScrolledText(self, font='Arial 14')
        text_widget.insert('1.0', self.text_content)
        text_widget.pack(side='top', expand=True, fill='both', 
                       padx=('1c', '1c'), pady=('1c', '1c'))
        
        # close this window
        close_button = tkinter.Button(text="fermer", command=self.destroy)
        close_button.pack(side='bottom', padx=('2c', 0))


if __name__ =="__main__":
  app = TextExtractorInterface() 