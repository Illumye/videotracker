import cv2

class VideoModel:
    def __init__(self, filename):
        self.filename = filename
        self.cap = cv2.VideoCapture(self.filename)
        
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
