from lex_parser import lexer

data = """
- var friends = 0
case friends
  when 0
  when 1
    p you have very few friends
  default
    p you have #{friends} friends
"""

lexer.input(data)

for tok in lexer:
    print(tok)