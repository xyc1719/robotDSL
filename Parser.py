from logging import getLogger
from ply.yacc import yacc
from ConfigYamlLoader import MyConfigLoader
from Lexer import MyLexer
from ASTNode import MyASTNode

logrecord = getLogger('Interpreter')

'''
使用解析器解析输入，它会返回一个AST的根节点。
def parse(program):
    return parser.parse(program)

ast = parse("3 + 4 * 5")
'''
class MyParser:
    '''
    Myparser:基于MyLexer和MYASTNode的语法分析器
    '''
    def __init__(self,configLoader: MyConfigLoader,myLexer:MyLexer):
        self._my_lexer = myLexer
        self.tokens = myLexer.tokens
        self._yacc = yacc(module=self,debug=True)
        self._configLoader=configLoader

    def parseScript(self,script):
        '''
        输入脚本字符串，返回语法生成树
        :param script: 脚本字符串
        '''
        return self._yacc.parse(script,self._lexer.getLexer())

    def p_error(self,p):
        if(self._configLoader.getScriptConfig()['halt-onerror']):
            raise RuntimeError(f"SyntaxError on line{self._my_lexer.getLexer().lineno}, unexpected syntax: {p}")
        logrecord.error(f"SyntaxError on line{self._my_lexer.getLexer().lineno}, unexpected syntax: {p}")

    def p_script(self,p):
        '''
        script  : newlines
                | newlines stepblock script
        '''
        if(len(p)==2):
            p[0]=MyASTNode("Root")
        else:
            p[0]=MyASTNode("Root",p[2],*p[3])

    def p_stepblock(self,p):
        '''
        stepblock   : STEP ID statements ENDSTEP
        '''
        p[0]=MyASTNode(['stepblock',p[2]],*p[3])

    def p_statements(self,p):
        '''
        statements  : newlines
                    | NEWLINE statement statements
        '''
        if(len(p)==2):
            p[0]=[]
        else:
            p[0]=[p[2],*p[3]]
    def p_statement(self,p):
        '''
        statement   : action
                    | switch_case
        '''
        p[0]=p[1]
    def p_action(self,p):
        '''
        action  : VAR '=' expression
                | SPEAK expression
                | LISTEN expr expr
                | STEPTO ID
                | EXIT
                | CALL ID args
        '''
        if(len(p)==4 and p[2]=='='):
            p[0]=MyASTNode(['statement','assign',p[1]],p[3])
        elif len(p)==2:
            p[0]=MyASTNode(('statement',p[1]),)
        else:
            p[0]=MyASTNode(('statement',p[1]),*p[2:])

    def p_switch_case(self,p):
        '''
        switch_case : SWITCH VAR cases ENDSWITCH
        '''
        p[0]=MyASTNode(['statement','switch',p[2]],*p[3])

    def p_cases(self,p):
        '''
        cases   : newlines
                | newlines case cases
                | newlines default
        '''
        if len(p)==2:
            p[0]=[]
        elif len(p)==4:
            p[0]=[p[2]]+p[3]
        else :
            #reduce
            pass

    def p_case(self,p):
        '''
        case    : CASE STR action
        '''
        p[0]=MyASTNode(['case',p[2]],p[3])

    def p_default(self,p):
        '''
        default : DEFAULT action newlines
        '''
        p[0]=MyASTNode(['default',],p[2])

    def p_expression(self,p):
        '''
        expression  : expr
                    | expr '+' expression
        '''
        if len(p)==2:
            p[0]=MyASTNode(['expression',],p[1])
        else:
            p[0]=p[3]
            p[0].childs=[p[1]]+p[0].childs

    def p_expr_VAR(self,p):
        '''
        expr    : VAR
        '''
        p[0]=MyASTNode(['var',p[1]],)

    def p_expr_STR(self,p):
        '''
        expr    : STR
        '''
        p[0]=MyASTNode(['str',p[1]],)

    def p_args(self,p):
        '''
        args    : empty
                | expr args
        '''
        if len(p)==2:
            p[0]=MyASTNode(['args',])
        else:
            p[0]=p[2]
            p[0].childs=[p[1]]+p[0].childs

    def p_empty(self,p):
        '''
        empty   :
        '''
        pass

    def p_newlines(self,p):
        '''
        newlines    : empty
                    | NEWLINE
        '''
        pass

if __name__=='__main__':
    conf=MyConfigLoader()
    conf.load('./data/default.yaml')
    lexer=MyLexer(conf)
    lexer.loadScript('./testdata/example.dsl')
    parser=MyParser(conf,lexer)