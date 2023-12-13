from lib.ConfigYamlLoader import MyConfigLoader
from lib.Lexer import MyLexer
from lib.Parser import MyParser
from lib.Interpreter import MyInterpreter
from lib.FuncVar import MyFuncVar
import yaml
import sys

goodconf=MyConfigLoader()
goodconf.load('./testdata/default.yaml')

'''
自动化测试脚本
其中一部分内容为可行性测试
一部分为正确性测试
测试过程均会有输出，但是只有正确性测试会有异常抛出
最后一个测试可以通过修改manual变量，改为手动测试
'''
class MyConfigLoaderTest:
    '''
    MyConfigLoader类的测试桩
    '''
    def test_parseScript(self):
        '''
        测试简单DSL脚本能否进行静态分析
        可行性检测
        正确性检测需要在执行时测试
        '''
        conf=MyConfigLoader()
        conf.load('./data/default.yaml')
        lexer=MyLexer(conf)
        lexer.loadScript('./testdata/example.dsl')
        parser=MyParser(conf, lexer)
        with open('testdata/example.dsl', 'r', encoding='utf-8') as file :
            tree = parser.parseScript(file.read())
            tree.printTree()

    def test_missingKey(self):
        '''
        配置文件缺省项测试
        用默认配置补充缺省项
        '''
        conf=MyConfigLoader()
        conf.load('./testdata/missingKey.yaml')
        if conf._config=={}:
            print('failed in missingKey...')
            print(conf._config)
            self.testflag=False
        else:
            print('fixed by default.yaml in missingKey...')

    def test_wrongValueType(self):
        '''
        配置文件填写有误
        启用默认配置
        '''
        conf = MyConfigLoader()
        conf.load('./testdata/wrongValueType.yaml')
        if conf._config=={}:
            print('failed in wrongValueType...')
            print(conf._config)
            self.testflag=False
        else:
            print('fixed by default.yaml in wrongValueType...')

    def test_goodValue(self):
        '''
        另一个正确的配置文件
        要求读入校验后内容不发生修改
        :return:
        '''
        conf = MyConfigLoader()
        conf.load('./testdata/goodValue.yaml')
        with open('testdata/goodValue.yaml', 'r', encoding='utf-8')as file:
            directload=yaml.safe_load(file)
        if directload==conf._config:
            print('Loaded correctly from goodValue...')
        else:
            print('failed in goodValue...')
            print(conf._config)
            self.testflag=False

    def test_list(self):
        self.testflag=True
        self.test_parseScript()
        self.test_missingKey()
        self.test_wrongValueType()
        self.test_goodValue()
        if self.testflag==False:
            raise RuntimeError('Test failed in MyConfigLoaderTest...')

class MyLexerTest:
    '''
    MyLexer类的测试桩
    '''
    def test_getToken(self,str):
        '''
        字符串输入的词法分析测试
        可行性检测
        正确性检测在Parser测试桩中完成
        :param str: 输入字符串
        '''
        config=MyConfigLoader()
        config.load('./testdata/default.yaml')
        lexer=MyLexer(config)
        lexer.loadStr(str)
        tokens=[]
        token=lexer.getToken()
        while(token):
            tokens.append(token)
            token=lexer.getToken()
        return tokens

    def test_loadScript(self,path='./testdata/example.dsl'):
        '''
        文本输入的词法分析测试
        :param path: 测试脚本地址
        '''
        config=MyConfigLoader()
        config.load('./testdata/default.yaml')
        lexer=MyLexer(config)
        lexer.loadScript(path)
        tokens=[]
        token=lexer.getToken()
        while(token):
            tokens.append(token)
            token=lexer.getToken()
        return tokens


    def test_list(self):
        print(self.test_getToken('''step stepto name endstep'''))
        print('-----------')
        print(self.test_getToken('''afsfd reserved exit call switch cases'''))
        print('-----------')
        print(self.test_loadScript())

class MyParserTest:
    '''
    MyParser类的测试桩
    '''
    def test_example(self):
        '''
        静态部分分析树测试桩
        可行性测试
        正确性测试在执行时检测
        '''
        path_yaml= 'testdata/default.yaml'
        path_dsl= 'testdata/example.dsl'
        config=MyConfigLoader()
        config.load(path_yaml)
        lexer=MyLexer(config)
        lexer.loadScript(path_dsl)
        parser=MyParser(config,lexer)
        with open(path_dsl,'r',encoding='utf-8')as file:
            tree=parser.parseScript(file.read())
            tree.printTree()

    def test_list(self):
        self.test_example()

class MyFuncVarTest:
    '''
    MyFuncVar类的测试桩
    '''

    def test_varTable(self):
        '''
        符号表测试
        '''
        config=goodconf
        funcVar=MyFuncVar('007',config)
        funcVar.assign('variable1',123457)
        funcVar.assign('variable0','aksdjlfsd')
        if funcVar.getVar('variable1')!='123457':
            return False
        elif funcVar.getVar('variable0')!='aksdjlfsd':
            return False
        else:
            return True
    def test_list(self):
        if not self.test_varTable():
            raise RuntimeError('Test failed in MyFuncVarTest...')
        else:
            pass

class MyInterpreterTest:
    '''
    MyInterpreter类的测试桩
    '''

    def test_goodDSL(self):
        '''
        简单的DSL脚本
        自动测试
        '''
        config=MyConfigLoader()
        config.load('./testdata/default.yaml')
        funcVar=MyFuncVar('test1',config)
        interpreter=MyInterpreter(config)
        interpreter.reset(funcVar)
        interpreter.run()

    def test_strongDSL(self,manual=False):
        '''
        DSL强测试
        默认自动输入
        可手动调试
        '''
        config=MyConfigLoader()
        config.load('./testdata/strongTest.yaml')
        funcVar=MyFuncVar('test2',config,timeout=manual)
        interpreter=MyInterpreter(config)
        interpreter.restart(funcVar)
        # while interpreter.getStatus():
        if not manual:
            print('auto mode')
            sys.stdin=open('./testdata/in.txt','r',encoding='utf-8')
            sys.stdout=open('./testdata/tempout.txt','w',encoding='utf-8')
            interpreter.run()
            sys.stdout=sys.__stdout__
            with open('./testdata/tempout.txt','r',encoding='utf-8') as file:
                tempout=file.read()
            with open('./testdata/out.txt','r',encoding='utf-8')as file:
                answer=file.read()
            if tempout==answer:
                pass
            else:
                print(tempout)
                print(answer)
                raise RuntimeError('Test failed in MyInterpreter...')
        else:
            print('manual mode')
            interpreter.run()

    def test_list(self,manual=False):
        self.test_goodDSL()
        print('-----------')
        self.test_strongDSL(manual)

if __name__=='__main__':
    '''
    通过manual控制最后一部分测试是否手动
    '''
    manual=False
    print('Test for MYConfigLoader...')
    print("----------------------------")
    test=MyConfigLoaderTest()
    test.test_list()
    print("----------------------------")
    print('Test for MyLexer...')
    print("----------------------------")
    test=MyLexerTest()
    test.test_list()
    print("----------------------------")
    print('Test for MyParser...')
    print("----------------------------")
    test=MyParserTest()
    test.test_list()
    print("----------------------------")
    print('Test for MyFuncVar...')
    print("----------------------------")
    test=MyFuncVarTest()
    test.test_list()
    print('Test passed....')
    print("----------------------------")
    print('Test for MyInterpreter...')
    print("----------------------------")
    test=MyInterpreterTest()
    test.test_list(manual)
    print('Test passed....')
    print("----------------------------")