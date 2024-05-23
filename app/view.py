import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import cv2
from tkinter import ttk, font, PhotoImage
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from tkinter import filedialog

class View(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent)

    s = tb.Style()
    s.configure('TButton', font=('Helvetica 18 bold'))

    self.BtnWidth = 8
    # print(font.families())

    self.test_Lbl = tb.Label(self,
                             text='DISASTER ASSIST DRONE',
                             font=('Helvetica', 20, 'bold'),
                             bootstyle='primary')
    self.test_Lbl.grid(row=0, column=0, columnspan=5, sticky=tk.W)

    self.video_capture = cv2.VideoCapture(0)
    self.cur_img = None
    self.canvas = tk.Canvas(self, width=640, height=480)
    self.canvas.grid(row=1, column=0, columnspan=5, padx=10)

    self.update_camera(parent)

    self.scanBtn = tb.Button(self, text='SCAN', width=self.BtnWidth, command=lambda:self.scan_window())
    self.scanBtn.grid(row=2, column=0, pady=10, padx=10, ipady=2, sticky=tk.W)
    self.notifyBtn = tb.Button(self, text='NOTIFY', width=self.BtnWidth)
    self.notifyBtn.grid(row=2, column=1, pady=10, padx=10, ipady=2, sticky=tk.W)
    self.importBtn = tb.Button(self, text='IMPORT', width=self.BtnWidth, command=lambda:self.import_file(self))
    self.importBtn.grid(row=2, column=4, pady=10, padx=10, ipady=2)

  def set_controller(self, controller):
    self.controller = controller

  def update_camera(self, window):
    ret, frame = self.video_capture.read()

    if ret:
      frame = cv2.flip(frame, 1)
      frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
      self.cur_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

      self.photo = ImageTk.PhotoImage(image=self.cur_img)
      self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
      window.after(15, lambda:self.update_camera(window))

  def destroy_windows(self):
    cv2.destroyAllWindows()

  def import_file(self, window):
    self.filename = filedialog.askopenfilename(parent=window)
    print(self.filename)

  def scan_window(self):
    scan_Win = tb.Window(self)

    scan_img = None

    scan_canvas = tk.Canvas(scan_Win, width=512, height=512)
    scan_canvas.grid(row=0, column=0, padx=10)

    # ret, frame = self.video_capture.read()

    # if ret:
    #   frame = cv2.flip(frame, 1)
    #   frame = cv2.resize(frame, (512, 512), interpolation=cv2.INTER_AREA)
    #   scan_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #   print(scan_img)
    #   scan_photo = ImageTk.PhotoImage(image=scan_img)
    scan_photo = self.cur_img.resize((512, 512))
    scan_canvas.create_image(0, 0,image=scan_photo)
