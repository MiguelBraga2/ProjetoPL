from IndentationException import IndentationException
from yacc_parser import parser
import sys

data = """
if 1+1==2
    p ola
else if 1+1==3
    p ole
"""

#for line in sys.stdin:
#    data += line

if data[-1] != '\n':
    data += '\n'

try:
    tree = parser.parse(data)
    html = tree.to_html()
    html = html.lstrip()
    print(html, end='')
except IndentationException as ex:
    print(ex)
