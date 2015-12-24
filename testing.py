import unittest
import extractexcel as excel

myfile = open('A test csv.csv', 'r')

ExcelFile = excel.Excel(myfile)

class Test(unittest.TestCase):

    def setUp(self):
        self.fixture = ExcelFile.get_num_of_subjects()

    def tearDown(self):
        del self.fixture

    def test(self):
        self.failUnlessEqual(self.fixture, 30)

if __name__ =='__main__':
    unittest.main()
