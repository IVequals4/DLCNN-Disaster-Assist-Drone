import tkinter as tk
from tkinter import PhotoImage
import ttkbootstrap as tb

from view import View
from model import Model
from controller import Controller

class Main(tb.Window):
    def __init__(self):
        super().__init__(themename='solar')

        self.title("D.A.D. Menu")

        model = Model()

        self.view = View(self)
        self.view.grid(row=0, column=0)

        controller = Controller(model, self.view)
        self.view.set_controller(controller)

if __name__ == '__main__':
    app = Main()
    app.mainloop()
