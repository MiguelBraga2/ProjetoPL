from lex_parser import lexer

data = """
p.
  This is a very long and boring paragraph that spans multiple lines.
  Suddenly there is a #[strong strongly worded phrase] that cannot be
  #[em ignored].
"""

lexer.input(data)

for tok in lexer:
    print(tok)