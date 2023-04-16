import ply.yacc as yacc

from lex_parser import tokens

## incio da GIC

start = 'pug'

def p_pug(p):
    '''
    pug : comment DOCTYPE TEXT taglist
        | DOCTYPE TEXT taglist
        | taglist
    '''
    if len(p) > 4:
        p[0] = p[1] + '\n<!' + p[2] + ' ' + p[3] + '>\n' + p[4]
    elif len(p) > 3:
        p[0] = '\n<!' + p[1] + ' ' + p[2] + '>\n' + p[3]
    else:
        p[0] = p[1]    
    
def p_taglist(p):
    '''
    taglist : comment TAG TEXT INDENT taglist DEDENT taglist 
            | TAG TEXT INDENT taglist DEDENT taglist 
            | TAG INDENT taglist DEDENT taglist 
            | TAG TEXT taglist
            |
    '''
    indent = parser.indentation

    if len(p) > 7:
        p.parser.indentation = p[4]
        p[0] = p[1] + '<' + p[2] + '>' + p[3] + p[4] + p[5] + indent + '</' + p[2] + '>' + p[6] + p[7]
        p.parser.indentation = p[6]
    elif len(p) > 6:
        p.parser.indentation = p[3]
        p[0] = '<' + p[1]  + '>' + p[2][1:] + p[3] + p[4] + indent + '</' + p[1] + '>' + p[5] + p[6]
        p.parser.indentation = p[5]
    elif len(p) > 5:
        p.parser.indentation = p[2]
        p[0] = '<' + p[1]  + '>' + p[2] + p[3] + indent + '</' + p[1] + '>' + p[4] + p[5]
        p.parser.indentation = p[4]
    elif len(p) > 3:
        p[0] =  '<' + p[1] + '>' + p[2][1:] + '</' + p[1] + '>' + indent + p[3]
    else:
        p[0] = ''

def p_comment(p):
    '''
    comment : COMMENT
    '''
    pass

def p_tagparams(p):
    '''
    tagparams : CLASS ID ATTRIBUTE 
        | CLASS ATTRIBUTE ID  
        | ATTRIBUTE CLASS ID  
        | ATTRIBUTE ID CLASS
        | ID ATTRIBUTE CLASS  
        | ID CLASS ATTRIBUTE
        | CLASS ATTRIBUTE  
        | ATTRIBUTE CLASS  
        | ATTRIBUTE ID  
        | ID ATTRIBUTE 
        | CLASS ID  
        | ID CLASS 
    ''' 
    if len(p) > 3:
        pass
    elif len(p) > 2:
        pass



###inicio do parsing
parser = yacc.yacc(start='pug')
parser.indentation = ''

data =  '''
ul
  li OLAAAAAAA
    li ola
ul
  li massa
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

