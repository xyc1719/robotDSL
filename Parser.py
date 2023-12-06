from logging import getLogger
from ply.yacc import yacc
from ConfigYamlLoader import MyConfigYamlLoader
from Lexer import MyLexer

logrecord = getLogger('Interpreter')
class Parser:
    def __init__(self,configLoader: MyConfigYamlLoader,lexer:MyLexer):
        self._lexer = lexer
        self.tokens = lexer.tokens
        self._yacc = yacc(module=self,debug=True)
        self._configLoader=configLoader

    def parseStr(self,str):
        return self._yacc.parse(str,self._lexer.getLexer())

    def