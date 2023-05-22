from lex_parser import lexer

data = """
- for (var x = 0; x < 3; x++)
  li item
"""

lexer.input(data)

for tok in lexer:
    print(tok)