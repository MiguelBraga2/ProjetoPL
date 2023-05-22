from yacc_parser import parser

data = """
- for (var x = 0; x < 3; x++)
  li item
"""

if data[-1] != '\n':
    data += '\n'

tree = parser.parse(data)
html = tree.to_html()
html = html[1:]


print(html,end='')
