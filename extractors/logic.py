"""
here the core functionnality of this framework.

"""


#-------------------------------------------------------------------------#
# text extractor of pdf 
# pdf extractor .
# the extractor use pypdf module.
# pip install pypdf
#-------------------------------------------------------------------------#


from pypdf import  PdfReader
from pathlib import Path
from collections.abc import Callable


class PDFExtractor(PdfReader):

   #-----------------------------------------------------------------------#
   # readonly and privates attributes
   #-----------------------------------------------------------------------# 

   # the name of this core functionality
   _core = "pdf-extractor" 
   
   # the version, so this extractor class may be update
   # it help the user to target this release for instance.
   _version = "1.0.1"
   
   # the developpeur
   _author = "gnabro israel"
   
   # message error prints when Permission Error is raised
   # these attributes are privated.
   __setter_error_msg = "can't be update this is a readonly attribute"
   __deleter_error_msg = "can't delete this is attribute"
   
  
   def __init__(self, src, dest:str, callback, 
               page_number:int=-1,  **args):
    """
    src should be an open file in 'rb' mode (read binary)
    if the destination file isn't exists, it will be creaded.
    
    """
    # ensure that source and dest files exist
    if not (Path(dest).exists() and Path(src).exists()):
      raise ValueError("The file doesn't exist.")

    """
    if not hasattr(src, 'write'):
      raise TypeError('soruce file should be open with the open building function')
    """
      
    # ensure that 'callback' is a function
    if not isinstance(callback, Callable):
      raise TypeError("Callback should be a function or a method")

    # check for page_number
    if not isinstance(page_number, int):
      raise TypeError(f'page_number argument should be int')


    # binds the attributes to self
    self.src = src
    self.dest = dest 
    self.callback = callback
    self.page_number = page_number if page_number >= 0 else None

    
    super(PDFExtractor, self).__init__(src)
        

  #-----------------------------------------------------------------------#
  # methods of the readonly and private attributes
  #-----------------------------------------------------------------------#

   @property
   def core(self):
    """ return the name of this stage """
    return self._stage

   @core.setter
   def core(self, value):
    """ can't update this is readonly attribute """
    raise PermissionError(self.__setter_error_msg) 

   @core.deleter
   def core(self, value):
      """ can't update this is readonly attribute """
      raise PermissionError(self.__deleter_error_msg)


   @property
   def version(self):
      """ return the version of this instance """
      return self._version
  
   @version.setter
   def version(self, value):
      """ can't update this is readonly attribute """
      raise PermissionError(self.__setter_error_msg) 
  
   @version.deleter
   def version(self, value):
      """ can't update this is readonly attribute """
      raise PermissionError(self.__deleter_error_msg)

   @property
   def author(self):
      """ the author of this release """
      return self._author
  
   @author.setter
   def author(self, value):
      """ can't update this is readonly attribute """
      raise PermissionError(self.__setter_error_msg) 
  
   @author.deleter
   def author(self, value):
      """ can't update this is readonly attribute """
      raise PermissionError(self.__deleter_error_msg)


  #------------------------------------------------------------------------#
  # method definitions
  #------------------------------------------------------------------------#

   def extract_text(self):
    """
    method to call for extracting text.
    if all is set to True, this will extract all text
    otherwise it wil extract only the text of the page
    self.text_page

    Warning: this method will remove all the content 
    of the destination file.
    
    """
    # extract text of single page
    if self.page_number:
      # the page variable is a dictionary so we can 
      # count the items using len building function
      page = self.pages[self.page_number]
      
      
      with open(self.dest, "w",  encoding="utf-8") as dest:
        dest.write(page.extract_text())
        self.callback(self.page_number)
      return 


    # extract text of all  pages
    with open(self.dest, "w",  encoding="utf-8") as dest:
      for n, page in enumerate(self.pages):
        dest.write(page.extract_text(extraction_mode='layout'))
        self.callback(n)


   def async_extract_text(self):
      """
      method to call for extracting text.
      if all is set to True, this will extract all text
      otherwise it wil extract only the text of the page
      self.text_page
  
      Warning: this method will remove all the content 
      of the destination file.
      
      """
      # extract text of all  pages
      with open(self.dest, "w",  encoding="utf-8") as dest:
        for n, page in enumerate(self.pages):
          try:
            text = page.extract_text(extraction_mode="layout")
            
            if text:
              dest.write(text)

          except Exception as e:
            #:TODO use an otherlibrairy to extract the text of this page
            # the continue
            continue 
          
          yield n 
    


#-------------------------------------------------------------------------#
# docx extractor.
# the extractor use python-docx module.
# pip install python-docx 
#-------------------------------------------------------------------------#


from docx import Document
from pathlib import Path
from collections.abc import Callable


class DOCXExtractor:

   #-----------------------------------------------------------------------#
   # readonly and privates attributes
   #-----------------------------------------------------------------------# 

   # the name of this core functionality
   _core = "docx-extractor" 
   
   # the version, so this extractor class may be update
   # it help the user to target this release for instance.
   _version = "1.0.0"
   
   # the developpeur
   _author = "gnabro israel"
   
   # message error prints when Permission Error is raised
   # these attributes are privated.
   __setter_error_msg = "can't be update this is a readonly attribute"
   __deleter_error_msg = "can't delete this is attribute"

   def __init__(self, src:str, dest:str, callback,  **args):

    # ensure that source and dest files exist
    base_dir = Path('.').parent.resolve()
    src = base_dir / src
    dest = base_dir / dest
    
    if not (src.exists() and dest.exists()):
      raise ValueError("The file doesn't exist.")

    # ensure that 'callback' is a function
    if not isinstance(callback, Callable):
      raise TypeError("Callback should be a function or a method")

    # check for page_number
    #if not isinstance(page_number, int):
    #  raise TypeError(f'page_number argument should be int')


    # binds the attributes to self
    self.src = src
    self.dest = dest 
    self.callback = callback
    #self.page_number = page_number if page_number > 0 else None

    
    #super().__init__(self, src)
        


  #------------------------------------------------------------------------#
  # method definitions
  #------------------------------------------------------------------------#


   def extract_text(self):
    """
    method to call for extracting text.
    if all is set to True, this will extract all text
    otherwise it wil extract only the text of the page
    self.text_page

    Warning: this method will remove all the content 
    of the destination file.
    
    this code will be added into the body of this method
    later.
    
    if self.page_number:
      # the page variable is a dictionary so we can 
      # count the items using len building function
      page = self.pages[self.page_number]
      self.callback(len(page))
      
      return page.extract_text()
    now can't extract text of a single page.
    
    """
    #:TODO allow the extraction of text into single page.
    
    with open(self.dest, "w", encoding="utf-8") as dest:
      paragraphs = Document(self.src).paragraphs
      
      for n, paragraph in enumerate(paragraphs):
        dest.write(paragraph.text)
        self.callback(n)
