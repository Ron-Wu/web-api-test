import unittest
from app import home, FindWally, CreateNews, success, FindNews

class Testdemo(unittest.TestCase):
    def test_home(self):
        self.assertEqual(home(), "Welcome!")

    def test_FindWally(self):
        self.assertEqual(FindWally(), "Wally")

    def test_CreateNews(self):
        self.assertEqual(CreateNews(), "createNews done")

    def test_success(self):
        self.assertEqual(success('Wally'), "Hello World")

    def test_FindNews(self):
        self.assertEqual(FindNews(), "Wally")