from lex_parser import lexer

data = """
a #[p #[.class(attr=1) ola #{"ola"}]]
"""

lexer.input(data)

for tok in lexer:
    print(tok)