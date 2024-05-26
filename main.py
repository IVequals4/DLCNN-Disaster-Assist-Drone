import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Style
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import json
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import base64
import numpy as np
from controller import Controller
from appmodel import Model

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE = 'C:\\Users\\jonat\\OneDrive\\Desktop\\Repo\\DLCNN-Disaster-Assist-Drone\\app\\credentials.json'
TOKEN_FILE = 'token.json'

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("850x700")
        self.title("Disaster Assist Drone")

        self.bg_image_path = "DLCNN-Disaster-Assist-Drone/Background.jpg"
        self.bg_image = Image.open(self.bg_image_path).resize((850, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.image = self.bg_photo
        self.bg_label.pack(fill="both", expand=True)

        self.title_label = tk.Label(self, text='Disaster Assist Drone', font=('Helvetica', 24, 'bold'), foreground='white', background='#cd7f32', borderwidth=2, relief="solid", padx=10, pady=5)
        self.title_label.place(relx=0.5, rely=0.4, anchor='center')

        self.message_label = tk.Label(self, text='Here to help all your drone and road identification needs!', font=('Helvetica', 18), foreground='white', background='#cd7f32', borderwidth=2, relief="solid", padx=10, pady=5)
        self.message_label.place(relx=0.5, rely=0.5, anchor='center')

        self.continue_button = ttk.Button(self, text="Continue", command=self.on_continue, style='Large.TButton')
        self.continue_button.place(relx=0.5, rely=0.65, anchor='center', width=300, height=100)

    def on_continue(self):
        self.destroy()
        self.master.deiconify()

class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.photo = None
        self.images = []
        self.photos = []
        self.image_filenames = []

        self.style = Style(theme='solar')
        self.style.configure('Large.TButton', font=('Helvetica', 24), padding=(20, 20), width=25)
        self.bg_image_path = "DLCNN-Disaster-Assist-Drone/Background.jpg"
        self.bg_image = Image.open(self.bg_image_path).resize((850, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.bg_label = tk.Label(self.main_frame, image=self.bg_photo)
        self.bg_label.image = self.bg_photo
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label_frame = tk.Frame(self.main_frame, bd=2, relief="solid", background='#cd7f32')
        self.title_label_frame.place(x=200, y=20)
        self.title_label = tk.Label(self.title_label_frame, text='DISASTER ASSIST DRONE', font=('Helvetica', 24, 'bold'), foreground='white', background='#cd7f32', borderwidth=2, relief="solid", padx=10, pady=5)
        self.title_label.pack()

        self.style.configure('Custom.TButton', font=('Helvetica', 14), padding=(10, 12), width=20)
        self.scan_button = ttk.Button(self.main_frame, text='Scan', command=lambda: self.show_frame(self.scan_frame), style='Custom.TButton')
        self.scan_button.place(x=100, y=200)

        self.notify_button = ttk.Button(self.main_frame, text='Notify', command=lambda: self.show_frame(self.notify_frame), style='Custom.TButton')
        self.notify_button.place(x=500, y=200)

        self.import_button = ttk.Button(self.main_frame, text='Import', command=lambda: self.show_frame(self.import_frame), style='Custom.TButton')
        self.import_button.place(x=100, y=300)

        self.about_button = ttk.Button(self.main_frame, text='About Us', command=lambda: self.show_frame(self.about_us_frame), style='Custom.TButton')
        self.about_button.place(x=500, y=300)

        self.manual_button = ttk.Button(self.main_frame, text='Manual', command=lambda: self.show_frame(self.manual_frame), style='Custom.TButton')
        self.manual_button.place(x=300, y=400)

        self.controller = Controller(Model(), self)

        self.cur_img = None
        
        self.scan_frame = self.create_frame("Scan Section", 600, 300, True)
        self.notify_frame = self.create_frame("Notify Section", 600, 500, False)
        self.import_frame = self.create_frame("Import Section", 600, 300, True)
        self.about_us_frame = self.create_frame("About Us Section", 600, 300, True)
        self.manual_frame = self.create_frame("Manual Section", 600, 300, True)

        # if not os.path.exists(CREDENTIALS_FILE):
        #     messagebox.showerror("Error", f"'{CREDENTIALS_FILE}' not found. Please place the file in the same directory as this script.")
        #     return
        # self.credentials = self.authenticate_google()

    def create_frame(self, text, width, height, move_higher):
        frame = tk.Frame(self, width=850, height=700)
        frame.grid(row=0, column=0, sticky="nsew")
        bg_label = tk.Label(frame, image=self.bg_photo)
        bg_label.image = self.bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        title_label_frame = tk.Frame(frame, bd=2, relief="solid", background='#cd7f32')
        title_label_frame.place(relx=0.5, rely=0.1, anchor='center')
        title_label = tk.Label(title_label_frame, text=text, font=('Helvetica', 24, 'bold'), foreground='white', background='#cd7f32', borderwidth=2, relief="solid", padx=10, pady=5)
        title_label.pack()
        if move_higher:
            content_frame = tk.Frame(frame, bd=2, relief="solid", background='white')
            content_frame.place(relx=0.5, rely=0.45, anchor='center', width=width, height=height)
        else:
            content_frame = tk.Frame(frame, bd=2, relief="solid", background='white')
            content_frame.place(relx=0.5, rely=0.55, anchor='center', width=width, height=height)
        back_button = ttk.Button(frame, text="Back", command=lambda: self.show_frame(self.main_frame), style='Custom.TButton')
        back_button.place(relx=0.5, rely=0.9, anchor='center')

        if text == "Import Section":
            self.init_import_section(content_frame)
        elif text == "Scan Section":
            self.init_scan_section(content_frame)
        elif text == "Notify Section":
            self.init_notify_section(content_frame)
        elif text == "About Us Section":
            self.init_about_us_section(content_frame)
        elif text == "Manual Section":
            self.init_manual_section(content_frame)
        return frame

    def init_import_section(self, content_frame):
        import_button = ttk.Button(content_frame, text="Import Images", command=self.import_files, style='Custom.TButton')
        import_button.pack(pady=20)
        self.import_indicator = tk.Label(content_frame, text="No images imported", font=('Helvetica', 14), foreground='red', background='white')
        self.import_indicator.pack(pady=10)

    def init_scan_section(self, content_frame):
        self.image_options = ttk.Combobox(content_frame, state="readonly")
        self.image_options.pack(pady=10)
        self.scan_button = ttk.Button(content_frame, text="Scan Selected Image", style='Custom.TButton', command=self.scan_selected_image)
        self.scan_button.pack(pady=10)
        self.image_options.bind("<<ComboboxSelected>>", self.display_selected_image)
        self.scan_image_label = tk.Label(content_frame, background='white')
        self.scan_image_label.pack(pady=10)
        self.non_scan_image_label = tk.Label(content_frame, background='white')
        self.non_scan_image_label.pack(pady=10)
        self.preview_button = ttk.Button(content_frame, text="Preview Image", style='Custom.TButton', command=self.preview_image)
        self.preview_button.pack(pady=10)

    def init_notify_section(self, content_frame):
        notify_label = tk.Label(content_frame, text="Send Email/Message", font=('Helvetica', 14), background='white', padx=10, pady=5)
        notify_label.pack(pady=10)
        email_label = ttk.Label(content_frame, text="Email:", font=('Helvetica', 12))
        email_label.pack(pady=5)
        self.email_entry = ttk.Entry(content_frame, font=('Helvetica', 12))
        self.email_entry.pack(pady=5)
        message_label = ttk.Label(content_frame, text="Message:", font=('Helvetica', 12))
        message_label.pack(pady=5)
        self.message_entry = ttk.Entry(content_frame, font=('Helvetica', 12))
        self.message_entry.pack(pady=5)
        self.image_options_notify = ttk.Combobox(content_frame, state="readonly")
        self.image_options_notify.pack(pady=5)
        self.attach_button = ttk.Button(content_frame, text="Attach Image", style='Custom.TButton', command=self.attach_image)
        self.attach_button.pack(pady=5)
        self.selected_image = None
        self.selected_image_label = tk.Label(content_frame, text="No image selected", font=('Helvetica', 12), background='white')
        self.selected_image_label.pack(pady=5)
        send_button = ttk.Button(content_frame, text="Send", style='Custom.TButton', command=self.send_email)
        send_button.pack(pady=20)

    def init_about_us_section(self, content_frame):
        about_text = "This application was developed to assist with disaster management using drone technology."
        about_label = tk.Label(content_frame, text=about_text, font=('Helvetica', 14), wraplength=550, background='white')
        about_label.pack(pady=20)

    def init_manual_section(self, content_frame):
        manual_text = (
            "This is the user manual for the Disaster Assist Drone application.\n\n"
            "Scan: Use this button to scan the imported image.\n\n"
            "Notify: Use this button to send an email in case of an emergency.\n\n"
            "Import: Use this button to import an image for scanning.\n\n"
            "About Us: Learn more about the project and the team behind it."
        )
        manual_label = tk.Label(content_frame, text=manual_text, font=('Helvetica', 14), wraplength=550, background='white')
        manual_label.pack(pady=20)

    def show_frame(self, frame):
        frame.tkraise()

    def import_files(self):
        self.filenames = filedialog.askopenfilenames(parent=self)
        if self.filenames:
            new_images = [Image.open(f) for f in self.filenames]
            self.images.extend(new_images)
            self.photos.extend([ImageTk.PhotoImage(img) for img in new_images])
            self.import_indicator.config(text="Images imported successfully", foreground='green')
            new_filenames = [os.path.basename(f) for f in self.filenames]
            self.image_filenames.extend(new_filenames)
            self.image_options['values'] = self.image_filenames
            self.image_options_notify['values'] = self.image_filenames
            if not self.image_options.current():
                self.image_options.current(0)
            if not self.image_options_notify.current():
                self.image_options_notify.current(0)

    def display_selected_image(self, event=None):
        pass

    def preview_image(self):
        if self.images:
            selected_index = self.image_options.current()
            self.cur_img = self.images[selected_index]
            self.photo = self.photos[selected_index]
            preview_window = tk.Toplevel(self)
            preview_window.title("Preview Image")
            preview_label = tk.Label(preview_window, image=self.photo)
            preview_label.image = self.photo
            preview_label.pack()

    def scan_selected_image(self):
        if self.images:
            scan_window = tk.Toplevel(self)
            scan_window.title("Scan Result")

            selected_index = self.image_options.current()
            self.cur_img = self.images[selected_index]
            filename = self.image_options['values'][selected_index]
            # self.photo = self.photos[selected_index]

            # STATUS IS A BOOLEAN ON WHETHER OR NOT A BLOCKAGE WAS FOUND
            # CURRENTLY UNUSED
            prediction_image, status = self.controller.predict_roads(self.cur_img, filename)

            original_image_label = tk.Label(scan_window, text="Original Image", font=('Helvetica', 14), background='white')
            original_image_label.grid(row=0, column=0, padx=20, pady=10)

            input_photo = ImageTk.PhotoImage(self.cur_img.resize((400, 400)))
            input_label = tk.Label(scan_window, image=input_photo)
            input_label.image = input_photo
            input_label.grid(row=1, column=0, padx=20, pady=10)

            result_label = tk.Label(scan_window, text="Prediction", font=('Helvetica', 14), background='white')
            result_label.grid(row=0, column=1, padx=20, pady=10)

            prediction_image = (prediction_image > 0.5).astype(np.uint8) * 255
            prediction_image = Image.fromarray(prediction_image)
            prediction_photo = ImageTk.PhotoImage(prediction_image.resize((400, 400)))
            pred_label = tk.Label(scan_window, image=prediction_photo)
            pred_label.image = prediction_photo
            pred_label.grid(row=1, column=1, padx=20, pady=10)

            block_label = tk.Label(scan_window, text="Blockage Prediction", font=('Helvetica', 14), background='white')
            block_label.grid(row=0, column=2, padx=20, pady=10)

            vector_img = Image.open(f'{filename} vector prediction.png')
            vector_img = vector_img.resize((400, 400))
            vector_photo = ImageTk.PhotoImage(vector_img)
            vector_label = tk.Label(scan_window, image=vector_photo)
            vector_label.image = vector_photo
            vector_label.grid(row=1, column=2, padx=20, pady=10)

    def attach_image(self):
        if self.images:
            selected_index = self.image_options_notify.current()
            self.selected_image = self.images[selected_index]
            self.selected_image_label.config(text=f"Selected: {self.image_filenames[selected_index]}")

    def send_email(self):
        email = self.email_entry.get()
        message = self.message_entry.get()
        try:
            msg = MIMEMultipart()
            msg['From'] = 'your_email@gmail.com'
            msg['To'] = email
            msg['Subject'] = 'Emergency Notification'
            msg.attach(MIMEText(message, 'plain', 'utf-8'))  # Set encoding to 'utf-8'
            if self.selected_image:
                attachment = self.selected_image.convert("RGB")
                attachment.save("temp_image.jpg")
                with open("temp_image.jpg", "rb") as img_file:
                    img_attachment = MIMEBase('application', 'octet-stream')
                    img_attachment.set_payload(img_file.read())
                    encoders.encode_base64(img_attachment)
                    img_attachment.add_header("Content-Disposition", "attachment", filename="image.jpg")
                    msg.attach(img_attachment)
            service = googleapiclient.discovery.build('gmail', 'v1', credentials=self.credentials)
            raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            message = {'raw': raw_message}
            service.users().messages().send(userId="me", body=message).execute()
            self.show_message("Message Sent Successfully!")
        except Exception as e:
            self.show_message(f"Failed to send message: {str(e)}")

    def authenticate_google(self):
        creds = None
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r') as token:
                creds = google.oauth2.credentials.Credentials.from_authorized_user_info(json.load(token), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(google.auth.transport.requests.Request())
            else:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        return creds

    def show_message(self, message):
        messagebox.showinfo("Notification", message)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Drone Assist")
    root.geometry("850x700")
    root.resizable(False, False)
    root.withdraw()
    style = Style(theme='solar')
    style.configure('Selected.TButton', background='#d4af37', font=('Helvetica', 14), padding=(10, 12), width=20)
    splash = SplashScreen(root)
    view = View(root)
    view.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
