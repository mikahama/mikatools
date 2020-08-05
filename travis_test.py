#encoding: utf-8
import unittest
from mikatools import *


class TestFSTS(unittest.TestCase):

    def setUp(self):
        pass

    def test_json(self):
        result = {"äfdfer" : "009id"}
        json_dump(result, "test.json")
        d = json_load("test.json")
        self.assertEqual(result["äfdfer"], d["äfdfer"])


if __name__ == '__main__':
    unittest.main()