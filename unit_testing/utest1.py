import unittest
import main
import spelling

question_error = "What is meant by ora-00942"
question_file = "What is the meaning of listener.ora"

question_spelling_error = "Wht is ORA12542 "
question_spelling_correct = "what is ora12542 "

question_query = "What is meant by ora-00942"


class ValidateQuestionTest(unittest.TestCase):

    def test_for_has_a_number(self):
        self.assertTrue(main.has_numbers(question_spelling_correct),"checking for numbers in question")

    def test_of_error_code(self):
        self.assertTrue(main.regex_for_error_code.search(question_error), "checking error code in question")

    def test_of_file_name(self):
        self.assertTrue(main.regex_for_oracle_file.search(question_file), "checking file name in question")


class SpellingMistakesCheck(unittest.TestCase):

    def test_of_spelling(self):
        question = ""

        word_list = question_spelling_error.lower().split()

        for word in word_list:
            question += spelling.correct(word) + " "

        print question

        self.assertEqual(question, question_spelling_correct, "checking spelling mistakes")

