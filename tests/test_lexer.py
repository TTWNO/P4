# As of right now all tests can be run by either one of the following commands in the terminal:
# python -m unittest discover -s ./tests -p test_*.py
# python -m unittest discover -s tests

from unittest import TestCase

from Token import Token
from lexer import Lexer

class TestLexer(TestCase):
    def setUp(self):
        self.lexer = Lexer("Test")

    def tearDown(self):
        self.lexer = None

    def test_lexer_should_exist(self):
        self.lexer = Lexer("Test")
        self.assertEqual(self.lexer.input_string, "Test")
        self.assertEqual(self.lexer.position.index, 0)
        self.assertEqual(self.lexer.position.row, 0)
        self.assertEqual(self.lexer.position.column, 0)
        self.assertEqual(self.lexer.current_character, 'T')

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

    def test_tokenize_should_return_correct_token_list(self):
        lexer = Lexer("x is 42+3.14")
        tokens = lexer.tokenize()
        expected_tokens = [Token("ID", "x"), Token("WS"), Token("ASSIGN"),
                           Token("WS"), Token("INT", 42), Token("PLUS"),
                           Token("FLOAT", 3.14)]
        self.assertEqual(tokens, expected_tokens)

    def test_peeked_word_ahead_should_be_Batman(self):
        self.lexer = Lexer(" Batman")
        self.assertEqual(self.lexer.peek_word_ahead(), "Batman")

    def test_digit_tokenize_should_return_integer_42_token(self):
        self.lexer = Lexer("42")
        token = self.lexer.digit_tokenize()
        self.assertEqual(token.type, "INT")
        self.assertEqual(token.value, 42)

    def test_digit_tokenize_should_return_float_3_14_token(self):
        self.lexer = Lexer("3.14")
        token = self.lexer.digit_tokenize()
        self.assertEqual(token.type, "FLOAT")
        self.assertEqual(token.value, 3.14)

    def test_escape_character_token_should_be_newline(self):
        self.lexer = Lexer('\n')
        token = self.lexer.escape_tokenize()
        self.assertEqual(token.type, "NL")
        self.assertEqual(token.value, None)

    def test_token_should_be_assignment(self):
        self.lexer = Lexer("is")
        token = self.lexer.keyword_tokenize()
        self.assertEqual(token.type, "ASSIGN")
        self.assertEqual(token.value, None)

    def test_token_should_be_cell_R2(self):
        self.lexer = Lexer("cell R2")
        token = self.lexer.keyword_tokenize()
        self.assertEqual(token.type, "CELL")
        self.assertEqual(token.value, "R2")

    def test_cell_value_should_be_D2(self):
        self.lexer = Lexer(" D2")
        token = self.lexer.handle_excel_cell()
        self.assertEqual(token.type, "CELL")
        self.assertEqual(token.value, "D2")

    def test_token_should_be_return_keyword(self):
        self.lexer = Lexer("return")
        token = self.lexer.keyword_tokenize()
        self.assertEqual(token.type, "KW")
        self.assertEqual(token.value, "return")

    def test_token_should_be_identifier(self):
        self.lexer = Lexer("myVariable")
        token = self.lexer.keyword_tokenize()
        self.assertEqual(token.type, "ID")
        self.assertEqual(token.value, "myVariable")

    def test_token_should_be_string(self):
        self.lexer = Lexer('"Beam me up, Scotty!"')
        token = self.lexer.string_tokenize()
        self.assertEqual(token.type, "STR")
        self.assertEqual(token.value, '"Beam me up, Scotty!"')

    def test_token_should_be_greater_than_or_equal_to(self):
        self.lexer = Lexer("is greater than or equal to")
        token = self.lexer.keyword_tokenize()
        self.assertEqual(token.type, ">=")
        self.assertEqual(token.value, None)

    def test_multi_word_operator_should_be_equal_to(self):
        token = self.lexer.handle_multi_word_operator("is equal to")
        self.assertEqual(token.type, "==")
        self.assertEqual(token.value, None)

    def test_multi_word_operator_should_be_illegal(self):
        with self.assertRaises(SystemExit):
            self.lexer.handle_multi_word_operator("is ekual to")

    def test_character_should_be_illegal(self):
        self.lexer = Lexer("?")
        with self.assertRaises(SystemExit):
            self.lexer.tokenize()