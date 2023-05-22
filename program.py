from yacc_parser import parser

data = """
html(lang="en")
  head
    title= pageTitle
    script(type='text/javascript').
      if (foo) bar(1 + 5)
  body
    h1 Pug - node template engine
    #container.col
      if youAreUsingPug
        p You are amazing
      else
        p Get on it!
      p.
        Pug is a terse and simple templating language with a
        strong focus on performance and powerful features
"""

if data[-1] != '\n':
    data += '\n'

tree = parser.parse(data, debug=True)
html = tree.to_html()
html = html[1:]


print(html,end='')
