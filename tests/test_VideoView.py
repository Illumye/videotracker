import unittest
import _tkinter
from unittest.mock import MagicMock, patch
from tkinter import Tk, simpledialog, messagebox, filedialog, Canvas, Frame, Toplevel
from src.views.VideoView import VideoView
from src.models.Point import Point

class CustomTclError(Exception):
    pass

@patch('_tkinter.TclError', CustomTclError)
class TestVideoView(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.controller_mock = MagicMock()
        self.model_mock = MagicMock()
        self.view = VideoView(self.root, "Test Video", 800, 600, self.controller_mock, self.model_mock)

    def tearDown(self):
        self.root.destroy()


    # def testResizeVideo(self):        # doesn't work for some reason
    #     # Set initial canvas size
    #     initial_width = 800
    #     initial_height = 600
    #     self.view.canvas.config(width=initial_width, height=initial_height)

    #     # Resize the canvas
    #     new_width = 1024
    #     new_height = 768
    #     self.view.resize_video(new_width, new_height)

    #     print(self.view.canvas.winfo_width(),self.view.canvas.winfo_height())

    #     # Check if canvas size is updated correctly
    #     self.assertEqual(self.view.canvas.winfo_width(), new_width)
    #     self.assertEqual(self.view.canvas.winfo_height(), new_height)

    @patch.object(filedialog, 'askopenfilename', return_value='/path/to/file')  # Mocking the filedialog.askopenfilename method
    def testOpenFile(self, askopenfilename_mock):
        # Simulate opening a file
        self.view.open_file()

        # Ensure that the controller's open_video method is called with the correct file path
        self.controller_mock.open_video.assert_called_once_with('/path/to/file')

    @patch.object(messagebox, 'showerror')  # Patching messagebox.showerror method
    def testAlertMessage(self, showerror_mock):
        # Simulate alert message
        title = "Test Title"
        message = "Test Message"
        self.view.alert_message(title, message)

        # Ensure that messagebox.showerror was called with the correct arguments
        showerror_mock.assert_called_once_with(title=title, message=message)

    @patch.object(simpledialog, 'askfloat', return_value=5.0)  # Mocking the simpledialog.askfloat method
    def testOpenScaleDialog(self, askfloat_mock):
        # Simulate opening the scale dialog
        self.view.open_scale_dialog()

        # Ensure that the controller's scale attribute is set correctly
        self.assertEqual(self.controller_mock.scale, 5.0)

    def testDrawPoint(self):
        # Simulate drawing a point
        self.view.draw_point(100, 100, "red", "test_point")
        items = self.view.canvas.find_withtag("test_point")
        self.assertNotEqual(len(items), 0)

    def testDrawScale(self):
        # Simulate drawing a scale
        self.view.draw_scale([(100, 100), (200, 200)])
        items = self.view.canvas.find_withtag("scale_point")
        self.assertNotEqual(len(items), 0)

    def testDrawAxes(self):
        # Simulate drawing axes
        origin = (50, 50)
        self.view.draw_axes(origin)
        lines = self.view.canvas.find_all()
        self.assertEqual(len(lines), 2)

    def testResetPoints(self):
        # Simulate resetting points
        self.view.canvas.create_oval(0, 0, 10, 10, tags="scale_point")
        self.view.reset_points()
        items = self.view.canvas.find_withtag("scale_point")
        self.assertEqual(len(items), 0)

    def testTable(self):
        self.view.open_table()      # to make sure table_window exists
        del self.view.table_window
        self.view.open_table()
        self.view.open_table()

    def testUpdateTable(self):
        self.view.open_table()      # reset table state
        del self.view.table_window
        self.view.open_table()
        self.view.update_table([Point(-1,-2,0),Point(1,2,3)],(-6,9))
        answer = ["0","11","5","3","7","7"]

        bin = []
        for row in self.view.table.get_children():
            values = self.view.table.item(row,'values')
            for i in values:
                bin.append(i)
        self.assertEqual(answer,bin,"UpdateTable")







class TestRerrangeWidgets(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.controller_mock = MagicMock()
        self.model_mock = MagicMock()
        self.view = VideoView(self.root, "Test Video", 800, 600, self.controller_mock, self.model_mock)
        self.canvas_mock = MagicMock(spec=Canvas)
        self.buttons_frame_mock = MagicMock(spec=Frame)
        self.view.canvas = self.canvas_mock
        self.view.buttons_frame = self.buttons_frame_mock

    def tearDown(self):
        self.root.destroy()

    def testRearrangeWidgets(self):
        # Simulate rearranging widgets
        self.view.rearrange_widgets()

        # Ensure that the canvas and buttons_frame are packed again
        self.canvas_mock.pack.assert_called_once()
        self.buttons_frame_mock.pack.assert_called_once_with(side='bottom', pady=10)


if __name__ == '__main__':
    unittest.main()