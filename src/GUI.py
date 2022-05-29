import tkinter as tk
from tkinter import Menu, filedialog, Canvas, PhotoImage, NW, Label, Text, Entry, simpledialog
from Image import Image
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class GUI:
    root = tk.Tk()

    def __init__(self):
        self.root.title('Image processing')
        self.root.geometry("1700x850")
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

        operations_menu = Menu(menubar)

        operations_menu.add_command(
            label='histogram equalizer',
            command=self.histogram_equalizer
        )
        operations_menu.add_command(
            label='saturation transformation',
            command=self.saturation_transformation
        )

        operations_menu.add_command(
            label='generate salt & pepper noise',
            command=self.generate_random_noise
        )

        operations_menu.add_command(
            label='median filter',
            command=self.median_filter
        )

        operations_menu.add_command(
            label='average filter',
            command=self.average_filter
        )
        operations_menu.add_command(
            label='binarize ',
            command=self.binarize
        )
        menubar.add_cascade(
            label="Operations",
            menu=operations_menu
        )

        self.initInputCanvas()

        self.initOutputCanvas()
        self.root.mainloop()

    def initInputCanvas(self):

        self.inputCanvas = Canvas(self.root, width=500, height=400)
        Label(self.inputCanvas, text="INPUT").grid(column=1, row=1, sticky='w')
        self.inputCanvas.grid(column=1, row=1, sticky='w')
        self.inputInfo = Canvas(self.inputCanvas)

    def initOutputCanvas(self):

        self.outputCanvas = Canvas(self.root, width=500, height=400)
        Label(self.outputCanvas, text="OUTPUT").grid(
            column=1, row=1, sticky='w')
        self.outputCanvas.grid(column=1, row=2, sticky='w')
        self.outputInfo = Canvas(self.outputCanvas)

    def openInput(self):
        filename = filedialog.askopenfilename(
            initialdir="./samples", title="Select a File")
        self.inputImage = Image()
        self.inputImage.load_from_pgm(filename)
        self.inputCanvas.destroy()
        self.initInputCanvas()
        self.outputCanvas.destroy()
        self.initOutputCanvas()
        fig = plt.Figure(figsize=(4, 4), dpi=96)
        ax = fig.add_subplot(111)
        ax.imshow(self.inputImage.matrix, cmap='gray')
        ax.axis('off')
        canvas = FigureCanvasTkAgg(fig, self.inputCanvas)
        canvas.get_tk_widget().grid(column=1, row=2, sticky='w')
        canvas.draw()

        self.updateInfo('input')
        self.root.mainloop()

    def updateInfo(self, element):
        '''element is string can be 'input' or 'output'  '''
        if(element == 'input'):
            canvas = self.inputCanvas
            image = self.inputImage
            infoCanvas = self.inputInfo
        elif(element == 'output'):
            canvas = self.outputCanvas
            image = self.outputImage
            infoCanvas = self.outputInfo
        else:
            return

        infoCanvas.destroy()
        infoCanvas = Canvas(canvas)
        infoCanvas.grid(column=2, row=1, rowspan=2, sticky='n')
        Label(infoCanvas, text=f'height {image.height}').grid(
            column=1, row=1, sticky='w')
        Label(infoCanvas, text=f'width {image.width}').grid(
            column=1, row=2, sticky='w')
        Label(infoCanvas, text=f'average {image.average()}').grid(
            column=1, row=3, sticky='w')
        Label(infoCanvas, text=f'standard_deviation {image.standard_deviation()}').grid(
            column=1, row=4, sticky='w')
        if(element == "output"):
            Label(infoCanvas, text=f'signal to noise ratio {Image.signal_to_noise_ratio(self.inputImage,self.outputImage)}').grid(
                column=1, row=5, sticky='w')

        data = {
            'level': range(image.max_gray+1),
            'nb_pixels': image.histogram()
        }

        df = DataFrame(data, columns=['level', 'nb_pixels'])

        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, infoCanvas)
        line.get_tk_widget().grid(column=2, row=1, rowspan=4, sticky='w')
        df = df[['level', 'nb_pixels']].groupby('level').sum()
        df.plot(kind='line', legend=True, ax=ax, color='r', fontsize=10)
        ax.set_title('histogram')

        data = {
            'level': range(image.max_gray+1),
            'nb_pixels': image.cumulated_histogram()
        }

        df = DataFrame(data, columns=['level', 'nb_pixels'])

        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, infoCanvas)
        line.get_tk_widget().grid(column=3, row=1, rowspan=4, sticky='w')
        df = df[['level', 'nb_pixels']].groupby('level').sum()
        df.plot(kind='line', legend=True, ax=ax, color='r', fontsize=10)
        ax.set_title('cummulated histogram')

    def histogram_equalizer(self):
        self.outputImage = self.inputImage.histogram_equalizer()
        self.updateOutput()

    def updateOutput(self):

        self.outputCanvas.destroy()
        self.initOutputCanvas()
        fig = plt.Figure(figsize=(4, 4), dpi=96)
        ax = fig.add_subplot(111)
        ax.imshow(self.outputImage.matrix, cmap='gray')
        ax.axis('off')
        canvas = FigureCanvasTkAgg(fig, self.outputCanvas)
        canvas.get_tk_widget().grid(column=1, row=2, sticky='w')
        canvas.draw()

        self.updateInfo('output')
        self.root.mainloop()

    def saturation_transformation(self):

        answer = simpledialog.askstring(
            "Input",
            "provide saturation points in this form: x1 y1 x2 y2 x3 y3 ...",
            parent=self.root)
        answer = answer.split()
        saturation_points = []
        while(len(answer) != 0):
            saturation_points.append((int(answer.pop(0)), int(answer.pop(0))))

        self.outputImage = self.inputImage.saturation_transformation(
            saturation_points)
        self.updateOutput()
        return

    def generate_random_noise(self):
        self.outputImage = self.inputImage.generate_random_noise()
        self.updateOutput()

    def median_filter(self):

        answer = simpledialog.askstring(
            "Input",
            "provide the median filter size",
            parent=self.root)
        self.outputImage = self.inputImage.median_filter(int(answer))
        self.updateOutput()

    def average_filter(self):
        answer = simpledialog.askstring(
            "Input",
            "provide the average filter size",
            parent=self.root)
        self.outputImage = self.inputImage.average_filter(int(answer))
        self.updateOutput()

    def saveOutput(self):
        
        filename = filedialog.asksaveasfilename(
            initialdir="./samples", title="choose file location")
        self.outputImage.save_to_pgm(filename)
        return
    
    def binarize(self):
        threshold = simpledialog.askstring(
            "Input",
            "provide the threshold",
            parent=self.root)
        self.outputImage=self.inputImage.binarize(int(threshold))
        self.updateOutput()
        
