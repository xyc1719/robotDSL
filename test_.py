from ConfigYamlLoader import MyConfigLoader
from Lexer import MyLexer
from Parser import MyParser
from ASTNode import MyASTNode
import yaml

goodconf=MyConfigLoader()
goodconf.load('./testdata/default.yaml')

class MyConfigYmalLoaderTest:

    def test_parseScript(self):
        conf=MyConfigLoader()
        conf.load('./data/default.yaml')
        lexer=MyLexer(conf)
        lexer.loadScript('./testdata/example.dsl')
        parser=MyParser(conf, lexer)
        with open('./testdata/example.dsl','r',encoding='utf-8') as file :
            p = parser.parseScript(file.read())
            print(p)

    def test_missingKey(self):
        conf=MyConfigLoader()
        conf.load('./testdata/missing_key.yaml')
        if conf._config=={}:
            print('Error from func missingKey...')
        else:
            print('failed in missingKey...')

    def test_wrongValueType(self):
        conf = MyConfigLoader()
        conf.load('./testdata/wrongValueType.yaml')
        if conf._config=={}:
            print('Error from func wrongValueType...')
        else:
            print('failed in wrongValueType...')

    def test_goodValue(self):
        conf = MyConfigLoader()
        conf.load('./testdata/goodValue.yaml')
        with open('./testdata/goodValue.yaml','r',encoding='utf-8')as file:
            directload=yaml.safe_load(file)
        if directload==conf._config:
            print('Loaded correctly from goodValue...')
        else:
            print('failed in goodValue...')

    def test_list(self):
        test.test_parseScript()
        test.test_missingKey()
        test.test_wrongValueType()
        test.test_goodValue()

if __name__=='__main__':
    test=MyConfigYmalLoaderTest()
    print('fucker...')
    test.test_list()