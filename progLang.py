#scanner
tokens = ('STR', 'CLASSNAME', 'MAKECLASS', 'SUBCLASS',
    'CONCAT', 'COMP', 'VARNAME')


literals = ['.', '=' , ';']
def t_STR(t): r''' "([^"\n]|(\\"))*"|'([^'\n]|(\\'))*' '''; return t
def t_CLASSNAME(t): r''' [A-Z]+ '''; return t
def t_MAKECLASS(t): r'''makeclass'''; return t
def t_SUBCLASS(t): r'''subclass'''; return t
def t_CONCAT(t): r'''concat'''; return t
def t_COMP(t): r'''compare'''; return t
def t_VARNAME(t): r'''_[a-z]+ '''; return t
t_ignore   = ' \n\t\r'
t_ignore_COMMENT = r'\//.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    ''' Prints error messages when scan fails '''
    print "Illegal character at line {} '{}'".format(t.lexer.lineno, \
        t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex
lex.lex()

#############################################
#
#   BNF Grammar
#
##
## <statement_list> ::=  <statement_list> <statement> ;
##                  | <statement> 
##
## <statement>  ::= MAKECLASS CLASSNAME <statement_list> ;
##              | SUBCLASS CLASSNAME CLASSNAME statement_list ;
##              | VARNAME '=' <expr> ;
##              | <expr> ;
##
## <expr> ::= CLASSNAME
##          | <expr> CONCAT <expr>
##          | <expr> COMP <expr>
##          | STR
##          | VARNAME
##
#############################################

class Node:
    """ stores nodes in a parse tree """
    allCLassesDict = {}
    allVarsDict = {}  
    
    def doit(self):
        return "Error"
    
class MakeclassNode(Node):
    """ """
    def __init__(self, name, bodyStatements):
        self.name = name
        self.bodyStatements = bodyStatements ##
        Node.allCLassesDict[name] = self ##
    def doit(self):
        #Node.allClassesDict[self.name] = self
        return self.name  
        
class SubclassNode(Node):
    """ """
    def __init__(self, supername, name, bodyStatements):
        self.name = name
        self.supername = supername
        self.bodyStatements = bodyStatements
        
        Node.allCLassesDict[name] = self ##
        
    def doit(self):
        #Node.allClassesDict[self.name] = self
        #print  self.supername, " : ", self.name
        return self.supername


class CallNode(Node):
    """ """
    def __init__(self, name):
        self.name = name

    def doit(self):
        node = Node.allCLassesDict[self.name]
        result = ""
        for statement in node.bodyStatements:
            result =statement.doit()
        return result
        
class ConcatNode(Node):
    def __init__(self, leftNode, rightNode):
        self.leftNode = leftNode
        self.rightNode = rightNode
        
    def doit(self):
        result = self.leftNode.doit() + self.rightNode.doit()
        print result
        return result   
        
class CompareNode(Node):
    def __init__(self, leftNode, rightNode):
        self.leftNode = leftNode
        self.rightNode = rightNode
        
    def doit(self):
        result = "False"
        if self.leftNode.doit() == self.rightNode.doit():
            result = "True"
        print result
        return result                     
        
class StringNode(Node):
    def __init__(self, thestring):
        self.value = thestring[1:-1]
        
    def doit(self):
        return self.value
        
class AssignVarNode(Node):
    def __init__(self, variable_name, node):
        self.variable_name = variable_name
        self.node_value = node
    
    def doit(self):
        Node.allVarsDict[self.variable_name] = self.node_value
        return self.node_value
           

class GetVarValueNode(Node):
    def __init__(self, variable_name):
        self.variable_name = variable_name
    
    def doit(self):
        result = Node.allVarsDict[self.variable_name].doit()
        print result
        return result        
        
 
                      
        
######################################################################
# Parsing rules

def p_statement_list_mult(p):
    " statement_list : statement_list statement "
    p[0] = p[1].append(p[2]) # return a list

def p_statement_list_single(p):
    " statement_list : statement "
    p[0] = [p[1]] # return a list
 
def p_statement_makeclass(p):
    " statement : MAKECLASS CLASSNAME statement_list ';' "
    p[0] = MakeclassNode(p[2], p[3])

    
def p_statement_sublass(p):
    " statement : SUBCLASS CLASSNAME CLASSNAME statement_list ';' "
    p[0] = SubclassNode(p[2], p[3], p[4])
  
def p_statement_assignvar(p):
    " statement : VARNAME '=' expr ';' "
    p[0] = AssignVarNode(p[1], p[3])
    
    
def p_statement_expr(p):
    " statement : expr ';' "
    p[0] = p[1]
    
    
def p_expr_call(p):
    " expr : CLASSNAME "
    p[0] = CallNode(p[1])
    
def p_expr_concat(p):
    " expr : expr CONCAT expr "
    p[0] = ConcatNode(p[1], p[3])
    
def p_expr_comp(p):
    " expr : expr COMP expr "
    p[0] = CompareNode(p[1], p[3])

def p_expr_string(p):
    " expr : STR "
    p[0] = StringNode(p[1])
    
def p_expr_getvalue(p):
    " expr : VARNAME "
    p[0] = GetVarValueNode(p[1])
    
     
# Error reporting
def p_error(p):
    ''' Prints error messages when parse fails '''
    if p: print("Syntax error at line {} '{}'".format(
          p.lineno, p.value))
    else: print("Syntax error at EOF")

  


import ply.yacc as yacc
yacc.yacc()

######################################################################
# Test driver

def interpret_result_list(a_result_list):
    
    if None != a_result_list:
       [node.doit() for node in a_result_list]

import sys

if 1 < len(sys.argv):
   with open(sys.argv[1], 'r') as myfile:data=myfile.read()
   
   f.closed
   interpret_result_list(yacc.parse(data+'\n')) # parse returns None upon error

else:
   while 1:
       try:
           s = raw_input('calc > ')
       except EOFError:
           break
       if not s: continue
      
       interpret_result_list(yacc.parse(s+'\n')) # parse returns None upon error