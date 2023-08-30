from .token import Token
from .token_type import TokenType

_alpha = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÀÂÃáàâãÉÈÊéàêÍÌíìÓÒÔÕóòôõÚÙúùÇç_-")
_digit = set("0123456789")
_ordinal = set("ºª")
_delimiter = set(" \n\r\t\'\"!#%&*()=+{[}]<><;?|@$:/")
_blank = set(" \r\t")  # also in _delimiter
_numeric_part = set(".")  # not in delimiter also comma "," should be here
_inv_token = Token('', TokenType.INVALID)


class Scan_PTBR:

    def __init__(
            self
    ):

        # Attributes
        self.fragment: str = ''  # reference to text fragment received by 'next_fragment()'
        self.token: Token = _inv_token  # Token instance returned by 'next_token()'

        # Protected

        self._length: int = 0  # length of text fragment
        self._pos: int = 0  # next character position on the text fragment
        self._c = " "  # current character being processed

    def next_fragment(self, fragment):
        self.fragment = fragment
        self.token = _inv_token
        self._length = len(self.fragment)
        self._pos = 0
        self._c = " "

    def next_token(self):
        self.token = _inv_token
        while True:
            # Ignore blanks
            self.__ignore_blanks()

            # Check end-of-text (\0) or end-of-line (\n)  -> thus a fragment has one line
            if self._c == "\0" or self._c == "\n":
                self.token = Token('', TokenType.EOT)
                return

            # WORD
            if self._c in _alpha:
                self.__get_alpha()
                if self.token.text == 'and':
                    self.token.token_type = TokenType.AND
                if self.token.text == 'or':
                    self.token.token_type = TokenType.OR
                if self.token.text == 'not':
                    self.token.token_type = TokenType.NOT
                return

            # INTEGER
            if self._c in _digit:
                return self.__get_digit()

            # DELIMITER
            if self._c in _delimiter:
                return self.__get_delimiter()

            # INVALID
            self.__truncate_invalid()

    def __ignore_blanks(self):
        while self._c in _blank:
            self.__get_char()
        return

    def __get_char(self):
        if self._pos >= self._length:
            self._c = "\0"
            return
        self._c = self.fragment[self._pos]
        self._pos += 1
        return

    def __get_alpha(self):

        # WORD -> (r'^\w+$')
        self.token.token_type = TokenType.WORD
        while self._c in _alpha or self._c in _digit:
            self.token.text += self._c
            self.__get_char()
        return

    def __get_digit(self):

        # INTEGER -> (r'^\d+$')
        self.token.token_type = TokenType.INT
        count = 0
        while self._c in _digit:
            count += 1
            self.token.text += self._c
            self.__get_char()
        if self._c in _delimiter:
            self.token.value = int(self.token.text)
            return

        # NUMBER -> (r'^\d+(\.\d*){0,1}$')
        if self._c == ".":  # '.'
            self.token.token_type = TokenType.REAL
            self.token.text += self._c
            self.__get_char()
            while self._c in _digit:
                self.token.text += self._c
                self.__get_char()
        self.token.value = float(self.token.text)
        return

    def __get_delimiter(self):
        if self._c == '<':
            self.__get_char()
            if self._c == '=':
                self.token.text = '<='
                self.token.token_type = TokenType.LE
                self.__get_char()
                return
            else:
                self.token.text = '<'
                self.token.token_type = TokenType.LT
                return
        elif self._c == '=':
            self.token.text = '='
            self.token.token_type = TokenType.EQ
            self.__get_char()
            return
        elif self._c == '>':
            self.__get_char()
            if self._c == '=':
                self.token.text = '>='
                self.token.token_type = TokenType.GE
                self.__get_char()
                return
            else:
                self.token.text = '>'
                self.token.token_type = TokenType.GT
                return
        elif self._c == '(':
            self.token.text = '('
            self.token.token_type = TokenType.LPAR
            self.__get_char()
            return
        elif self._c == ')':
            self.token.text = ')'
            self.token.token_type = TokenType.RPAR
            self.__get_char()
            return
        elif self._c == '*':
            self.token.text = '*'
            self.token.token_type = TokenType.STAR
            self.__get_char()
            return
        elif self._c == '!':
            self.__get_char()
            if self._c == '=':
                self.token.text = '!='
                self.token.token_type = TokenType.NE
                self.__get_char()
                return

        self.__truncate_invalid()  # move to the next char

    def __truncate_invalid(self):
        self.token.token_type = TokenType.INVALID
        while self._c != '\n' and self._c != '\0':
            self.token.text += self._c
            self.__get_char()
