from typing import List
import re
from .token import Token
from .token_type import TokenType

_keywords = {'and': 'AND', 'or': 'OR', 'not': 'NOT'}
_token_specification = [
    ('REAL', r'\d+\.\d*'),
    ('INT', r'\d+'),
    ('LPAR', r'\('),
    ('RPAR', r'\)'),
    ('LE',   r'\<='),
    ('LT',   r'\<'),
    ('EQ',  r'='),
    ('GE', r'\>='),
    ('GT', r'\>'),
    ('WORD', r'[\_\-A-Za-z][\_\-0-9A-Za-z]*'),
    ('STAR', r'\*'),
    ('EOT', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('INVALID', r'.')
    ]
_tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in _token_specification)


class Scanner:

    def __init__(self, code):
        self.code = str.strip(code)
        self.tokenlist: List[Token] = []
        self._tokenize()

    def _tokenize(self):
        line_start = 0
        column = 0
        for mo in re.finditer(_tok_regex, self.code):
            kind = TokenType[mo.lastgroup]
            value = mo.group()
            column = mo.start() - line_start
            match kind:
                case TokenType.REAL:
                    value = float(value)
                case TokenType.INT:
                    value = int(value)
                case TokenType.WORD:
                    if value in _keywords.keys():
                        kind = TokenType[_keywords[value]]
                    value = 0
                case TokenType.EOT:
                    line_start = mo.end()
                case TokenType.SKIP:
                    continue
                case TokenType.INVALID:
                    raise RuntimeError(f'{value!r} unexpected on column {column+1}')
            self.tokenlist.append(Token(mo.group(), kind, value))

        self.tokenlist.append(Token('', TokenType.EOT,))
