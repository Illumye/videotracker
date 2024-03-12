from models.VideoModel import VideoModel
import cv2
from tkinter import filedialog

class VideoController:
    def __init__(self, view, model, delay):
        self.view = view
        self.model = model 
        self.delay = delay
        self.pause = True  # La vidéo est en pause par défaut
    
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()  # Ouvre le dialogue de sélection de fichier
        if file_path:
            self.open_video(file_path)
    
    def open_video(self, file_path):
        if self.model is not None:
            self.model.release()
        self.model = VideoModel(file_path)
        self.show_first_frame()
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
            if back:
                # Après avoir montré la frame précédente, ajuster pour rester sur cette frame
                current_pos = int(self.model.cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.model.cap.set(cv2.CAP_PROP_POS_FRAMES, current_pos - 1)
        else:
            self.view.alert_message("Erreur", "Impossible de naviguer dans la vidéo.")
