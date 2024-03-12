from tkinter import *
from tkinter import messagebox, filedialog
import PIL.Image, PIL.ImageTk

class VideoView:
    def __init__(self, window, window_title, width, height, controller):
        self.window = window
        self.window.title(window_title)
        self.controller = controller  # Assurez-vous que ceci est défini avant de setup_menu
        self.canvas = Canvas(window, width=width, height=height)
        self.canvas.pack()

        self.setup_menu()

        # Créer un Frame pour les boutons pour les organiser horizontalement
        buttons_frame = Frame(window)
        buttons_frame.pack(side=BOTTOM, pady=10)  # Centrer les boutons en bas de la fenêtre

        # Bouton "Début"
        self.rewind_button = Button(buttons_frame, text="<<", command=self.controller.rewind_video)
        self.rewind_button.pack(side=LEFT, padx=5)

        # Bouton "-1 frame"
        self.frame_back_button = Button(buttons_frame, text="<", command=self.controller.frame_back)
        self.frame_back_button.pack(side=LEFT, padx=5)

        # Bouton "Pause"
        self.pause_button = Button(buttons_frame, text="Pause", command=self.controller.pause_video)
        self.pause_button.pack(side=LEFT, padx=5)

        # Bouton "Lire"
        self.resume_button = Button(buttons_frame, text="Lire", command=self.controller.resume_video)
        self.resume_button.pack(side=LEFT, padx=5)

        # Bouton "+1 frame"
        self.frame_forward_button = Button(buttons_frame, text=">", command=self.controller.frame_forward)
        self.frame_forward_button.pack(side=LEFT, padx=5)

        # Bouton "Fin"
        self.forward_button = Button(buttons_frame, text=">>", command=self.controller.forward_video)
        self.forward_button.pack(side=LEFT, padx=5)
        
    def setup_menu(self):
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Ouvrir", command=self.controller.open_file_dialog)
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
    
    def show_frame(self, frame):
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

    def alert_message(self, title, message):
        messagebox.showerror(title=title, message=message)
    
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.controller.open_video(file_path)
