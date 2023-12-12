from logging import getLogger
import inputimeout

from lib.ConfigYamlLoader import MyConfigLoader

logrecord=getLogger('FuncVar')

class MyFuncVar:

    varTable={
        'inputBuffer':'',
        '_robotID':''
    }
    def __init__(self,robotID,configLoader:MyConfigLoader):
        logrecord.info('Initializing Running Environment...')
        self._config=configLoader
        self.varTable['_robotID']=str(robotID)

    def assign(self,var,value):
        '''
        给变量Var赋值
        :param var:变量名
        :param value:变量值，赋值后自动变为字符串
        '''
        self.varTable[var]=str(value)

    def getVar(self,var):
        '''
        从变量表中得到变量值
        :param var: 变量名
        :return:变量值，类型为字符串
        '''
        if var not in self.varTable.keys():
            self.varTable[var]=''
        return self.varTable[var]

    def speak(self,sentence):
        '''
        程序把说的内容显示到屏幕上
        若需要语音输出则需要改写该接口
        :param sentence: speak的内容
        '''
        print(f'''Robot {self.getVar('_robotID')} SPEAK >> {sentence}''')

    def listen(self,limitedTime):
        '''
        等待用户输入，并限制输入时间
        输入结果存入 inputBuffer
        :param limitedTime: 最大输入时间，单位为秒
        '''
        print(f'Please speak within {limitedTime} seconds...')
        try:
            inputBuffer=inputimeout.inputimeout(prompt='SPEAK << ',timeout=int(limitedTime))
        except inputimeout.TimeoutOccurred:
            inputBuffer=''
            logrecord.info('User Speak timeout...')
        self.assign('inputBuffer', inputBuffer)

    def exit(self):
        '''
        退出指令，主程序在运行侧退出
        记录退出信息
        '''
        logrecord.info(f'''Robot {self.getVar('_robotID')}exits....''')