import langdetect
import re

class LanguageDetector:
    def __init__(self):
        # lang detect fails if the string is not long enough
        self._min_length_for_lang_detect = 500
        self._threshold = 0.60

    def remove_special_characters(self, s):
        return re.sub('[^ A-Za-z]+', '', s)

    def detect(self, input_text:str):
        text = self.remove_special_characters(input_text)
        text_length = len(text)

        if text_length > self._min_length_for_lang_detect:
            text = text[0:self._min_length_for_lang_detect]
            lang_probabilities = langdetect.detect_langs(text)
            for prob in lang_probabilities:
                return prob.lang

if __name__ == "__main__":
    # detect = LanguageDetector().detect("Machine learning (ML) is the scientific study of algorithms and statistical models that computer systems use to effectively perform a specific task without using explicit instructions, relying on patterns and inference instead. It is seen as a subset of artificial intelligence. Machine learning algorithms build a mathematical model based on sample data, known as \"training data\", in order to make predictions or decisions without being explicitly programmed to perform the task.[1][2]:2 Machine learning algorithms are used in a wide variety of applications, such as email filtering, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning, and focuses on exploratory data analysis through unsupervised learning.[3][4] In its application across business problems, machine learning is also referred to as predictive analytics.")
    # print(detect)
    # pass
    pass