from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk
import PIL.Image, PIL.ImageTk

class VideoView:
    def __init__(self, window: Tk, window_title: str, width: int, height: int, controller, model):
        """
        Constructeur de la classe VideoView.

        Args:
            window (Tk): La fenêtre principale.
            window_title (str): Le titre de la fenêtre.
            width (int): La largeur de la fenêtre.
            height (int): La hauteur de la fenêtre.
            controller (VideoController): Le contrôleur de la vidéo.
            model (VideoModel): Le modèle de la vidéo.
        """
        self.window = window
        self.window.title(window_title)
        self.controller = controller
        self.model = model
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
        self.frame_back_button = Button(self.buttons_frame, text="⏮", command=self.controller.frame_back)
        self.frame_back_button.pack(side=LEFT, padx=5)

        # Bouton "Pause"
        self.pause_button = Button(self.buttons_frame, text="⏸", command=self.controller.pause_video)
        self.pause_button.pack(side=LEFT, padx=5)

        # Bouton "Lire"
        self.resume_button = Button(self.buttons_frame, text="⏵", command=self.controller.resume_video)
        self.resume_button.pack(side=LEFT, padx=5)

        # Bouton "+1 frame"
        self.frame_forward_button = Button(self.buttons_frame, text="⏭", command=self.controller.frame_forward)
        self.frame_forward_button.pack(side=LEFT, padx=5)

        # Bouton "Fin"
        self.forward_button = Button(self.buttons_frame, text=">>", command=self.controller.forward_video)
        self.forward_button.pack(side=LEFT, padx=5)
        
        self.canvas.bind("<Button-3>", self.controller.set_scale)
        
        self.canvas.bind("<Button-2>", self.controller.set_origin)
        
        self.canvas.bind("<Button-1>", self.controller.track_object)
        
    def open_scale_dialog(self):
        """
        Ouvre une boîte de dialogue pour définir l'échelle.
        """
        scale = simpledialog.askfloat("Échelle", "Entrez la distance réelle entre les deux points (en mètres) :")
        if scale is not None:
            self.controller.scale = scale
        
    def setup_menu(self):
        """
        Crée un menu pour l'application.
        """
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)

        # Créer un menu "Fichier"
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Charger un fichier vidéo", command=self.controller.open_file_dialog, accelerator="Ctrl+O")
        file_menu.add_command(label="Lire une vidéo", command=self.controller.resume_video, accelerator="Space")
        file_menu.add_separator()
        file_menu.add_command(label="Exporter les données du tableau", command=self.controller.save_points_to_csv_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.window.quit, accelerator="Ctrl+Q")
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        
        # Créer un menu "View"
        view_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Graphique y(x)", command=self.controller.show_yx_graph)
        view_menu.add_command(label="Graphique x(t)", command=self.controller.show_xt_graph)
        view_menu.add_command(label="Graphique y(t)", command=self.controller.show_yt_graph)
        menu_bar.add_cascade(label="View", menu=view_menu)
        
        # Créer un menu "Échelle"
        scale_menu = Menu(menu_bar, tearoff=0)
        scale_menu.add_command(label="Réinitialiser l'échelle", command=self.controller.reset_scale_points)
        menu_bar.add_cascade(label="Echelle", menu=scale_menu)
        
        # Créer un menu "Éditer"
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Afficher valeurs", command=self.open_table)
        menu_bar.add_cascade(label="Editer", menu=edit_menu)
        
        
    def shortcut_key(self):
        """
        Définit les raccourcis clavier pour l'application.
        """
        self.window.bind("<Control-o>", lambda e: self.controller.open_file_dialog()) # Ouvrir un fichier vidéo
        self.window.bind("<Control-q>", lambda e: self.window.quit()) # Quitter l'application
        self.window.bind("<space>", lambda e: self.controller.resume_video() if self.controller.pause else self.controller.pause_video()) # Lire/Pause la vidéo
        self.window.bind("<Left>", lambda e: self.controller.frame_back()) # Reculer d'une frame
        self.window.bind("<Right>", lambda e: self.controller.frame_forward()) # Avancer d'une frame
        self.window.bind("<Control-Left>", lambda e: self.controller.rewind_video()) # Revenir au début de la vidéo
        self.window.bind("<Control-Right>", lambda e: self.controller.forward_video()) # Aller à la fin de la vidéo
        self.window.bind("<Escape>", lambda e: self.controller.stop_tracking())
    
    def show_frame(self, frame):
        """
        Affiche une image dans le canevas.
        """
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

    def alert_message(self, title: str, message: str):
        """
        Affiche une boîte de dialogue d'alerte.

        Args:
            title (str): Le titre de la boîte de dialogue.
            message (str): Le message de la boîte de dialogue.
        """
        messagebox.showerror(title=title, message=message)
    
    def open_file(self):
        """
        Ouvre une boîte de dialogue pour sélectionner un fichier vidéo.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.controller.open_video(file_path)

    def resize_video(self, width: int, height: int):
        """
        Redimensionne le canevas.

        Args:
            width (int): La largeur du canevas.
            height (int): La hauteur du canevas.
        """
        self.canvas.config(width=width, height=height)
    
    def rearrange_widgets(self):
        """
        Réorganise les widgets dans la fenêtre.
        """
        self.canvas.pack_forget()
        self.buttons_frame.pack_forget()
        self.canvas.pack()
        self.buttons_frame.pack(side=BOTTOM, pady=10)
        
    def draw_point(self, x: int, y: int, color: str, tags: str):
        """
        Dessine un point sur le canevas.

        Args:
            x (int): La coordonnée x du point.
            y (int): La coordonnée y du point.
            color (str): La couleur du point.
            tags (str): Les tags du point.
        """
        radius = 5
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, tags=tags)
    
    def draw_scale(self, points: list):
        """
        Dessine l'échelle sur le canevas.
        
        Args:
            points (list): La liste des points de l'échelle.
        """
        if len(points) < 2:
            return
        self.canvas.create_line(points[0][0], points[0][1], points[1][0], points[1][1], fill="yellow", tags="scale_point")
    
    def draw_axes(self, origin: tuple):
        """
        Dessine les axes sur le canevas.

        Args:
            origin (tuple): Les coordonnées de l'origine.
        """
        # Dessine l'axe des x
        self.canvas.create_line(origin[0], origin[1], self.canvas.winfo_width(), origin[1], fill="black")
        # Dessine l'axe des y
        self.canvas.create_line(origin[0], origin[1], origin[0], 0, fill="black")
    
    def reset_points(self):
        """
        Réinitialise les points sur le canevas.
        """
        self.canvas.delete("scale_point")
        
    def update_table(self, points: list, origin: tuple):
        """
        Met à jour le tableau des valeurs.

        Args:
            points (list): La liste des points.
            origin (tuple): Les coordonnées de l'origine.
        """
        if not hasattr(self, 'table_window') or not self.table_window.winfo_exists():
            return
        else:
            for row in self.table.get_children():
                self.table.delete(row)
        
        for point in points:
            relative_x = point.getX() - origin[0]
            relative_y = origin[1] - point.getY()       # big brain moment
            time = point.getTime()
            self.table.insert("", "end", values=(time, relative_y, relative_x))

    def open_table(self):
        """
        Ouvre une boîte de dialogue pour afficher les valeurs.
        """
        # print("Open table")
        if not hasattr(self, 'table_window') or not self.table_window.winfo_exists():
            self.table_window = Toplevel(self.window)
            self.table_window.title("Valeurs")
            self.table = ttk.Treeview(self.table_window, columns=("Temps", "Position X", "Position Y"), show="headings")
            self.table.heading("Temps", text="Temps")
            self.table.heading("Position X", text="Position X")
            self.table.heading("Position Y", text="Position Y")
            self.table.pack()
            if self.model is not None:
                self.update_table(self.model.points, self.model.origin)
            self.table_window.protocol("WM_DELETE_WINDOW", self.close_table)
        else:
            if self.model is not None:
                self.update_table(self.model.points, self.model.origin)
            
    def close_table(self):
        """
        Ferme la boîte de dialogue des valeurs.
        """
        self.table_window.destroy()