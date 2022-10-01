# -----------------------------------------------------------------------------
# json_dic.py
#
# A simple json to python dictionary converter -- all in one file.
# -----------------------------------------------------------------------------
import sys
import json
tokens = (
    'LCURLYBRACKET','NUMBER','FLOAT', 'ID', 'COMMA', 'SEPA',
    'RCURLYBRACKET','LBRACKET','RBRACKET', 'TRUE', 'FALSE', 'NULL'
    )

# Tokens
t_LCURLYBRACKET = r'\{'
t_RCURLYBRACKET = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_COMMA = r'\,'
t_SEPA = r':'

def t_TRUE(t):
    r'true'
    t.value = True
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t

def t_NULL(t):
    r'null'
    t.value = None
    return t

def t_FLOAT(t):
    r'[+-]?[0-9]+\.[0-9]+[e]?[0-9]+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_NUMBER(t):
    r'[-]?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'\"(\\.|[^"\\])*\"'
    try:
        print(t.value)
        t.value = str(t.value)[1:-1].encode().decode('unicode_escape')
    except ValueError:
        print("Not string %d", t.value)
        t.value = ""
    return t

# Ignored characters
t_ignore = " \t\r\f\v"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

dic ={}

# dictionary of names
names = { }

def p_state_start(t):
    '''start : json 
             | arraylist'''
    print(t[1])

def p_state_json(t):
    '''json : LCURLYBRACKET keyvalues RCURLYBRACKET
            | LCURLYBRACKET RCURLYBRACKET'''
    #print("json :")
    t[0] = t[2]

def p_state_keyvalues(t):
    '''keyvalues : keyvalues COMMA keyvalue 
                 | keyvalue'''
    #print("keyvalues :")
    c = {}
    for v in t:
        if type(v) is dict:
            c.update(v)
    
    t[0] = c

def p_state_keyvalue(t):
    'keyvalue : key SEPA value'
    #print("keyvalue :")
    t[0] = {t[1]:t[3]}

def p_state_key(t):
    '''key : ID
           | NUMBER'''
    #print("key :")
    t[0] = t[1]

def p_state_value(t):
    '''value : ID
           | NUMBER
           | FLOAT
           | TRUE
           | FALSE
           | NULL
           | arraylist
           | json'''
    #print("value :")
    t[0] = t[1]

def p_state_arraylist(t):
    '''arraylist : LBRACKET array RBRACKET
                 | LBRACKET RBRACKET'''
    if len(t) == 4:
        t[0] = t[2]
    elif len(t) == 3:
        t[0] = list()

def p_state_array(t):
    '''array : array COMMA value
             | value '''
    c = list()

    if len(t) == 2:
        if type(t[1]) is list:
            c.extend(t[1])
        elif t[1]!= None :
            c.append(t[1])
    elif len(t) == 4:     
        if type(t[1]) is list:
            c.extend(t[1])
        elif t[1]!= None :
            c.append(t[1])  
        if type(t[3]) is list:
            c.extend(t[3])
        elif t[3] != None :
            c.append(t[3])       
    t[0] = c

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = ""
        for line in sys.stdin:
            stripped = line.strip()
            if not stripped: break
            s = s + stripped

        print(json.loads(s))
        print("-------------------- MAGIC TEXT ---------------------")
    except EOFError:
        break
    parser.parse(s)
    break