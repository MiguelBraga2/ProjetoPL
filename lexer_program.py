from lex_parser import lexer

data = """
- var text = "ola123"
- var num = 145.5
p.
  This is a very long and boring paragraph that spans multiple lines. #{num}
  Suddenly there is a #[strong strongly worded phrase] that cannot be
  #[em ignored] #{text}.
"""

lexer.input(data)

for tok in lexer:
    print(tok)