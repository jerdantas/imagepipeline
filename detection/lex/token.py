from .token_type import TokenType


class Token:
    """
    Represents a token recognized by Lexical Analyzer
    """
    def __init__(
            self,
            text: str,
            token_type: TokenType,
            value = 0
    ):
        self.text = text
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f'Token: Text: {self.text}, type: {self.token_type.name}, value: {self.value}'
