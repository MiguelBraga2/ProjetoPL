from lex_parser import lexer

data = """
-
  var list = ["Uno", "Dos", "Tres",
          "Cuatro", "Cinco", "Seis"]
each item in list
  li= item
"""

lexer.input(data)

for tok in lexer:
    print(tok)