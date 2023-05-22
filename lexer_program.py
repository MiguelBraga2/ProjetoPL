from lex_parser import lexer

data = """
// just some paragraphs
       ola manos
#id foo
#ola bar
"""

lexer.input(data)

for tok in lexer:
    print(tok)