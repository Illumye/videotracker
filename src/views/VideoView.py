from tkinter import *
from tkinter import messagebox
import PIL.Image, PIL.ImageTk

class VideoView:
    def __init__(self, window, window_title, width, height):
        self.window = window
        self.window.title(window_title)
        self.canvas = Canvas(window, width=width, height=height)
        self.canvas.pack()
    
    def show_frame(self, frame):
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image = photo, anchor = NW)
        self.window.photo = photo
    
    def alert_message(self, title, message):
        messagebox.showerror(title=title, message=message)
