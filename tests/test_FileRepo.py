import unittest
from src.models.FileRepo import FileRepo
from src.models.Point import Point

class test_FileRepo(unittest.TestCase):
    def setUp(self):
        self.file_repo = FileRepo("test.csv", "./tests")
        self.points = [Point(1, 2, 1), Point(3, 4, 2), Point(5, 6, 3)]
        self.temps = [1, 2, 3]
        
    def test_transformData2CSV(self):
        csv_data = self.file_repo.transformData2CSV(self.temps, self.points, ";")
        self.assertEqual(csv_data, "Temps;Position X;Position Y\n1;1;2\n2;3;4\n3;5;6\n")
        
    def test_export2CSV(self):
        self.file_repo.export2CSV(self.temps, self.points, ";")
        with open("./tests/test.csv", "r") as file:
            csv_data = file.read()
        self.assertEqual(csv_data, "Temps;Position X;Position Y\n1;1;2\n2;3;4\n3;5;6\n")
            
    def tearDown(self):
        import os
        if os.path.exists("./tests/test.csv"):
            os.remove("./tests/test.csv")

if __name__ == "__main__":
    unittest.main()