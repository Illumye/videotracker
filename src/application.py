from tkinter import *
from controllers.VideoController import VideoController
from models.VideoModel import VideoModel
from views.VideoView import VideoView

def main():
    window = Tk()
    app_view = VideoView(window, "Video Tracker", 800, 600)
    app_model = VideoModel("./resources/videos/compteur.mp4")
    app_controller = VideoController(app_view, app_model, 15)
    window.mainloop()

if __name__ == "__main__":
    main()