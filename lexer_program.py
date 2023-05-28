from lex_parser import lexer

data = """
div
  p This text belongs to the paragraph tag.
  br
  .
    This text belongs to the div tag.
"""

lexer.input(data)

for tok in lexer:
    print(tok)