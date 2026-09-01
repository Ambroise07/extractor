"""
utils fonctions and class.
31/08/2026, gnabro israel.

"""
from abc import ABC, abstractmethod

class StreamsHandler(ABC):
  """
  define base class for its children.

  first a StreamsHandler subclass should has:

   - process_streams: which perform task on stream
                      task can be *read* the stream,
                      *write* in it and so on.

   - stop_process: call when process_streams should be stopped.
                   note, this is only call WHEN process_streams
                   is executed.
                   it raised an PermissionError when process_streams
                   when is not call.

   - cancel_process: call when process_streams or stop_process 
                      is executed.

   - resum_process : call process_streams when stop_process is being 
                     executed.

   notice These methods communicate using the values of the STATE flag, 
   which draws its values from the STATES tuple. 
  """

  """ avaibles values of the state flag """
  STATES = ['on_process', 'on_stop', 'on_cancel']
  
  def __init__(self, stream: any, **args):

    # current state 
    self.STATE = self.STATES[0]


  @abstractmethod
  def process_stream(self):
    """ implemented by other class """
    pass

  
  def run_process_stream(self):
    """ perform task on stream """
    if not  self.STATE == self.STATES[0]:
      raise PermissionError('cannot process the streams')

    self.process_stream() 


  @abstractmethod
  def stop_process(self):
    """ implemented by other class """
    pass

    
  def stop_executor(self):
    """ perform task on stream """
    if self.STATE in self.STATES[1:]:
      raise PermissionError('cannot stop again the streams')
  
    self.stop_process()


  @abstractmethod
  def cancel_process(self):
    """ implemented by other class """
    pass
     
  def cancel_executor(self):
    """ perform task on stream """

    # cancel task only on two states: stopped or processing
    if self.STATE in self.STATES[:1]:
      self.cancel_process() 

  @abstractmethod
  def resum_process(self):
    """ implemented by other class """
    pass

     
  def resum_executor(self):
    """call again process_stream """

    # cancel task only on two states: stopped or processing
    if not self.STATE == self.STATES[1]:
      raise PermissionError(
      """cannot resum process it on_process or  on_cancel mode """
      )

    self.resum_process()

