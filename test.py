def op_steps():
    """
    op_steps is a generator.
    
    """
    
    global root
    for i in range(200):
      yield i
    
def cancel_op(*args):
   print('oparation is canceled')


def finish_op(*args):
   print('oparation is end with success')


  root = tkinter.Tk()

  # set callbacks and desc_cont
  root.cancel_op = cancel_op
  root.finish_op = finish_op
  root.desc_cont = "a book about programming"
  root.max_val = 200
  root.op_steps = op_steps()  

  # create widget
  progress_ui = ProgressUI(root=root)

  root.after(3000, op_steps)
  root.mainloop()
""" 