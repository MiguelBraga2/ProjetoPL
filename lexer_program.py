from lex_parser import lexer

data = """
nav#navbar-default
  .container-fluid
    h1.navbar-header My Website!
"""

lexer.input(data)

for tok in lexer:
    print(tok)