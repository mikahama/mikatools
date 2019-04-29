#encoding: utf-8
import unittest
from mikatools import *


class TestFSTS(unittest.TestCase):

    def setUp(self):
        pass

    def test_lemmatize(self):
        result = uralicApi.lemmatize("lehmäni", "fin",force_local=True)
        self.assertEqual(result[0], 'lehmä')


if __name__ == '__main__':
    unittest.main()