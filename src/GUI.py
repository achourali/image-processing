import tkinter as tk
from tkinter import Menu, filedialog, Canvas, PhotoImage, NW,Label,Text
from Image import Image
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GUI:
    root = tk.Tk()

    def __init__(self):
        self.root.title('Image processing')
        self.root.geometry("1700x800")
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
        Label(self.inputCanvas, text="INPUT").grid(column=1,row=1,sticky='w')
        self.inputCanvas.grid(column=1,row=1,sticky='w')
        self.inputInfo=Canvas(self.inputCanvas)
        

        self.outputCanvas = Canvas(self.root, width=500, height=400)
        Label(self.outputCanvas, text="OUTPUT").grid(column=1,row=1,sticky='w')
        self.outputCanvas.grid(column=1,row=2,sticky='w')
        self.outputInfo=Canvas(self.outputCanvas)

        self.root.mainloop()

    def openInput(self):
        filename = filedialog.askopenfilename(
            initialdir="./samples", title="Select a File")
        self.inputImage=Image()
        self.inputImage.load_from_pgm(filename)
        img = PhotoImage(file=filename)
        canvas=Canvas(self.inputCanvas)
        canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.grid(column=1,row=2,sticky='w')
        self.updateInfo('input')
        self.root.mainloop()
      
    
    def updateInfo(self,element):
        '''element is string can be 'input' or 'output'  '''
        if(element=='input'):
            canvas=self.inputCanvas
            image=self.inputImage
            infoCanvas=self.inputInfo
        elif(element=='output'):
            canvas=self.outputCanvas
            image=self.outputImage
            infoCanvas=self.outputInfo
        else:
            return

        infoCanvas.destroy()
        infoCanvas=Canvas(canvas)
        infoCanvas.grid(column=2,row=1,rowspan=2,sticky='n')
        Label(infoCanvas, text = f'height {image.height}').grid(column=1,row=1,sticky='w')
        Label(infoCanvas, text = f'width {image.width}').grid(column=1,row=2,sticky='w')
        Label(infoCanvas, text = f'average {image.average()}').grid(column=1,row=3,sticky='w')
        Label(infoCanvas, text = f'standard_deviation {image.standard_deviation()}').grid(column=1,row=4,sticky='w')
        data={
            'level':range(image.max_gray+1),
            'nb_pixels':image.histogram()
        }
        
        df = DataFrame(data,columns=['level','nb_pixels'])

        figure = plt.Figure(figsize=(5,4), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, infoCanvas)
        line.get_tk_widget().grid(column=2,row=1,rowspan=4,sticky='w')
        df = df[['level','nb_pixels']].groupby('level').sum()
        df.plot(kind='line', legend=True, ax=ax, color='r', fontsize=10)
        ax.set_title('histogram')
        
        data={
            'level':range(image.max_gray+1),
            'nb_pixels':image.cumulated_histogram()
        }
        
        df = DataFrame(data,columns=['level','nb_pixels'])

        figure = plt.Figure(figsize=(5,4), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, infoCanvas)
        line.get_tk_widget().grid(column=3,row=1,rowspan=4,sticky='w')
        df = df[['level','nb_pixels']].groupby('level').sum()
        df.plot(kind='line', legend=True, ax=ax, color='r', fontsize=10)
        ax.set_title('cummulated histogram')
          

    def saveOutput(self):
        return
