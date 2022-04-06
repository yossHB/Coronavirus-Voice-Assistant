import unittest
from unittest import result
import main
import classCovid

class TestProject(unittest.TestCase):

    def test_get_audio(self):
        result = main.get_audio()
        self.assertAlmostEqual(result,'stop')
    
    def test_get_list_of_countries(self):
        pass
