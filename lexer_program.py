from lex_parser import lexer

data = """
- var x = 1
  li= x
"""

lexer.input(data)

for tok in lexer:
    print(tok)