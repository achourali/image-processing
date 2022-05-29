import tkinter as tk
from tkinter import Menu, filedialog, Canvas, PhotoImage, NW


class GUI:
    root = tk.Tk()

    def __init__(self):
        self.root.title('Image processing')
        self.root.geometry("1000x500")
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar)

        file_menu.add_command(
            label='Open image',
            command=self.openImage
        )
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        self.root.mainloop()

    def openImage(self):
        filename = filedialog.askopenfilename(
            initialdir="./samples", title="Select a File")
        canvas = Canvas(self.root, width=1000, height=1000)
        canvas.grid(column=2, row=2)
        img = PhotoImage(file=filename)
        canvas.create_image(20, 20, anchor=NW, image=img)
        self.root.mainloop()
