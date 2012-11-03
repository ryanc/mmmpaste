import unittest

from mmmpaste.base62 import b62_encode, b62_decode

class TestBase62Functions(unittest.TestCase):

    def test_encode(self):
        self.assertEqual("0",  b62_encode(0))
        self.assertEqual("1",  b62_encode(1))
        self.assertEqual("a",  b62_encode(10))
        self.assertEqual("A",  b62_encode(36))
        self.assertEqual("Z",  b62_encode(61))
        self.assertEqual("1a", b62_encode(72))
        self.assertEqual("1A", b62_encode(98))
        self.assertEqual("1Z", b62_encode(123))

    def test_decode(self):
        self.assertEqual(0,   b62_decode("0"))
        self.assertEqual(1,   b62_decode("1"))
        self.assertEqual(10,  b62_decode("a"))
        self.assertEqual(36,  b62_decode("A"))
        self.assertEqual(61,  b62_decode("Z"))
        self.assertEqual(72,  b62_decode("1a"))
        self.assertEqual(98,  b62_decode("1A"))
        self.assertEqual(123, b62_decode("1Z"))

    def test_loop(self):
        for i in range(100):
            self.assertEquals(i, b62_decode(b62_encode(i)))

class TestNothing(unittest.TestCase):

    def test_nothing(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
