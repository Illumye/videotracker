import cv2
from .Point import Point

class VideoModel:
    def __init__(self, filename):
        self.filename = filename
        self.cap = cv2.VideoCapture(self.filename)
        self.points: list[Point] = []
        self.origin = None

    def open(self, filename):
        self.filename = filename
        self.cap = cv2.VideoCapture(self.filename)
        if not self.cap.isOpened():
            print("Erreur: Impossible d'ouvrir la vidéo.")
        
    def get_frame(self):
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
        if self.cap.isOpened():
            self.cap.release()

    def get_points(self):
        return self.points

    def add_point(self, point: Point):
        self.points.append(point)