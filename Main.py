from lib import Interpreter
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: [%(name)s] %(message)s'
)
#启动时欢迎界面,ascii艺术
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
    config= Interpreter.MyConfigLoader()
    config.load('./config.yaml')
    funcVar= Interpreter.MyFuncVar('007', config)
    global interpreter
    interpreter= Interpreter.MyInterpreter(config)
    interpreter.loadFuncVar(funcVar)

if __name__=="__main__":
    greeting()
    initializing()
    while not interpreter._stop:
        interpreter.run()