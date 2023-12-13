from lib.ConfigYamlLoader import MyConfigLoader
from lib.Lexer import MyLexer
from lib.Parser import MyParser
from lib.ASTNode import MyASTNode
from lib.FuncVar import MyFuncVar
import importlib
from logging import getLogger

logrecord=getLogger('Interpreter')

class MyInterpreter:
    '''
    脚本执行器
    分析语法树，并执行
    基本关键词调用和符号表由FuncVar管理
    脚本递归调用过程和分析的递归调用过程一致，不需要特别用数据结构管理
    '''

    script=''
    astTree=None
    steps={}
    _stop=False
    _module=None

    def __init__(self,configLoader:MyConfigLoader):
        self._config=configLoader
        self._lexer=MyLexer(configLoader)
        self._parser=MyParser(self._config,self._lexer)
        self._module=importlib.import_module(self._config.getExtendedConfig()['dirs'][0])

        self._loadScript()
        self._getastTree()

    def reset(self,funcVar:MyFuncVar):
        '''
        初始化Interpreter执行环境，载入符号表和关键词函数
        :param funcVar: 辅助Interpreter运行的类，包含了关键词的实现函数函数和符号表
        '''
        self._stop=False
        self.funcVar=funcVar

    def run(self):
        '''
        启动DSL脚本执行器
        默认从main函数进入
        '''
        if not self.funcVar or not self.astTree:
            raise RuntimeError('Load Script and RunningConfig before running...')
        logrecord.info('Begin running...')
        if 'main' not in self.steps:
            print(self.steps.keys())
            raise RuntimeError('step main not be defined...')
        self._runStep(self.steps['main'])

    def getStatus(self):
        '''
        获取当前Interpreter执行状态
        :return:Interpreter执行状态，是否可以继续
        '''
        return not self._stop

    def _runStep(self,step:MyASTNode):
        '''
        依次执行step中的代码
        :param step: step树，即函数代码块
        '''
        for statement in step.childs:
            self._execute(statement)

    def _getStep(self,stepID):
        '''
        在DSL脚本执行器进入某个函数时，需要先检验函数是否存在
        :param stepID: 函数名

        step 目标函数的语法树
        '''
        step=self.steps.get(stepID,None)
        if not step:
            raise RuntimeError(f'Step {stepID} not be defined...')
        return step

    def _execute(self,statement:MyASTNode):
        '''
        分拣执行语句的执行函数，语句的种类如下：
        1.非执行语句;2.关键词引导的执行语句;3.函数进入;4.调用扩展函数;5.进入分支语句;
        :param statement:执行语句的语法树
        '''
        if self._stop:
            return
        if statement.type[0]!='statement':
            logrecord.error('statement not found...')
        elif statement.type[1]=='assign':
            self.funcVar.assign(statement.type[2],self._getVal(statement.childs[0]))
        elif statement.type[1]=='speak':
            self.funcVar.speak(self._getVal(statement.childs[0]))
        elif statement.type[1]=='listen':
            self.funcVar.listen(self._getVal(statement.childs[0]))
        elif statement.type[1]=='exit':
            self._stop=True
            self.funcVar.exit()
        elif statement.type[1]=='stepto':
            self._runStep(self._getStep(statement.childs[0].type[1]))
        elif statement.type[1]=='call':
            self._callFunction(statement.childs[0].type[1],self._getArgs(statement.childs[1]))
        elif statement.type[1]=='switch':
            self._switchCase(statement)

    def _getArgs(self,args:MyASTNode):
        '''
        获取调用扩展函数时所需要的参数
        :param args: 参数所在的语法树
        :return: 列表化后的参数，均为字符串
        '''
        arg_list=[]
        for child in args.childs:
            arg_list.append(self._getVal(child))
        return arg_list

    def _callFunction(self,funcName,args):
        '''
        调用扩展函数的执行函数
        返回结果为字符串，存入$ret中
        :param funcName:扩展函数名
        :param args:扩展函数需要的参数，格式为列表，类型为字符串

        func -> 扩展函数
        '''
        func = getattr(self._module,funcName,None)

        if func and callable(func):
            self.funcVar.assign('ret',func(*args))
        else:
            if self._config.getExtendedConfig()['halt_on_error']==True:
                raise RuntimeError(f"Function {funcName} not found in {self._config.getExtendedConfig()['dirs'][0]}")
            logrecord.debug(f"Function {funcName} not found in {self._config.getExtendedConfig()['dirs'][0]}")


    def _switchCase(self,statement:MyASTNode):
        '''
        分治语句执行函数
        :param statement:分治条件的语法树

        condition 条件变量的值
        cases 条件变量可能值
        silence条件 可以通过 case '' action 实现
        '''
        condition=self.funcVar.getVar(statement.type[2])
        cases=[child.type[1] for child in statement.childs if child.type[0]=='case']
        default=statement.childs[-1] if statement.childs[-1].type[0] == 'default' else None
        pointer=-1
        for i in range(len(cases)):
            if cases[i]==condition:
                pointer=i
                break
        if pointer !=-1 :
            self._execute(statement.childs[pointer].childs[0])
        elif pointer==-1 and default :
            self._execute(default.childs[0])

    def _getVal(self,expression:MyASTNode):
        '''
        获取目标语法树的值
        :param expression: 待求值的语法树
        :return: 语法树的值
        :RuntimeError: 类型不匹配

        var 从符号表中得到变量值
        str 字符串值
        expression 递归求字符串并做合并

        '''
        if expression.type[0]=='var':
            return self.funcVar.getVar(expression.type[1])
        elif expression.type[0]=='str':
            return expression.type[1]
        elif expression.type[0]=='expression':
            strValue=''
            for expr in expression.childs:
                strValue=strValue+self._getVal(expr)
            return strValue
        else:
            if self._config.getScriptConfig()['halt_on_error']==True:
                raise RuntimeError(f'Illegal access to getVal with object{expression.type[0]}...')
            logrecord.debug(f'Illegal access to getVal with object{expression.type[0]}...')

    def _loadScript(self):
        '''
        读入配置文件中的目标脚本
        '''
        with open(self._config.getScriptConfig().get('path'),'r',encoding='utf-8')as file:
            self.script=file.read()
        self._lexer.loadStr(self.script)

    def _getastTree(self):
        '''
        通过语法分析，得到语法分析树
        同时，得到每个step函数的语法树
        '''
        logrecord.info('Build ASTree for scripts...')
        if self.script=='':
            raise RuntimeError('Script not found...')
        self.astTree=self._parser.parseScript(self.script)
        for child in self.astTree.childs:
            self.steps[child.type[1]]=child