from lex_parser import lexer

data = """
<!--[if IE 8]>
<html lang="en" class="lt-ie9">
<![endif]-->
<!--[if gt IE 8]><!-->
<html lang="en">
<!--<![endif]-->

body
  p Supporting old web browsers is a pain.

</html>
"""

lexer.input(data)

for tok in lexer:
    print(tok)