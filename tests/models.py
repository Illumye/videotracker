import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"\\..\\src\\models")
print(sys.path)
import FileRepo
import Point

class TestFileRepo(unittest.TestCase):
    def setUp(self):
        self.repo = FileRepo.FileRepo("FileRepoTest",".")
    def testTransformData2CSV(self):
        print(self.repo.transformData2CSV([i for i in range(10)],[Point.Point(i,i,i) for i in range(10)],";"))
        self.assertEqual(
            self.repo.transformData2CSV([i for i in range(10)],[Point.Point(i,i,i) for i in range(10)],';'),
            "Temps;Position X;Position Y\n0;0;0\n1;1;1\n2;2;2\n3;3;3\n4;4;4\n5;5;5\n6;6;6\n7;7;7\n8;8;8\n9;9;9\n"
        )



if __name__ == "__main__":
    unittest.main(verbosity=2)