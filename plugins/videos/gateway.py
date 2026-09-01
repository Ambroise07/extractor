from queue import Queue, Empty

#--------------------------------------------------------------------
# threadLock class

class ThreadLocker(Queue):

  def __init__(self, maxsize:int=0, **args):
    super().__init__(maxsize)

    # share data: notice that you can shared data
    # with method, but here I want use them
    # to share message (not dict) ...
    self.share_data = None
    

  def set_share_data(self, data:any):
    """
    share data, the data could be an python object
    or custom object. to share status (i.e : str)
    use set_status / get_status
    """
    self.share_data = data


  def get_share_data(self):
    """
    share data, the data could be an python object
    or custom object. to share status (i.e : str)
    use set_status / get_status
    """
    return self.share_data
    

  def get_status(self, **args):
    """ 
    return a string that give  audio apis status
    status can be "ready", "start", "process" "error" and "end"

    ----------------------------------------------------------
    ready: when audio api is ready to play
    start : when is start working
    process : when is working
    error : when is meet error
    end : when is finished his work. 
    sleep: this status is send by the ThreadLock 
             when audio api is not ready
             
    -----------------------------------------------------------

    """
     
    try:
      status = self.get(block=False)

      # add again the stop status send 
      # by the window to be receive as order 
      # by audio api
      if status.lower() == "stop":
        self.put("stop")
        status = "sleep"

    except Empty:
      status = "sleep"

       
    return status      


  def send_status(self, data:dict):
    """
    used by audio apis to send his status 
    to the window thread
    data hold the sender (a key) and the (status)
    this is allow this object to not send the status 
    of the window only of the audio api.
    
    """
    if data['sender'].lower() != 'receiver' :
      self.put(data['status']) 



  def stop_producer(self, **args):
    """
    when invocate this method send stop status
    to producer.
    
    """
    self.put('stop')


  def check_for_stop_order(self) -> bool:
    """
    Used ONLY by the audio API to check if Window requested a stop.
    Returns True if a 'stop' order is found.
    """
    try:
      order = self.get(block=False)

      if order.lower() == "stop":
        return True

      else:
        # Si ce n'est pas un stop, c'est un statut destiné à la fenêtre, 
        # on le remet immédiatement dans la file
        self.put(order)

    except Empty:
      pass

    return False

  

#----------------------------------------------------------------------

