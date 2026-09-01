# Message from author

Video player used to read the sound by  audio_api, an 
object of classe store at audio.py.
This handles high-quality video using tkvideoplayer.
This is only for reading MP4 files, but if you
want to use it inside a project, I left it free.

Of course, I don't speak English but I write it fine :)
Because it's the way developers communicate.

                              Gnabro Israel
                                          DATE: 29/08/2026

# Architecture

What if we use this architecture:
 1. A thread dedicated to decoding the audio stream.
 2. Another thread for Tkinter to handle our video player.
 3. A queue object, named ThreadLock, to ensure bidirectional communication.

    
# Scenario

The window initializes and displays an 'initialization' message.
The window thread reads the latest message stored in the ThreadLock to update the UI: it consumes the message and instantiates our player.

The secondary thread then takes over, letting our AudioHandler decode the audio stream and write a new message into the Bridge for the window, allowing the process to loop continuously.
