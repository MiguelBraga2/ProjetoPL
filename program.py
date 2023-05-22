from yacc_parser import parser

data = """
ul
  each val, key in {1: 'one', 2: 'two', 3: 'three'}
    li= key + ': ' + val
"""

if data[-1] != '\n':
    data += '\n'

tree = parser.parse(data)
html = tree.to_html()
html = html[1:]


print(html,end='')
