class VideoController:
    def __init__(self, view, model, delay):
        self.view = view
        self.model = model
        self.delay = delay
        self.pause = False
        self.play_video()
        
    def play_video(self):
        ret, frame = self.model.get_frame()
        if ret:
            self.view.show_frame(frame)
        else:
            self.view.alert_message("Alerte", "Fin de la vidéo.")
            return
        if not self.pause:
            self.view.window.after(self.delay, self.play_video)
    
    def pause_video(self):
        self.pause = True
    
    def resume_video(self):
        self.pause = False
        self.play_video()
    
    def release_video(self):
        self.model.release()
