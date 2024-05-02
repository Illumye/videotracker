#!/usr/bin/env python3

from tkinter import *
from controllers.VideoController import VideoController
from models.VideoModel import VideoModel
from views.VideoView import VideoView

def main():
    window = Tk()
    app_model: VideoModel | None = None
    app_controller: VideoController = VideoController(None, app_model, 30)
    app_view: VideoView = VideoView(window, "Video Tracker", 800, 600, app_controller, app_model)
    app_controller.view = app_view
    window.mainloop()

if __name__ == "__main__":
    main()