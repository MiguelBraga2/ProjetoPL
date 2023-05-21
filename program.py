from yacc_parser import parser

data = """
- if (1==1)
  p= 1
"""

if data[-1] != '\n':
    data += '\n'

tree = parser.parse(data)
html = tree.to_html()
html = html[1:]


print(html,end='')
