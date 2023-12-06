import Interpreter
import logging

#启动时欢迎界面,ascii艺术
def greeting():
    picture='''
****   ***  *****  ***  ***** ****    ***  *     
*   * *   * *   * *   *   *   *   *  *     *     
****  *   * ****  *   *   *   *   *   ***  *     
* *   *   * *   * *   *   *   *   *      * *     
*  **  ***  *****  ***    *   ****    ***  ***** 
'''
    print(picture)

if __name__=="__main__":
    greeting()