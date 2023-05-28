from lex_parser import lexer

data = """
- for(let i=0; i<100; i++)
    - for(let j=0; j<2; j++)
        p= 2*i + j
"""

lexer.input(data)

for tok in lexer:
    print(tok)