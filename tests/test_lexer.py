# As of right now all tests can be run by either one of the following commands in the terminal:
# python -m unittest discover -s ./tests -p test_*.py
# python -m unittest discover -s tests

import unittest
from unittest import TestCase

import lexer
from lexer import Lexer

class TestLexer(TestCase):
    def setUp(self):
        self.lexer = Lexer("Test")

    def tearDown(self):
        self.lexer = None

    def test_current_character_in_focus_should_be_T(self):
        self.assertEqual(self.lexer.current_character, 'T')

    def test_peeked_character_should_be_e(self):
        self.assertEqual(self.lexer.peek(), 'e')

    def test_next_character_in_focus_should_be_s(self):
        self.lexer.next_character()
        self.lexer.next_character()
        self.assertEqual(self.lexer.current_character, 's')

    def test_advance_3_characters_should_be_t(self):
        self.lexer.advance_n(3)
        self.assertEqual(self.lexer.current_character, 't')

    def test_peeked_word_ahead_should_be_Batman(self):
        self.lexer = Lexer(" Batman")
        self.assertEqual(self.lexer.peek_word_ahead(), "Batman")

    def test_digit_tokenize_should_return_integer_42_token(self):
        self.lexer = Lexer("42")
        token = self.lexer.digit_tokenize()
        self.assertTrue(token.type, "INTEGER")
        self.assertEqual(token.value, 42)

    def test_digit_tokenize_should_return_float_3_14_token(self):
        self.lexer = Lexer("3.14")
        token = self.lexer.digit_tokenize()
        self.assertTrue(token.type, "FLOAT")
        self.assertEqual(token.value, 3.14)

    def test_escape_character_token_should_be_newline(self):
        self.lexer = Lexer('\n')
        token = self.lexer.escape_tokenize()
        self.assertTrue(token.type, "NEWLINE")
        self.assertEqual(token.value, None)

if __name__ == '__main__':
    unittest.main()