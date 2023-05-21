from yacc_parser import parser

data = """
each x in [1,2,3]
  li= x
"""

if data[-1] != '\n':
    data += '\n'

tree = parser.parse(data)
html = tree.to_html()
html = html[1:]


print(html,end='')
