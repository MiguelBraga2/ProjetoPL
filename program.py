from yacc_parser import parser
import sys

data = """
"""

for line in sys.stdin:
 data += line

if data[-1] != '\n':
    data += '\n'

tree = parser.parse(data)
html = tree.to_html()
html = html.lstrip()


print(html,end='')
