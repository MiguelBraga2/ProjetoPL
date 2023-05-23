from yacc_parser import parser
import sys

data = """
a #[p #[.class(attr=1) ola #{"ola"}]]
""" 

#for line in sys.stdin:
#  data += line

if data[-1] != '\n':
    data += '\n'

tree = parser.parse(data)
html = tree.to_html()
html = html[1:]


print(html,end='')
