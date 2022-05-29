from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image


class GUI:
    win=Tk()
    def __init__(self):
        self.win.geometry("1600x800")

        open_image = Button(self.win,
                                text="open image",
                                command=self.openImage)
        open_image.grid(column = 1, row = 1)
        mainloop()

    def openImage(self):
        filename = filedialog.askopenfilename(
            initialdir="./samples", title="Select a File")
        canvas = Canvas(self.win, width=1000, height=1000)
        canvas.grid(column=2,row=2)
        img = PhotoImage(file=filename)
        canvas.create_image(20, 20, anchor=NW, image=img)
        mainloop()
