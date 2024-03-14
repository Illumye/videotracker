from models.FileRepo import FileRepo
from models.Point import Point
from models.VideoModel import VideoModel
import cv2
import os
from tkinter import filedialog
import matplotlib.pyplot as plt

class VideoController:
    def __init__(self, view, model, delay):
        self.view = view
        self.model = None 
        self.delay = delay
        self.pause = True  # La vidéo est en pause par défaut
        
        # Points pour l'échelle
        self.scale_point1 = None
        self.scale_point2 = None
        self.scale_points = []
        
        self.tracking = True
    
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(initialdir="./resources/videos")  # Ouvre le dialogue de sélection de fichier
        if file_path:
            self.open_video(file_path)
    
    def open_video(self, file_path):
        self.model = VideoModel(file_path)
        self.model.open(file_path)
        video_name = os.path.split(file_path)[1]
        video_width = int(self.model.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(self.model.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if self.model is not None:
            self.model.release()
        self.model = VideoModel(file_path)
        self.view.window.title(f"Video Tracker - {video_name}")
        self.view.resize_video(video_width, video_height)
        self.show_first_frame()
        self.view.rearrange_widgets()
        self.pause = True
        
    def show_first_frame(self):
        # Récupère la première frame sans changer l'état de pause
        ret, frame = self.model.get_frame()
        if ret:
            self.view.show_frame(frame)
        else:
            self.view.alert_message("Erreur", "Impossible de charger la vidéo.")
        self.model.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Réinitialise le capteur à la première frame

    def play_video(self):
        if self.pause or self.model is None:  # Ajouter cette vérification pour éviter de jouer une vidéo non chargée
            return
        ret, frame = self.model.get_frame()
        if ret:
            self.view.show_frame(frame)
            self.view.window.after(self.delay, self.play_video)
        else:
            self.view.alert_message("Alerte", "Fin de la vidéo.")

    def pause_video(self):
        self.pause = True

    def resume_video(self):
        if self.model is not None and self.pause:
            self.pause = False
            self.play_video()

    def release_video(self):
        if self.model is not None and self.model.cap.isOpened():
            self.model.release()
            
    def rewind_video(self):
        if self.model is not None:
            self.model.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.pause = True
            self.show_first_frame()

    def forward_video(self):
        if self.model is not None:
            # Réinitialiser la vidéo pour s'assurer qu'elle part du début
            self.model.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            last_frame = None
            while True:
                ret, frame = self.model.get_frame()
                if not ret:
                    break  # Sortir de la boucle si on ne peut plus lire de frame
                last_frame = frame  # Stocker la dernière frame valide
            
            if last_frame is not None:
                # Afficher la dernière frame valide
                self.view.show_frame(last_frame)
                # S'assurer que la vidéo est en pause après avoir affiché la dernière frame
                self.pause = True
            else:
                self.view.alert_message("Erreur", "Impossible de trouver la dernière frame de la vidéo.")
    def frame_back(self):
        if self.model is not None and self.pause:
            # Reculer d'une frame (doit ajuster car la lecture avance automatiquement de 1)
            current_pos = int(self.model.cap.get(cv2.CAP_PROP_POS_FRAMES))
            # Pour reculer d'une frame réellement, on doit se positionner 2 frames en arrière
            self.model.cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, current_pos - 2))
            self.show_current_frame(back=True)

    def frame_forward(self):
        if self.model is not None and self.pause:
            # Avancer d'une frame (la lecture avance automatiquement de 1 après get_frame)
            self.show_current_frame()

    def show_current_frame(self, back=False):
        ret, frame = self.model.get_frame()
        if ret:
            self.view.show_frame(frame)
            self.view.draw_point(self.model.origin[0], self.model.origin[1], "black", "origin")
            self.view.draw_axes(self.model.origin)
            self.view.draw_point(self.scale_point1[0], self.scale_point1[1], "yellow", "scale_point")
            self.view.draw_point(self.scale_point2[0], self.scale_point2[1], "yellow", "scale_point")
            self.view.draw_scale(self.scale_points)
            for point in self.model.points:
                color = "red" if point == self.model.points[-1] else "green"
                self.view.draw_point(point.getX(), point.getY(), color, "points")
            if back:
                # Après avoir montré la frame précédente, ajuster pour rester sur cette frame
                current_pos = int(self.model.cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.model.cap.set(cv2.CAP_PROP_POS_FRAMES, current_pos - 1)
        else:
            self.view.alert_message("Erreur", "Impossible de naviguer dans la vidéo.")

    def set_scale(self, event):
        if self.model is None:
            return
        
        if self.scale_point1 is not None and self.scale_point2 is not None:
            return
        
        self.view.draw_point(event.x, event.y, "yellow", "scale_point")
        
        if self.scale_point1 is None:
            self.scale_point1 = (event.x, event.y)
            self.scale_points.append(self.scale_point1)
        else:
            self.scale_point2 = (event.x, event.y)
            self.scale_points.append(self.scale_point2)
            self.view.open_scale_dialog()
        self.view.draw_scale(self.scale_points)

    def reset_scale_points(self):
        self.scale_point1 = None
        self.scale_point2 = None
        self.scale_points = []
        self.view.reset_points()
        
    def set_origin(self, event):
        if self.model is None:
            return
        if self.model.origin is None:
            self.model.origin = (event.x, event.y)
            self.view.draw_point(event.x, event.y, "black", "origin")
            self.view.draw_axes(self.model.origin)
    
    def track_object(self, event):
        if self.model is None:
            return
        current_pos = int(self.model.cap.get(cv2.CAP_PROP_POS_FRAMES))
        total_frames = int(self.model.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if current_pos >= total_frames - 1:
            self.view.alert_message("Alerte", "Fin de la vidéo.")
            return
        if not self.tracking:
            return
        if self.model.origin is None:
            return
        if self.model.points:
            last_point = self.model.points[-1]
            self.view.draw_point(last_point.getX(), last_point.getY(), "green", "points")
        point = Point(event.x, event.y, current_pos)
        self.model.points.append(point)
        self.view.draw_point(point.getX(), point.getY(), "red", "points")
        self.frame_forward()
        self.view.update_table(self.model.points, self.model.origin)
    
    def stop_tracking(self):
        self.tracking = False
        self.view.alert_message("Information", "Le pointage a été arrêté manuellement.")
    
    def update_table(self):
        if self.model is not None:
            points = self.model.get_points()
            self.view.update_table(points, self.model.origin)
    
    def add_point(self, point):
        self.model.add_point(point)
        self.view.update_table(self.model.get_points(), self.model.origin)
        
    def show_yx_graph(self):
        points = self.points
        
        x = [point.getX() for point in points]
        y = [point.getY() for point in points]
        
        plt.figure()
        plt.plot(x, y)
        plt.title('Graphique y(x)')
        plt.xlabel('x')
        plt.ylabel('y')
        
        plt.show()
        
    def show_xt_graph(self):
        points = self.points
        
        t = [point.getTime() for point in points]
        x = [point.getX() for point in points]
        
        plt.figure()
        plt.plot(t, x)
        plt.title('Graphique x(t)')
        plt.xlabel('t')
        plt.ylabel('x')
        
        plt.show()
    
    def show_yt_graph(self):
        points = self.points
        
        t = [point.getTime() for point in points]
        y = [point.getY() for point in points]
        
        plt.figure()
        plt.plot(t, y)
        plt.title('Graphique y(t)')
        plt.xlabel('t')
        plt.ylabel('y')
        
        plt.show()
    
    def save_points_to_csv(self, file_name, path):
        file_repo = FileRepo(file_name, path)
        temps = [point.getTime() for point in self.points]
        points = [point for point in self.points]
        file_repo.export2CSV(temps, points)
        
    def save_points_to_csv_dialog(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")], initialdir="./resources/points")
        if file_name:
            path, file_name = os.path.split(file_name)
            self.save_points_to_csv(file_name, path)