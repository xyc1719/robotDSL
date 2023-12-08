import yaml
from cerberus import Validator

class MyConfigYamlLoader:
    # 定义schema
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
        'extended_script': {
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
        return self._config

    def getRuntimeConfig(self):
        return self._config.get('runtime')

    def getScriptConfig(self):
        return self._config.get('script')

    def getExtendConfig(self):
        return self._config.get('extend')

    def load(self,path='./config.yaml',encoding='utf-8'):
        with open(path,'r',encoding=encoding) as file:
            config=yaml.safe_load(file)
        if self._validate(config):
            self._config=config
        else:
            self._config={}
        self._svaeConfig()

    def _saveConfig(self):
        with open('./saved.yaml','r',encoding='utf-8') as file:
            savedConfig = yaml.safe_load(file)
        savedConfig.update(self._config)
        self._config=savedConfig

    def _validate(self,config):
        validator = Validator(self.schema)
        return validator.validate(config)

