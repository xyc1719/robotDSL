import yaml
from cerberus import Validator

class MyConfigYamlLoader:
    def __int__(self,path=''):
        if path:
            self.load(path)

    def getConfigYaml(self):
        return self._config

    def load(self,path='./config.yaml',encoding='utf-8'):
        with open(path,'r',encoding=encoding) as file:
            config=yaml.safe_load(file)
        if self._validate(config):
            self._config=config
        else:
            self._config={}
        pass

    def getRumtime