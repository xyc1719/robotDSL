from ConfigYamlLoader import MyConfigLoader
from Lexer import MyLexer
from Parser import MyParser
from ASTNode import MyASTNode
import yaml

goodconf=MyConfigLoader()
goodconf.load('./testdata/default.yaml')

class MyConfigLoaderTest:
    '''
    MyConfigLoader类的测试桩
    '''
    def test_parseScript(self):
        conf=MyConfigLoader()
        conf.load('./data/default.yaml')
        lexer=MyLexer(conf)
        lexer.loadScript('./testdata/example.dsl')
        parser=MyParser(conf, lexer)
        with open('./testdata/example.dsl','r',encoding='utf-8') as file :
            tree = parser.parseScript(file.read())
            tree.printTree()

    def test_missingKey(self):
        conf=MyConfigLoader()
        conf.load('./testdata/missingKey.yaml')
        if conf._config=={}:
            print('failed in missingKey...')
            print(conf._config)
            self.testflag=False
        else:
            print('fixed by default.yaml in missingKey...')

    def test_wrongValueType(self):
        conf = MyConfigLoader()
        conf.load('./testdata/wrongValueType.yaml')
        if conf._config=={}:
            print('failed in wrongValueType...')
            print(conf._config)
            self.testflag=False
        else:
            print('fixed by default.yaml in wrongValueType...')

    def test_goodValue(self):
        conf = MyConfigLoader()
        conf.load('./testdata/goodValue.yaml')
        with open('./testdata/goodValue.yaml','r',encoding='utf-8')as file:
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
            raise RuntimeError("Error in MyConfigLoaderTest...")

class MyLexerTest:
    '''
    MyLexer类的测试桩
    '''
    def test_getToken(self,str):
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
        print(self.test_getToken('''afsfd reserved exit call switch cases'''))
        print(self.test_loadScript())

class MyParserTest:
    '''
    MyParser类的测试桩
    '''
    def test_example(self):
        path_yaml='./testdata/default.yaml'
        path_dsl='./testdata/example.dsl'
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



if __name__=='__main__':
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