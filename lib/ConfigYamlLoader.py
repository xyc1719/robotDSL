import yaml
from cerberus import Validator

class MyConfigLoader:
    '''
    提供 载入分析yaml格式配置文件 的类
    '''
    schema = {
        'runtime': {
            'type': 'dict',
            'schema': {
                'log_level': {'type': 'string', 'allowed': ['info', 'debug', 'error']}
            }
        },
        'script': {
            'type': 'dict',
            'schema': {
                'path': {'type': 'string'},
                'halt_on_error': {'type': 'boolean'}
            }
        },
        'extended': {
            'type': 'dict',
            'schema': {
                'halt_on_error': {'type': 'boolean'},
                'dirs': {'type': 'list', 'schema': {'type': 'string'}}
            }
        }
    }

    def __int__(self,path=''):
        if path:
            self.load(path)
        else:
            pass

    def getConfigYaml(self):
        '''
        获取配置文件解析出的对象
        '''
        return self._config

    def getRuntimeConfig(self):
        '''
        获取Runtime部分配置
        '''
        return self._config.get('runtime')

    def getScriptConfig(self):
        '''
        获取script部分配置
        '''
        return self._config.get('script')

    def getExtendedConfig(self):
        '''
        获取extended部分配置
        '''
        return self._config.get('extended')

    def load(self,path='./default.yaml',encoding='utf-8'):
        '''
        载入有效配置文件
        :param path:文件位置默认在本文件夹中
        '''
        with open(path,'r',encoding=encoding) as file:
            config=yaml.safe_load(file)
        if self._validate(config):
            self._config=config
        else:
            self._config={}
        self._getDefaultConfig()

    def _getDefaultConfig(self):
        '''
        缺省部分用默认配置补全
        '''
        with open('./data/default.yaml', 'r', encoding='utf-8') as file:
            defaultConfig = yaml.safe_load(file)
        defaultConfig.update(self._config)
        self._config=defaultConfig

    def _validate(self,config):
        '''
        检验文件格式
        :param config: yaml格式的config
        '''
        validator = Validator(self.schema)
        return validator.validate(config)

