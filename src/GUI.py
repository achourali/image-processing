import tkinter as tk
from tkinter import Menu, filedialog, Canvas, PhotoImage, NW,Label
from Image import Image


class GUI:
    root = tk.Tk()
    inputImage = Image()

    def __init__(self):
        self.root.title('Image processing')
        self.root.geometry("1000x800")
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar)

        file_menu.add_command(
            label='Open input',
            command=self.openInput
        )

        file_menu.add_command(
            label='Save output',
            command=self.saveOutput
        )
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        self.inputCanvas = Canvas(self.root, width=500, height=400)
        Label(self.inputCanvas, text="INPUT").grid(column=1,row=1)
        self.inputCanvas.grid(column=1,row=1)

        self.outputCanvas = Canvas(self.root, width=500, height=400)
        Label(self.outputCanvas, text="OUTPUT").grid(column=1,row=1)
        self.outputCanvas.grid(column=1,row=2)

        self.root.mainloop()

    def openInput(self):
        filename = filedialog.askopenfilename(
            initialdir="./samples", title="Select a File")
        self.inputImage.load_from_pgm(filename)
        img = PhotoImage(file=filename)
        canvas=Canvas(self.inputCanvas)
        canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.grid(column=1,row=2)
        self.root.mainloop()

    def saveOutput(self):
        return
