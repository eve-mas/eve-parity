# ------------------------------------------------------------
# 
#   SRML parser for Rational Verification
# 
# ------------------------------------------------------------
import sys
sys.path.insert(0, "../../")
import ply.lex as lex
import ply.yacc as yacc
import copy
from srmlutil import *

# List of token names.   This is always required
tokens = (
   'COMMENT',
   'MODULE',
   'CONTROL',
   'INIT',
   'UPDATE',
   'COMMA',
   'DCOL',
   'ASSIGN',
   'TRUE',
   'FALSE',
   'EQUALS',
   'NEXT',
   'SEMICOLON',
   'GOAL',
   'AND',
   'OR',
   'IMPLIES',
   'IFF',
   'NOT',
   'LB',
   'G',
   'F',
   'X',
   'U',
   'RB',
   'NAME',
   'GUARD',
   'ENVIRONMENT',
   'PROPF'
)

# Regular expression rules for simple tokens
t_LB  = r'\('
t_RB  = r'\)'
t_COMMA = r','
t_DCOL = r'::'
t_ASSIGN = r'~>'
t_EQUALS = r':='
t_NEXT = r"'"
t_SEMICOLON = r';'
t_IMPLIES = r'->'
t_IFF = r'<->'
t_NOT = r'!'

RESERVED = {
    "module":"MODULE",
    "controls":"CONTROL",
    "init":"INIT",
    "update":"UPDATE",
    "true":"TRUE",
    "false":"FALSE",
    "goal":"GOAL",
    "and":"AND",
    # "&&" : "AND",
    "or":"OR",
    "G":"G",
    # "[]":"G",
    "F":"F",
    "X":"X",
    "U":"U",
    "guard":"GUARD",
    "environment": "ENVIRONMENT",
    "property": "PROPF"

}

precedence = (
    ('left', 'IMPLIES', 'IFF'),
    ('left', 'OR', 'AND'),
    ('right', 'NOT'),
)


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = RESERVED.get(t.value, "NAME")
    return t

def t_COMMENT(t):
    r'\--.*'
    pass
    # No return value. Token discarded    

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\r'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Give the lexer some input
#lexer.input(open('coba').read())

# Tokenize
#while True:
#    tok = lexer.token()
#    if not tok: 
#        break      # No more input
#    print(tok)

modules=[]
controlledVariables=[]
initValues={}
initCommands=[] 
guardExpression=[]
updateCommands={}
guardFormula={}
updateFormula={}
updateExpression=[]
environment=[]
goalFormula=[]
alphabets=[]
propFormula=[]
PFAlphabets=[]


def p_input_1(p):
    ''' input : MODULE NAME CONTROL var_y INIT init_y UPDATE update_y GOAL goal_form'''
#    print(p[2])
#    print (controlledVariables)
    modules.append({1:{p[2]},2:set(controlledVariables),3:{str(initCommands)},4:{str(updateCommands)},5:{p[10]},6:set(alphabets)})
    del controlledVariables[:]
    initValues.clear()
    del initCommands[:]
    del guardExpression[:]
    guardFormula.clear()
    updateCommands.clear()
    updateFormula.clear()
    del alphabets[:]

#def p_input_2(p):
#    '''input : MODULE NAME CONTROL var_y INIT init_y UPDATE update_y GOALS goal_form'''
##    print(p[2])
#    modules.append({1:{p[2]},2:set(controlledVariables),3:{str(initCommands)},4:{str(updateCommands)}})
#    del controlledVariables[:]
#    initValues.clear()
#    del initCommands[:]
#    del guardExpression[:]
#    guardFormula.clear()
#    updateCommands.clear()
#    updateFormula.clear()

def p_input_2(p):
    '''input : MODULE ENVIRONMENT CONTROL var_y INIT init_y UPDATE update_y'''
#    print(p[2])
    environment.append({1:{p[2]},2:set(controlledVariables),3:{str(initCommands)},4:{str(updateCommands)}})
    del controlledVariables[:]
    initValues.clear()
    del initCommands[:]
    del guardExpression[:]
    guardFormula.clear()
    updateCommands.clear()
    updateFormula.clear()
    
def p_input_3(p):
    '''input : input input '''

def p_input_4(p):
    '''input : input PROPF prop_form '''
#    print "property: "+p[3]
    propFormula.append(p[3])
#    print alphabets
    PFAlphabets.append(alphabets)
    
################# CONTROLLED VARS ######################################
def p_var_y_1(p):
    '''var_y : NAME'''
#    print(p[1])
    controlledVariables.append(p[1])
()
def p_var_y_2(p):
    '''var_y : var_y COMMA var_y'''
()
    
################ INIT COMMANDS #########################################

def p_init_y_1(p):
    '''init_y : DCOL init_command
                | init_y DCOL init_command'''
#    print (initValues)
    temp={}
    for key,value in initValues.items():
#        print (key,value)
        temp[key]=value
#        if i:
#            print 'benar'
#        else:
#            print 'salah'
    initCommands.append({str(temp)})
    temp.clear()
#    print (initCommands)
    initValues.clear()
    
    
def p_init_command_1(p):
    '''init_command : init_condition ASSIGN init_next_state'''
    
def p_init_condition_1(p):
    '''init_condition : TRUE'''

#def p_init_condition_2(p):
#    '''init_condition : FALSE'''
    
def p_init_next_state_1(p):
    '''init_next_state : NAME NEXT EQUALS TRUE'''
#    print ('true: '+p[1])
    initValues[p[1]]=True

def p_init_next_state_2(p):
    '''init_next_state : NAME NEXT EQUALS FALSE'''
#    print ('false: '+p[1])
    initValues[p[1]]=False


def p_init_next_state_3(p):
    '''init_next_state : init_next_state COMMA init_next_state'''

def p_init_next_state_4(p):
    '''init_next_state : init_next_state SEMICOLON'''

################ UPDATE COMMANDS #########################################
    
def p_update_command_1(p):
    '''update_command : update_condition ASSIGN update_next_state'''
#    print (guardExpression)
#    for g in guardExpression:
    guardFormula[len(guardFormula)]=copy.copy(guardExpression)
    del guardExpression[:]

def p_update_y_1(p):
    '''update_y : DCOL update_command
                | update_y DCOL update_command'''
#    for key,value in guardFormula.items():
#        updateCommands[key]={'guard':value}
#        print key
#        print ('UPFOR', updateFormula)
#        updateCommands[key]=merge_two_dicts(updateCommands[key],updateFormula)
#    updateCommands.clear()
    updateCommands[len(guardFormula)-1]={'guard':guardFormula[len(guardFormula)-1]}
    updateCommands[len(guardFormula)-1]=merge_two_dicts(updateCommands[len(guardFormula)-1],updateFormula)
    updateFormula.clear()

#def p_update_y_2(p):
#    '''update_y : update_y DCOL update_command'''
#    for key,value in guardFormula.items():
#            updateCommands['guard']=value
#    updateCommands.clear()
    
def p_update_condition_1(p):
    '''update_condition : formula_guard'''
()
def p_update_condition_2(p):
    '''update_condition : update_condition COMMA update_condition'''
    
################ GUARD FORMULA ########################################
    
def p_formula_guard_1(p):
    '''formula_guard : NAME'''
#    print (p[1])
    guardExpression.append(p[1])
()
def p_formula_guard_2(p):
    '''formula_guard : TRUE'''
#    print (p[1])
    guardExpression.append(p[1])

()
def p_formula_guard_3(p):
    '''formula_guard : FALSE'''
#    print (p[1])
    guardExpression.append(p[1])

()
def p_formula_guard_4(p):
    '''formula_guard : formula_guard OR formula_guard'''
#    print (p[2])
    guardExpression.append(p[2])
()
def p_formula_guard_5(p):
    '''formula_guard : formula_guard AND formula_guard'''
#    print (p[2])
    guardExpression.append(p[2])
()
def p_formula_guard_6(p):
    '''formula_guard : formula_guard IMPLIES formula_guard'''
#    print (p[2])
    guardExpression.append(p[2])
()
def p_formula_guard_7(p):
    '''formula_guard : formula_guard IFF formula_guard'''
#    print (p[2])
    guardExpression.append(p[2])
()
def p_formula_guard_8(p):
    '''formula_guard : NOT formula_guard'''
#    print (p[1])
    guardExpression.append(p[1])
()
def p_formula_guard_9(p):
    '''formula_guard : LB formula_guard RB'''
#    print (p[1]+p[3])
    
################ UPDATE VARS #############################3
    
def p_update_next_state_1(p):
    '''update_next_state : NAME NEXT EQUALS formula_assign'''
#    print (p[1])
    updateFormula[p[1]]=updateExpression[:]
    del updateExpression[:]

def p_update_next_state_2(p):
    '''update_next_state : update_next_state COMMA update_next_state'''

def p_update_next_state_3(p):
    '''update_next_state : update_next_state SEMICOLON'''
    
############### ASSIGNMENT FORMULA ###########################
    
def p_formula_assign_1(p):
    '''formula_assign : NAME'''
#    print (p[1])
    updateExpression.append(p[1])

def p_formula_assign_2(p):
    '''formula_assign : TRUE'''
#    print (p[1])
    updateExpression.append(p[1])

()
def p_formula_assign_3(p):
    '''formula_assign : FALSE'''
#    print (p[1])
    updateExpression.append(p[1])

()
def p_formula_assign_4(p):
    '''formula_assign : formula_assign OR formula_assign'''
#    print (p[2])
    updateExpression.append(p[2])
()
def p_formula_assign_5(p):
    '''formula_assign : formula_assign AND formula_assign'''
#    print (p[2])
    updateExpression.append(p[2])
()
def p_formula_assign_6(p):
    '''formula_assign : formula_assign IMPLIES formula_assign'''
#    print (p[2])
    updateExpression.append(p[2])
()
def p_formula_assign_7(p):
    '''formula_assign : formula_assign IFF formula_assign'''
#    print (p[2])
    updateExpression.append(p[2])
()
def p_formula_assign_8(p):
    '''formula_assign : NOT formula_assign'''
#    print (p[1])
    updateExpression.append(p[1])
()
def p_formula_assign_9(p):
    '''formula_assign : LB formula_assign RB'''
#    print (p[1]+p[3])
    
#################### GOAL FORMULA #####################################
def p_goal_form_1(p):
    '''goal_form : DCOL gf SEMICOLON'''
    p[0]=p[2]
()
#def p_goal_form_2(p):
#    '''goal_form : goal_form gf'''
    
def p_gf_1(p):
    '''gf : NAME'''
    p[0]=p[1]
#    print p[1]
    alphabets.append(p[1])
()
def p_gf_2(p):
    '''gf : TRUE'''
    p[0]="true"
()
def p_gf_3(p):
    '''gf : FALSE'''
    p[0]="false"
()
def p_gf_4(p):
    '''gf : gf OR gf'''
    p[0]=p[1]+" || "+p[3]
()
def p_gf_5(p):
    '''gf : gf AND gf'''
    p[0]=p[1]+" && "+p[3]
()
def p_gf_6(p):
    '''gf : gf IMPLIES gf'''
    p[0]=p[1]+" -> "+p[3]
    
()
def p_gf_7(p):
    '''gf : gf IFF gf'''
    p[0]=p[1]+" <-> "+p[3]
()
def p_gf_8(p):
    '''gf : G gf'''
    p[0]=" [] "+p[2]
()
def p_gf_9(p):
    '''gf : F gf'''
    p[0]=" <> "+p[2]
()
def p_gf_10(p):
    '''gf : X gf'''
    p[0]=" X "+p[2]
()
def p_gf_11(p):
    '''gf : gf U gf'''
    p[0]=p[1]+" U "+p[3]
()
def p_gf_12(p):
    '''gf : NOT gf'''
    p[0]=" ! "+p[2]
()
def p_gf_13(p):
    '''gf : LB gf RB'''
    p[0]=" ( "+p[2]+" ) "
 
   
'''
formula/property to be checked in E/A-Nash
'''
def p_prop_form_1(p):
    '''prop_form : DCOL pf SEMICOLON'''
    p[0]=p[2]
    # print 'ALPHA>>>',alphabets
()

def p_pf_1(p):
    '''pf : NAME'''
    p[0]=p[1]
#    print p[1]
    alphabets.append(p[1])
()
def p_pf_2(p):
    '''pf : TRUE'''
    p[0]="true"
()
def p_pf_3(p):
    '''pf : FALSE'''
    p[0]="false"
()
def p_pf_4(p):
    '''pf : pf OR pf'''
    p[0]=p[1]+" || "+p[3]
()
def p_pf_5(p):
    '''pf : pf AND pf'''
    p[0]=p[1]+" && "+p[3]
()
def p_pf_6(p):
    '''pf : pf IMPLIES pf'''
    p[0]=p[1]+" -> "+p[3]
    
()
def p_pf_7(p):
    '''pf : pf IFF pf'''
    p[0]=p[1]+" <-> "+p[3]
()
def p_pf_8(p):
    '''pf : G pf'''
    p[0]=" [] "+p[2]
()
def p_pf_9(p):
    '''pf : F pf'''
    p[0]=" <> "+p[2]
()
def p_pf_10(p):
    '''pf : X pf'''
    p[0]=" X "+p[2]
()
def p_pf_11(p):
    '''pf : pf U pf'''
    p[0]=p[1]+" U "+p[3]
()
def p_pf_12(p):
    '''pf : NOT pf'''
    p[0]=" ! "+p[2]
()
def p_pf_13(p):
    '''pf : LB pf RB'''
    p[0]=" ( "+p[2]+" ) "
    
###### YACC SYNTAX ERROR HANDLER ##############
#def p_error(p):
#    print ("Syntax Error: "+p.value)
#    sys.exit()


parser = yacc.yacc()


    