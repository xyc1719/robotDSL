from ply.lex import lex
from logging import getLogger
from ConfigYamlLoader import MyConfigLoader

logrecord = getLogger('Interpreter')
'''
    通过ply.lex实现词法分析
    通过MyLexer限制词法分析器的作用域
    MyLexer中的参数和大部分函数，都会在lex构建时被使用
'''
class MyLexer:
    #关键字
    reserved={
        'step':     'STEP',
        'endstep':  'ENDSTEP',
        'stepto':   'STEPTO',
        'switch':   'SWITCH',
        'case':     'CASE',
        'default':  'DEFAULT',
        'endswitch':'ENDSWITCH',
        'welcome':  'WELCOME',
        'speak':    'SPEAK',
        'listen':   'LISTEN',
        'EXIT':     'CALL'
    }
    #特殊符号类型
    tokens=['NEWLINE','VAR','STR','ID']+list(reserved.values())

    #直译符号
    literals=['=','+']
    # #号开头的脚本行为注释行
    t_ignore_COMMENT=r'\#.*'
    # 忽视空格和制表符
    t_ignore=' \t'

    def __init__(self,configLoader,**kwargs):
        self._lexer=lex(module=self,**kwargs)
        self._file=None
        self._configLoader=configLoader

    def getLexer(self):
        '''
        :return: 返回类中lex
        '''
        return self._lexer

    def loadScript(self,path):
        """
        载入脚本文件
        :param path:待分析文件路径
        :return: None
        """
        self._file=None
        with open(path,'r',encoding='utf-8') as file:
            self._file=file.read()
        if not self._file:
            logrecord.error(f'Failed to load script {path}')
            return
        self._lexer.input(self._file)
        self._lexer.lineno=1
    def loadStr(self,str):
        """
        载入分析用字符串
        :param str: 待分析字符串
        :return:None
        """
        self._file = str
        self._lexer.input(str)
        self._lexer.lineno = 1

    def getToken(self):
        """
        :return: 下一个词法分析结果
        :raises RuntimeError: 脚本文件载入失败
        """
        if not self._file:
            raise RuntimeError('fail to find the script.')
        return self._lexer.token()

    def t_NEWLINE(self,t):
        r'\n+'
        t.lexer.lineno+=len(t.value)
        return t

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-z0-9_]*'
        # 当t.value为保留字时返回保留字，否则返回ID类型和字符串的值
        t.type=self.reserved.get(t.value,'ID')
        return t

    def t_VAR(self,t):
        r'\$[a-zA-Z0-9_]+'
        t.value=t.value[1:]
        return t

    def t_STR(self,t):
        r'''"(?:\\.|[^"\\])*"'''
        #处理双引号内的字符串，包括\转义
        t.value=t.value[1:-1]
        return t

    def t_INT(self,t):
        r'0|[1-9][0-9]*'
        t.value=int(t.value)
        return t

    def t_error(self,t):
        msg = f'line {t.lexer.lineno}:unexpected symbol {t.value}'
        if self._configLoader.getJobConfig().get('halt-onerror'):
            raise RuntimeError(msg)
        logrecord.error(msg)
        t.lexer.skip(1)

if __name__=='__main__':
    c= MyConfigLoader('./testdata/default.yaml')
    myLexer =MyLexer(c)
    myLexer.loadStr('''step stepto name endstep''')
    token=myLexer.getToken()
    while token:
        print(token)
        token=myLexer.getToken()
