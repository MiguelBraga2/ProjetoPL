from yacc_parser import parser

data = """
- var n = 0;
ul
  while n < 4
    li= n++
"""

if data[-1] != '\n':
    data += '\n'

tree = parser.parse(data)
html = tree.to_html()
html = html[1:]


print(html,end='')
