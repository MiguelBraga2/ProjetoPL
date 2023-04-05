import ply.yacc as yacc

from lexer import tokens

## incio da GIC

start = 'tagList'

'''
tagList : tag aux1

aux1 : tagList
     | 

tag : tagline aux2

aux2 : INDENT tagList
     | 

tagline : TAG aux3

aux3 : TEXT 
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
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = ""

def p_tag(p):
    '''
    tag : tagline aux2
    '''
    p[0] = p[1] + "\n   " + p[2]

def p_aux2(p):
    '''
    aux2 : INDENT tagList
         | 
    '''
    if len(p) > 2:
        p[0] = p[3]
    else:
        p[0] = ""

def p_tagline(p):
    '''
    tagline : TAG aux3
    '''
    p[0] = "<" + p[1] + ">" + p[2] + "</" + p[1] + ">"

def p_aux3(p):
    '''
    aux3 : TEXT 
         |   
    '''
    if len(p) > 1:
        p[0] = p[1]
    else:
        p[0] = ""


###inicio do parsing
parser = yacc.yacc(start='tagList')
r = parser.parse('''
ul
li''')
print(r)
    
  

###inicio do parsing
#parser = yacc.yacc()
#parser.success = True
#fonte = ""
#for line in sys.stdin:
#    fonte += line   
#parser.parse(fonte)

