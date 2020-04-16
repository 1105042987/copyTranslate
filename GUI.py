from tkinter import Frame,Label
class Application(Frame):
  def __init__(self, text, master=None, *args, **kwargs):
    Frame.__init__(self,master, *args, **kwargs)
    self.grid()
    self.master.title('Translate')
    self.t = text
    self.createWidgets()

  def createWidgets(self):
    self.text = Label(self, text=self.t, bg='white', width = 40, wraplength = 240, justify = 'left')
    self.text.pack()


def show(text):
  app = Application(text)
  app.mainloop()

if __name__ == "__main__":
    app = Application(('你好！'*22+'\n')*10)
    app.mainloop()