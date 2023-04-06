import ply.yacc as yacc

from lex_parser import tokens

## incio da GIC

start = 'tagList'

'''
tagList : tag aux1

aux1 : tagList
     |

tag : TAG aux2

aux2 : TEXT INDENT tagList DEDENT
     | INDENT tagList DEDENT
     | TEXT DEDENT
     | DEDENT
     |

'''

def p_tagList(p):
    '''
    tagList : tag aux1
    '''
    p[0] = p[1] + p[2]
    
def p_aux1(p):
    '''
    aux1 : tagList
         |
    '''
    if len(p) > 1:
        p[0] = p[1]
    else:
        p[0] = ""

def p_tag(p):
    '''
    tag : TAG aux2
    '''
    p[0] = "<" + p[1] + ">" + p[2] + "</" + p[1] + ">\n"

def p_aux2(p):
    '''
    aux2 : TEXT INDENT tagList DEDENT
         | INDENT tagList DEDENT
         | TEXT
         |
    '''
    if len(p) > 4:
        p[0] = p[1] + p[2] + p[3] + p[4]
    elif len(p) > 3:
        p[0] = p[1] + p[2] + p[3]  
    elif len(p) > 1:
        p[0] = p[1]
    else:
        p[0] = ""


###inicio do parsing
parser = yacc.yacc(start='tagList')

data =  '''
ul
  li OLAAAAAAA
  li manos
  li xau
'''

r = parser.parse(data)
                 
print(r)
    
  

###inicio do parsing
#parser = yacc.yacc()
#parser.success = True
#fonte = ""
#for line in sys.stdin:
#    fonte += line   
#parser.parse(fonte)

