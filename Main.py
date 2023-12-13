from lib import Interpreter
import logging
'''
    主程序，循环调用脚本直到退出
'''
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: [%(name)s] %(message)s'
)
def greeting():
    '''
    启动界面
    '''
    picture='''
****   ***  *****  ***  ***** ****    ***  *     
*   * *   * *   * *   *   *   *   *  *     *     
****  *   * ****  *   *   *   *   *   ***  *     
* *   *   * *   * *   *   *   *   *      * *     
*  **  ***  *****  ***    *   ****    ***  ***** 
'''
    print(picture)

def initializing():
    '''
    初始化执行环境
    修改yaml配置和配置中对应文件的内容实现不同功能
    :return:
    '''
    config= Interpreter.MyConfigLoader()
    config.load('./config.yaml')
    funcVar= Interpreter.MyFuncVar('007', config)
    interpreter= Interpreter.MyInterpreter(config)
    interpreter.reset(funcVar)
    return interpreter

if __name__=="__main__":
    greeting()
    interpreter=initializing()
    while interpreter.getStatus():
        interpreter.run()