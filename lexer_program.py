from lex_parser import lexer

data = """
.class1(class="class")
.class2#id1(atta=1  class="class3 ola")
"""

lexer.input(data)

for tok in lexer:
    print(tok)