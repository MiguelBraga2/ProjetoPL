from lex_parser import lexer

data = """
//- will not output within markup
// will output within markup
p foo
p bar
"""

lexer.input(data)

for tok in lexer:
    print(tok)