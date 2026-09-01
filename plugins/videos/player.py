from tkinter import Frame, Tk
from tkVideoPlayer import  TkinterVideo
from utils import StreamsHandler

#-----------------------------------------------------------------------
# mp4player and Controls class



class MP4Player(TkinterVideo, StreamsHandler):


  def __init__(self, mp4_file_path:str,
               master:Frame |Tk, 
               **args):
    """
    intilise this class: check if mp4_file_path is 
    pointing to a mp4 file.

    get the file and create an instance of  tkvideoplayer
    which will be used as api to handle video.    

    """

    TkinterVideo.__init__(
      self,
      master=master,
      scaled=True,
      consistant_frame_rate=True,
      keep_aspect=True

    )
    
    StreamsHandler.__init__(self, stream=mp4_file_path)


    # load files and get attribute
    self.mp4_file_path = mp4_file_path
    self.load(rf'{mp4_file_path}')
    
    
  def process_stream(self):
    """ play the video """

    # call then play
    self.play()

    
  def show(self):
    self.pack(side="top", expand=True, fill="both")
    self.run_process_stream()

    
  def stop_process(self):
    """ stop playing the video """
    self.pause()


  def cancel_process(self):
    """ cancel player and close window """
    self.stop()

    
  def resum_process(self):
    self.play()


class Controls(Frame):
  """
  Because you can use the instance 
  of this class or the instance MP4Player,
  this class is provide to separate the controls
  widgets to the screen.
                                 Gnabro Israel
  """

  def __init__(self, player:MP4Player, **args):

    super().__init__()
    pass


#-----------------------------------------------------------------------
