from lex_parser import lexer

data = """
a(style={color: 'red', background: 'green'})
"""

lexer.input(data)

for tok in lexer:
    print(tok)