from yacc_parser import parser

data = """
<ul>
<li>
<p>Ola Mundo!</p>
</li>
</ul>
<p>Fora da lista</p>
"""

if data[-1] != '\n':
    data += '\n'

tree = parser.parse(data)
html = tree.to_html()
html = html[1:]


print(html,end='')
