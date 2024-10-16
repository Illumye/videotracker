import unittest
import src.models.FileRepo as FileRepo
import src.models.VideoModel as VideoModel
import src.models.Point as Point
from unittest.mock import patch

class TestFileRepo(unittest.TestCase):
    def setUp(self):
        self.repo = FileRepo.FileRepo("FileRepoTest",".")
    def testTransformData2CSV(self):
        self.repo.transformData2CSV([i for i in range(10)],[Point.Point(i,i,i) for i in range(10)],";")
        self.assertEqual(
            self.repo.transformData2CSV([i for i in range(10)],[Point.Point(i,i,i) for i in range(10)],';'),
            "Temps;Position X;Position Y\n0;0;0\n1;1;1\n2;2;2\n3;3;3\n4;4;4\n5;5;5\n6;6;6\n7;7;7\n8;8;8\n9;9;9\n"
        )

class TestPoint(unittest.TestCase):
    def setUp(self):
        self.point = Point.Point(1,2,3)
    def testPoint(self):

        self.assertEqual(
            self.point.getX(), 1, "Point.getX"
        )

        self.assertEqual(
            self.point.getY(), 2, "Point.getY"
        )

        self.assertEqual(
            self.point.getTime(), 3, "Point.getTime"
        )

class TestVideoModel(unittest.TestCase):
    def setUp(self):
        self.video = VideoModel.VideoModel("tests/ressources/test_video.mp4")
        
    def tearDown(self):
        self.video.release()
        
    def testOpenVideo(self):
        self.video.open("tests/ressources/test_video.mp4")
        self.assertTrue(self.video.cap.isOpened())
        
    def testGetFrame(self):
        self.video.open("tests/ressources/test_video.mp4")
        ret, frame = self.video.get_frame()
        self.assertTrue(ret)
        self.assertIsNotNone(frame)
        
    def testAddPoint(self):
        point = Point.Point(1, 2, 3)
        self.video.add_point(point)
        self.assertIn(point, self.video.get_points())

    def testGetPoint(self):
        point = Point.Point(1, 2, 3)
        self.video.add_point(point)
        point2 = Point.Point(2, 3, 4)
        points = [point,point2]
        self.video.add_point(point2)
        self.assertEqual(points, self.video.get_points())
    
    def testErrorMessage(self):
        with patch('builtins.print') as mocked_print:
            self.video.open("nonexistent_video.mp4")
            mocked_print.assert_called_with("Erreur: Impossible d'ouvrir la vidéo.")

    def testExcept(self):
        with patch('builtins.print') as mocked_print:
            self.video.open("nonexistent_video.mp4")
            a,b = self.video.get_frame()
            mocked_print.assert_called_with("Erreur: Impossible d'ouvrir la vidÃ©o.")
            self.assertEqual(a,False)
            self.assertEqual(b,None)

if __name__ == "__main__":
    unittest.main()