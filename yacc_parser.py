import ply.yacc as yacc
from lex_parser import tokens
from tree import Tree, context


def p_lines(p):
    """
    lines : lines line
          | line
    """

    if len(p) == 3:
        p[0] = p[1].addSubTree(p[2])
    else:
        p[0] = Tree('tags', '', p[1])

def p_line(p):
    """
    line : tagline
         | JSCODE
         | COMMENT
    """
    if type(p[1]) == list:
        p[0] = p[1]
    elif p[1].startswith('//'):
        p[0] = [ Tree('COMMENT', p[1], []) ]
    else:
        context.execute(p[1]) 
        p[0] = []

def p_tagline(p):
    """
    tagline : tag content INDENT lines DEDENT 
            | tag INDENT lines DEDENT 
            | tag content 
            | tag BAR
            | tag
    """
    if len(p) == 6:
        p[0] = p[1] + p[2] + [Tree('INDENT', p[3], []), p[4], Tree('DEDENT', p[5], [])]
    elif len(p) == 5:
        p[0] = p[1] + [Tree('INDENT', p[2], []), p[3], Tree('DEDENT', p[4], [])]
    elif len(p) == 3: 
        if p[2] != '/':
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1] + [Tree('BAR', p[2], [])]
    else:
        p[0] = p[1]

def p_tag(p):
    """
    tag : class_id_attributes LPAREN pug_attributes RPAREN 
        | TAG attributes 
        | class_id_attributes
        | TAG
    """
    if len(p) == 5:
        p[0] = p[1] + p[3]
    elif len(p) == 3:
        p[0] = [ Tree('TAG', p[1], []) ] + p[2]
    elif type(p[1]) == list:
        p[0] = p[1]
    else:
        p[0] = [ Tree('TAG', p[1], []) ]

def p_attributes(p):
    """
    attributes : class_id_attributes LPAREN pug_attributes RPAREN 
               | LPAREN pug_attributes RPAREN
               | class_id_attributes
    """
    if len(p) == 5:
        p[0] = p[1] + p[3] # parêntesis não precisos
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_class_id_attributes(p):
    """
    class_id_attributes : class ID CLASS
                        | class ID 
                        | ID class
                        | ID
                        | class
    """
    if len(p) == 4:
        p[0] = p[1] + [ Tree('ID', p[2], []), Tree('CLASS', p[3], []) ]
    elif len(p) == 3:
        if type(p[1]) == list:
            p[0] = p[1] + [Tree('ID', p[2], [])] 
        else:
            p[0] = [Tree('ID', p[1], [])] + p[2]
    else:
        if type(p[1]) == list:
            p[0] = p[1] 
        else:
            p[0] = [Tree('ID', p[1], [])] 
        

def p_class(p):
    """           
    class : class CLASS 
          | CLASS
    """
    if len(p) == 3:
        p[0] = p[1] + [ Tree('CLASS', p[2], []) ]
    else:
        p[0] = [ Tree('CLASS', p[1], []) ]


def p_pug_attributes(p):
    """
    pug_attributes : pug_attributes COMMA pug_attribute
                   | pug_attributes pug_attribute
                   | pug_attribute
    """
    if len(p) == 4:
        p[0] = p[1] + p[3]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]


def p_pug_attribute(p):
    """               
    pug_attribute : ATTRIBUTENAME EQUALS attribute_value
    """
    p[0] = [ Tree('ATTRIBUTENAME', p[1], []), Tree('EQUALS', p[2], []) ] + p[3]


def p_attribute_value(p):
    """
    attribute_value : STRING
                    | BOOLEAN
                    | NUMBER
    """
    if p[1][0] == '"':
        p[0] = [Tree('STRING', p[1], []) ]
    elif p[1] == 'true' or p[1] == 'false' :
        p[0] = [Tree('BOOLEAN', p[1], []) ]
    else:
        p[0] = [Tree('NUMBER', p[1], []) ]


def p_content(p):
    """           
    content : EQUALS interpolation
            | text
    """
    if len(p) == 3:
        p[0] = [Tree('EQUALS', p[1], []), p[2]] 
    elif len(p) == 2:
        p[0] = p[1]

def p_interpolation(p):
    """
    interpolation : STRING
                  | IDENTIFIER
                  | NUMBER
    """
    if p[1][0] == '"':
        p[0] = Tree('STRING', p[1], [])
    elif p[1][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        p[0] = Tree('NUMBER', p[1], [])
    else:
        p[0] = Tree('IDENTIFIER', context.eval(p[1]), [])
    

def p_text(p):
    """
    text : text BEGININTERP interpolation ENDINTERP
         | text TEXT
         | BEGININTERP interpolation ENDINTERP
         | TEXT
    """
    if len(p) == 5:
        p[0] = p[1] + [Tree('BEGININTERP', p[2], []), p[3], Tree('ENDINTERP', p[4], [])]
    elif len(p) == 4:
        p[0] = [Tree('BEGININTERP', p[1], []), p[2], Tree('ENDINTERP', p[3], [])]
    elif len(p) == 3:
        p[0] = p[1] + [ Tree('TEXT', p[2], []) ]
    else:
        p[0] = [ Tree('TEXT', p[1], []) ]

def p_error(p):
    print("Erro sintático")


parser = yacc.yacc(debug=True)

data = """
- var ola = "jose"

ul
  ul.class#id.class2
    li 1
  li(attr=1) 2
  li #{ola}! Tudo bem #{ola}?
  li= ola
  li 
""" 

tree = parser.parse(data)

print(tree.to_html())

  
