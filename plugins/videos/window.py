
#----------------------------------------------------------------------
# Window class 
from tkinter import Tk, StringVar
from player import MP4Player
from queue import Queue

class Window(Tk):

  def __init__(self, 
                thread_lock:Queue,
                audio_api, 
                video_file,
              **args):

    super().__init__()
    self.title('streams ')
    self.geometry('3000x3000')

    
    if not isinstance(thread_lock, Queue):
      raise TypeError("""
      thread_lock parameter should be an instance of queue.Queue
      """)

    if not isinstance(video_file, str):
      raise TypeError(f"""
            video_file parameter should be string
            not {type(video_file)}
            
            """)
    #--------------------------------------------------------------
    # three actors: self, thread_lock and player for this class
    #-------------------------------------------------------------- 

    # the thread_lock, audio_api and the video_file
    self.thread_lock = thread_lock
    self.video_file = video_file
    self.audio_api = audio_api
    
    # tkinter variables
    self.status = StringVar()
    self.status.set('lecteur audio inactif')

    # the player 
    self.player = MP4Player(
    master=self,
    mp4_file_path=video_file, 
    )
    


  def start(self, **args):
    """
    handle communication between this and 
    the thread_lock object wich is mainly 
    the backend gateway.
    
    """
    self.after(30, self.process_response)
    
    #self.player.pack(expand=True, fill="both")

    self.mainloop()
    



  def process_response(self, **args):
    """
    handling response receive from the 
    thread_lock.
    
    """
    self.after(3000, self.process_response)

    status = self.thread_lock.get_status()
    match status.upper():

      case "STOP":
        return 
        
      case "READY":
        print('ready display !')
        self.player.show()
        
      case "SLEEP":
        self.thread_lock.set_share_data(self.video_file)
        print('windows side : the video file is send')

        self.thread_lock.send_status({"sender": "receiver", "status": "start"})
        
        self.audio_api.start_process()
                
        self.status.set('lecteur audio inactif.')


      case "PROCESS":
        self.status.set('Lecteur audio en cours de traitement...')
        
      case "START":
        self.status.set('Quelques secondes...')

      case "ERROR":
        self.status.set("Une erreur est survenu, veuillez redemarer l'application")

      #:TODO update later
      case "END":
        self.player.destroy()

      case _:
        self.thread_locker.send_status(status)
        

#-------------------------------------------------------------------------

