import unittest
from ..translation.arabic_to_english import translate_arabic_to_english

def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

class TestTranslateArabicToEnglish(unittest.TestCase):
    def test_translate_arabic_to_english(self):
        text = "مرحبا بك في العالم البرمجة"
        translation = translate_arabic_to_english(text)
        print(f"English: {translation}")
        self.assertIsInstance(translation, str)
        self.assertTrue(is_english(translation))


if __name__ == '__main__':
    unittest.main()
