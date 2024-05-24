import tkinter as tk
from PIL import ImageTk, Image
import cv2
from tkinter import ttk, filedialog
from ttkbootstrap import Style
import numpy as np
import model  # Assuming model.py has the UNet model

class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Initialize ttkbootstrap style
        self.style = Style(theme='solar')

        # Main frame
        self.main_frame = ttk.Frame(self, style='TFrame')
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Title label
        self.title_label = ttk.Label(self.main_frame, text='DISASTER ASSIST DRONE', font=('Helvetica', 20, 'bold'), style='Primary.TLabel')
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Video canvas
        self.canvas_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.canvas_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=600, bg='black', bd=0, highlightthickness=0)
        self.canvas.pack()

        # Control buttons
        self.top_left_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.top_left_frame.grid(row=1, column=0, sticky='nw', padx=10, pady=10)
        
        self.scan_button = ttk.Button(self.top_left_frame, text='Scan', command=self.scan_window, style='Primary.TButton')
        self.scan_button.grid(row=0, column=0, padx=5, pady=5)

        self.notify_button = ttk.Button(self.top_left_frame, text='Notify', command=self.notify, style='Secondary.TButton')
        self.notify_button.grid(row=1, column=0, padx=5, pady=5)

        self.import_button = ttk.Button(self.top_left_frame, text='Import', command=self.import_file, style='Success.TButton')
        self.import_button.grid(row=2, column=0, padx=5, pady=5)

        self.status_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.status_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky='ew')

        self.status_label = ttk.Label(self.status_frame, text="Status: Ready", font=('Helvetica', 14), style='Info.TLabel')
        self.status_label.pack(fill='x', expand=True)

        # Video capture setup
        self.video_capture = cv2.VideoCapture(0)
        self.cur_img = None
        self.photo = None  # To hold the reference to the image

        self.update_camera(parent)

        # Initialize the model
        self.model = model.Model()

    def set_controller(self, controller):
        self.controller = controller

    def update_camera(self, window):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (800, 600), interpolation=cv2.INTER_AREA)
            self.cur_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.photo = ImageTk.PhotoImage(image=self.cur_img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            window.after(15, lambda: self.update_camera(window))

    def destroy_windows(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

    def import_file(self):
        self.filename = filedialog.askopenfilename(parent=self)
        if self.filename:
            img = Image.open(self.filename)
            img = img.resize((800, 600), Image.Resampling.LANCZOS)
            self.cur_img = img
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.status_label.config(text=f"File imported: {self.filename}")
            self.perform_inference()

    def scan_window(self):
        scan_win = tk.Toplevel(self)
        scan_win.title('Scan Window')

        scan_canvas = tk.Canvas(scan_win, width=512, height=512, bg='black')
        scan_canvas.grid(row=0, column=0, padx=20, pady=20)

        if self.cur_img:
            scan_photo = ImageTk.PhotoImage(self.cur_img.resize((512, 512), Image.Resampling.LANCZOS))
            scan_canvas.create_image(0, 0, image=scan_photo, anchor=tk.NW)
            scan_canvas.image = scan_photo  # Keep a reference to prevent garbage collection
            self.perform_inference()

    def notify(self):
        prediction = self.model.predict(self.cur_img)
        if prediction == 1:
            message = "Road Blocked"
        else:
            message = "Road Clear"
        self.status_label.config(text=message)

    def perform_inference(self):
        if self.cur_img:
            img = np.array(self.cur_img.resize((128, 128), Image.Resampling.LANCZOS))  # Example resize to match model input
            prediction = self.model.predict(img)
            if prediction == 1:
                self.status_label.config(text="Road Blocked")
            else:
                self.status_label.config(text="Road Clear")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Drone Assist")
    root.geometry("850x700")
    root.resizable(False, False)
    view = View(root)
    view.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
