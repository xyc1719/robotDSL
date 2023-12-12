from ConfigYamlLoader import MyConfigLoader
from Lexer import MyLexer
from Parser import MyParser
from ASTNode import MyASTNode
from FuncVar import MyFuncVar
from logging import getLogger

logrecord=getLogger('Interpreter')

class MyInterpreter:

    script=''
    astTree=None
    steps={}
    _stop=False

    def __init__(self,configLoader:MyConfigLoader):
        self._config=configLoader
        self._lexer=MyLexer(configLoader)
        self._parser=MyParser(self._config,self._lexer)

        self._loadScript()
        self._getastTree()

    def loadFuncVar(self,funcVar:MyFuncVar):
        self._stop=False
        self.funcVar=funcVar

    def run(self):
        if not self.funcVar or not self.astTree:
            raise RuntimeError('Load Script and RunningConfig before running...')
        logrecord.info('Begin running...')
        if 'main' not in self.steps:
            print(self.steps.keys())
            raise RuntimeError('step main not be defined...')
        self._runStep(self.steps['main'])

    def _runStep(self,step:MyASTNode):
        for statement in step.childs:
            self._execute(statement)

    def _getStep(self,stepID):
        step=self.steps.get(stepID,None)
        if not step:
            raise RuntimeError(f'Step {stepID} not be defined...')
        return step

    def _execute(self,statement:MyASTNode):
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
        elif statement.type[1]=='stepto':
            self._runStep(self._getStep(statement.childs[0].type[1]))
        elif statement.type[1]=='exit':
            self._stop=True
            self.funcVar.exit()
        elif statement.type[1]=='call':
            pass
        elif statement.type[1]=='switch':
            self._switchCase(statement)


    def _switchCase(self,statement:MyASTNode):
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
            raise RuntimeError('Illegal access to getVal...')

    def _loadScript(self):
        with open(self._config.getScriptConfig().get('path'),'r',encoding='utf-8')as file:
            self.script=file.read()
        self._lexer.loadStr(self.script)

    def _getastTree(self):
        logrecord.info('Build ASTree for scripts...')
        if self.script=='':
            raise RuntimeError('Script not found...')
        self.astTree=self._parser.parseScript(self.script)
        for child in self.astTree.childs:
            self.steps[child.type[1]]=child