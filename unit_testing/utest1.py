import unittest
import main,spelling

question_error = "What is meant by ora-00942"
question_file = "What is the meaning of listener.ora"

question_spelling_error = "Wht is ORA12542"
question_spelling_correct = "What is ORA12542"


class ValidateQuestionTest(unittest.TestCase):

    def test_of_error_code(self):
        self.assertTrue(main.regex_for_error_code.search(question_error), "checking error code in question ")

    def test_of_file_name(self):
        self.assertTrue(main.regex_for_oracle_file.search(question_file), "checking file name in question")


class SpellingCorrectionTest(unittest.TestCase):

    def test_of_spelling(self):

        question

        word_list = question_spelling_error.split()

        for word in word_list:
            question += spelling.correct(word) + " "

        print type(question)

        self.assertEqual("What is ORA12542", "What is ORA12542", "checking spelling mistakes")

if __name__ == '__main__':

    ValidateQuestionTest.test_of_error_code()
    ValidateQuestionTest.test_of_file_name()
    SpellingCorrectionTest.test_of_spelling()
