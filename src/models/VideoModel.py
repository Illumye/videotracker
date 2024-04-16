import cv2
from .Point import Point

class VideoModel:
    def __init__(self, filename: str):
        """
        Constructeur de la classe VideoModel.

        Args:
            filename (str): Le chemin de la vidéo.
        """
        self.filename = filename
        self.cap = cv2.VideoCapture(self.filename)
        self.points: list[Point] = []
        self.origin = None

    def open(self, filename: str):
        """
        Ouvre une vidéo.
        
        Args:
            filename (str): Le chemin de la vidéo.
        """
        self.filename = filename
        self.cap = cv2.VideoCapture(self.filename)
        if not self.cap.isOpened():
            print("Erreur: Impossible d'ouvrir la vidéo.")
        
    def get_frame(self) -> tuple[bool, any]:
        """
        Récupère une image de la vidéo.

        Returns:
            tuple[bool, any]: Un tuple contenant un booléen et une image.
        """
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                print("Erreur: Impossible d'ouvrir la vidÃ©o.")
                return False, None
        except:
            # messagebox.showerror(title='Alert', message='End of the video.')
            return False, None
            
    def release(self):
        """
        Ferme la vidéo.
        """
        if self.cap.isOpened():
            self.cap.release()

    def get_points(self) -> list[Point]:
        """
        Récupère les points de la vidéo.

        Returns:
            list[Point]: La liste des points.
        """
        return self.points

    def add_point(self, point: Point):
        """
        Ajoute un point à la vidéo.

        Args:
            point (Point): Le point à ajouter.
        """
        self.points.append(point)