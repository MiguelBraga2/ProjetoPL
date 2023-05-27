from yacc_parser import parser
import sys

data = """
p.
  This is a very long and boring paragraph that spans multiple lines.
  Suddenly there is a #[strong strongly worded phrase] that cannot be
  #[em ignored].
"""

#for line in sys.stdin:
# data += line

if data[-1] != '\n':
    data += '\n'

tree = parser.parse(data)
html = tree.to_html()
html = html.lstrip()


print(html,end='')
