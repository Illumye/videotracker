from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
import PIL.Image, PIL.ImageTk

class VideoView:
    def __init__(self, window, window_title, width, height, controller):
        self.window = window
        self.window.title(window_title)
        self.controller = controller  # Assurez-vous que ceci est défini avant de setup_menu
        self.canvas = Canvas(window, width=width, height=height)
        self.canvas.config(bd=2, relief="solid")
        self.canvas.pack()

        self.setup_menu()
        self.shortcut_key()

        # Créer un Frame pour les boutons pour les organiser horizontalement
        self.buttons_frame = Frame(window)
        self.buttons_frame.pack(side=BOTTOM, pady=10)  # Centrer les boutons en bas de la fenêtre

        # Bouton "Début"
        self.rewind_button = Button(self.buttons_frame, text="<<", command=self.controller.rewind_video)
        self.rewind_button.pack(side=LEFT, padx=5)

        # Bouton "-1 frame"
        self.frame_back_button = Button(self.buttons_frame, text="<", command=self.controller.frame_back)
        self.frame_back_button.pack(side=LEFT, padx=5)

        # Bouton "Pause"
        self.pause_button = Button(self.buttons_frame, text="Pause", command=self.controller.pause_video)
        self.pause_button.pack(side=LEFT, padx=5)

        # Bouton "Lire"
        self.resume_button = Button(self.buttons_frame, text="Lire", command=self.controller.resume_video)
        self.resume_button.pack(side=LEFT, padx=5)

        # Bouton "+1 frame"
        self.frame_forward_button = Button(self.buttons_frame, text=">", command=self.controller.frame_forward)
        self.frame_forward_button.pack(side=LEFT, padx=5)

        # Bouton "Fin"
        self.forward_button = Button(self.buttons_frame, text=">>", command=self.controller.forward_video)
        self.forward_button.pack(side=LEFT, padx=5)
        
        self.canvas.bind("<Button-3>", self.controller.set_scale)
        
        self.canvas.bind("<Button-1>", self.controller.set_origin)
        
    def open_scale_dialog(self):
        scale = simpledialog.askfloat("Échelle", "Entrez la distance réelle entre les deux points (en mètres) :")
        if scale is not None:
            self.controller.scale = scale
        
    def setup_menu(self):
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)

        # Créer un menu "Fichier"
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Charger un fichier vidéo", command=self.controller.open_file_dialog, accelerator="Ctrl+O")
        file_menu.add_command(label="Lire une vidéo", command=self.controller.resume_video, accelerator="Space")
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.window.quit, accelerator="Ctrl+Q")
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        
        # Créer un menu "View"
        view_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Graphique y(x)")
        view_menu.add_command(label="Graphique x(t)")
        view_menu.add_command(label="Graphique y(t)")
        menu_bar.add_cascade(label="View", menu=view_menu)
        
        # Créer un menu "Échelle"
        scale_menu = Menu(menu_bar, tearoff=0)
        scale_menu.add_command(label="Réinitialiser l'échelle", command=self.controller.reset_scale_points)
        menu_bar.add_cascade(label="Echelle", menu=scale_menu)
        
    def shortcut_key(self):
        self.window.bind("<Control-o>", lambda e: self.controller.open_file_dialog()) # Ouvrir un fichier vidéo
        self.window.bind("<Control-q>", lambda e: self.window.quit()) # Quitter l'application
        self.window.bind("<space>", lambda e: self.controller.resume_video() if self.controller.pause else self.controller.pause_video()) # Lire/Pause la vidéo
        self.window.bind("<Left>", lambda e: self.controller.frame_back()) # Reculer d'une frame
        self.window.bind("<Right>", lambda e: self.controller.frame_forward()) # Avancer d'une frame
        self.window.bind("<Control-Left>", lambda e: self.controller.rewind_video()) # Revenir au début de la vidéo
        self.window.bind("<Control-Right>", lambda e: self.controller.forward_video()) # Aller à la fin de la vidéo
    
    def show_frame(self, frame):
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

    def alert_message(self, title, message):
        messagebox.showerror(title=title, message=message)
    
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.controller.open_video(file_path)

    def resize_video(self, width, height):
        self.canvas.config(width=width, height=height)
    
    def rearrange_widgets(self):
        self.canvas.pack_forget()
        self.buttons_frame.pack_forget()
        self.canvas.pack()
        self.buttons_frame.pack(side=BOTTOM, pady=10)
        
    def draw_point(self, x, y):
        radius = 5
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red", tags="scale_point")
    
    def reset_points(self):
        self.canvas.delete("scale_point")