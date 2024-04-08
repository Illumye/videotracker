from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk
import PIL.Image, PIL.ImageTk

class VideoView:
    def __init__(self, window, window_title, width, height, controller, model):
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
        
        self.canvas.bind("<Button-2>", self.controller.set_origin)
        
        self.canvas.bind("<Button-1>", self.controller.track_object)
        
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
        self.window.bind("<Control-o>", lambda e: self.controller.open_file_dialog()) # Ouvrir un fichier vidéo
        self.window.bind("<Control-q>", lambda e: self.window.quit()) # Quitter l'application
        self.window.bind("<space>", lambda e: self.controller.resume_video() if self.controller.pause else self.controller.pause_video()) # Lire/Pause la vidéo
        self.window.bind("<Left>", lambda e: self.controller.frame_back()) # Reculer d'une frame
        self.window.bind("<Right>", lambda e: self.controller.frame_forward()) # Avancer d'une frame
        self.window.bind("<Control-Left>", lambda e: self.controller.rewind_video()) # Revenir au début de la vidéo
        self.window.bind("<Control-Right>", lambda e: self.controller.forward_video()) # Aller à la fin de la vidéo
        self.window.bind("<Escape>", lambda e: self.controller.stop_tracking())
    
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
        
    def draw_point(self, x, y, color, tags):
        radius = 5
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, tags=tags)
    
    def draw_scale(self, points):
        if len(points) < 2:
            return
        self.canvas.create_line(points[0][0], points[0][1], points[1][0], points[1][1], fill="yellow", tags="scale_point")
    
    def draw_axes(self, origin):
        # Dessine l'axe des x
        self.canvas.create_line(origin[0], origin[1], self.canvas.winfo_width(), origin[1], fill="black")
        # Dessine l'axe des y
        self.canvas.create_line(origin[0], origin[1], origin[0], 0, fill="black")
    
    def reset_points(self):
        self.canvas.delete("scale_point")
        
    def update_table(self, points, origin):
        if not hasattr(self, 'table_window') or not self.table_window.winfo_exists():
            return
        else:
            for row in self.table.get_children():
                self.table.delete(row)
        
        for point in points:
            relative_x = point.getX() - origin[0]
            relative_y = origin[1] - point.getY()
            time = point.getTime() + 1
            self.table.insert("", "end", values=(time, relative_y, relative_x))

    def open_table(self):
        print("Open table")
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
        self.table_window.destroy()