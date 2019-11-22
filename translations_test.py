import unittest
import translations
from translations import Transform, transforms_from_string


class TestTranslate(unittest.TestCase):
    def testTransforms(self):
        x = [Transform(from_lang ='en', to_lang='es'), Transform(from_lang='ca',to_lang='fy')]
        self.assertEqual(x, transforms_from_string('[ [en, es] [ca, fy] ]')[0])
    def testIgnoresExtra(self):
        x = [Transform(from_lang ='en', to_lang='es'), Transform(from_lang='ca',to_lang='fy')]
        res = transforms_from_string('[ [en, es] [ca, fy] ] ijdoiWJAOIjdoiwajiodjwaoijdwoiajdoiwajoi')
        self.assertEqual(x, res[0])
        self.assertEqual(" ijdoiWJAOIjdoiwajiodjwaoijdwoiajdoiwajoi", res[1])

if __name__ == '__main__':
    unittest.main()
