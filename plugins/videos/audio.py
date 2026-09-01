"""
31/08/2026, Gnabro Israel.
Audio decoding backend with absolute isolation (Delegation + Callback).
"""
import av
import sounddevice as sd
import numpy as np
import threading
import time


class Decoder:
  """ 
  Responsible ONLY for opening a file, decoding it and streaming to sounddevice.
  It knows absolutely NOTHING about the locker.
  """
  
  def __init__(self, 
  stream_path: str, 
  check_stop_callback=None,
  error_callback=None
  ):
    self.stream_path = stream_path
    
    # 1. Open file and create the container
    container = av.open(self.stream_path)
    
    # 2. Retrieve the audio streams
    try:
        streams = container.streams.audio[0]

    # the raise statment will be remove later :)
    except IndexError:
        if error_callback:
          error_callback()
        raise ValueError("No audio track found in this file")

    # 3. Configure sounddevice
    samplerate = streams.rate
    channels = streams.channels

    # 4. Audio packet decoding and playback loop
    with sd.OutputStream(samplerate=samplerate, channels=channels, dtype='float32') as stream:
      
      for frame in container.decode(streams):
        
        # --- THE HACK: CALLING THE ANONYMOUS CALLBACK ---
        # The decoder runs this function without knowing it talks to the locker
        if check_stop_callback and check_stop_callback():
          break

        # Give processing time to the Tkinter Thread 
        time.sleep(0.001)
                     
        # Convert the frame into a numpy array
        array = frame.to_ndarray()
                
        # If stereo, remap channels for speakers layout
        if channels > 1:
          audio_data = np.ascontiguousarray(array.T)
        else:
          audio_data = array 
                   
        # Send data to sound driver
        stream.write(audio_data)



class AudioHandler:
  """ 
  Responsible for thread isolation, gateway communication
  and orchestration.This is the ONLY actor that handles the locker.

  """
  
  def __init__(self, locker: any):

    # the locker, audio_thread flag and the mp4_file
    self.locker = locker
    self.audio_thread = None
    self.mp4_file = None
        
    # Inform the window that the backend is ready and waiting
    self.locker.send_status({"sender": "AudioHandler", "status": "sleep"})



  def start_process(self):
    """ Triggered by the window once the path is shared in the locker """

    self.mp4_file = self.locker.get_share_data()
    
    if  self.mp4_file is None:
        self.locker.send_status({"sender": "AudioHandler", "status": "sleep"})


    if self.mp4_file:
      print('here the locker data is not None')
      
   

    # 3. Thread isolation: Delegate the decoder to a secondary thread
    self.audio_thread = threading.Thread(target=self._run_decoder,
                              args=(self.mp4_file,), daemon=True)
    self.audio_thread.start()
    
    # 2. Inform the window that the engine is ready, not start hack !:)
    self.locker.send_status({"sender": "AudioHandler", "status": "ready"})


  def _run_decoder(self, file_path: str):
    """ Secondary thread execution worker """
    try:
        # We give the decoder a direct reference to our locker method
        # but the decoder will only see it as a black-box function.
        self.locker.send_status({"sender": "AudioHandler", "status": "process"})
        Decoder(file_path, 
        check_stop_callback=self.locker.check_for_stop_order,
        error_callback=self.send_error_status)        
        self.locker.send_status({"sender": "AudioHandler", "status": "end"})

    except Exception:
        self.locker.send_status({"sender": "AudioHandler", "status": "error"})

  def send_error_status(self):
    """
    send error to ui used by the decoder

    """
    self.locker.send_status({"sender": "AudioHandler", "status": "error"})
    
