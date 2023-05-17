from yacc_parser import parser


data = """
- var ref = 'google.com'
ul(href=ref)
  li 1
  li 2
  li 3
"""

if data[-1] != '\n':
    data += '\n'


tree = parser.parse(data)
html = tree.to_html()
html = html[1:]



print(html,end='')
