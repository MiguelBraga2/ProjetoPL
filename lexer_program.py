from lex_parser import lexer

data = """
a: .class ola:
a: a: p ola
"""

lexer.input(data)

for tok in lexer:
    print(tok)