import langdetect
import nltk
import re
import json
import codecs

nltk.download('words')
from nltk.corpus import words as nltk_words


dictionary = dict.fromkeys(nltk_words.words(), None)

def check_if_word_in_eng_dict(word):
    # creation of this dictionary would be done outside of
    #     the function because you only need to do it once.

    try:
        x = dictionary[word]
        return True
    except KeyError:
        return False

class EnglishDetector:
    def __init__(self):
        #self._enchant_english_detector = enchant.Dict("en_US")
        self._min_length_for_lang_detect = 500  # lang detect fails if the string is not long enough
        self._threshold_for_enchant = 0.60
        self._lang_detect_code_english = 'en'
    def remove_special_characters(self, s):
        # removes all except alphanumeric characters and spaces
        return re.sub('[^ A-Za-z]+', '', s)
    def is_english(self, input_text: str):
        text = self.remove_special_characters(input_text)
        text_length = len(text)
        if text_length > self._min_length_for_lang_detect:
            lang_probabilities = langdetect.detect_langs(text)
            for prob in lang_probabilities:
                if prob.lang == self._lang_detect_code_english:
                    print(f'Probability of English : {prob.prob}')
                    if prob.prob > self._threshold_for_enchant:
                        return True
            return False
        # cannot use lang detect as the text is not long enough
        # hence detecting the number of english words and non english words and taking a ratio of that
        else:
            words = text.split()
            english_words = [word for word in words if check_if_word_in_eng_dict(word)]
            #english_words = [word for word in words if self._enchant_english_detector.check(word)]
            print(f"ratio of english:total is {len(english_words)/len(words)}")
            if len(english_words)/len(words) >= self._threshold_for_enchant:
                return True
            return False

if __name__ == "__main__":
    pass