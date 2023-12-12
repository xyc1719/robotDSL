# 需求
## 基本要求：

 脚本语言的语法可以自由定义，只要语义上满足描述客服机器人自动应答逻辑的要求。

 程序输入输出形式不限，可以简化为纯命令行界面。

 应该给出几种不同的脚本范例，对不同脚本范例解释器执行之后会有不同的行为表现

## 评分标准

**风格：**
满分15分，其中*代码注释*6分，*命名*6分，其它3分。

**设计和实现：**
满分30分，其中*数据结构7*分，*模块划分*7分，*功能*8分，*文档*8分。

**接口：**
满分15分，其中*程序间接口*8分，*人机接口*7分。

**测试：**
满分30分，*测试桩*15分，*自动测试脚本*15分

**记法：**
满分10分，文档中对此*脚本语言的语法*的准确描述。


# 敏捷开发1.0
## parser和分析树合并
class parser代替分析和数据结构模块。

interpreter模块中调用parser模块完成初始化，实现客服脚本的分析和分析树的传递。

同理interpreter也使用class，供主程序调用
## 命名风格

命名应遵循以下风格：

- 类名统一使用大驼峰命名法，如： `RunPy, Parser`等
- 类的公开接口使用小驼峰命名法，如： `getInstance， callFunc`
- 类的私有方法使用下划线+小驼峰命名法，如： `_helper, _getConfig`

## BNF语法
### 关键词
```
   step endstep stepto
   switch case default endswitch 
   welcome speak listen 
   exit call(py脚本调用)  
```
silence通过 case '' action实现
### 符号
var STR INT
### 语法
```
script  : stepblock
        |stepblock script

stepblock   : 'step' stepname statements 'endstep'

statements  : ε
            | statement statements 

statement   : action
            | switch_case

action  : VAR '=' expression
        | 'speak' expression
        | 'listen' expr expr
        | 'stepto' stepname
        | 'exit'
        | 'call' filename args

switch_case : 'switch' VAR cases 'endswitch'

cases   : case
        | case cases
        | default

case    : 'case' STR action

default : 'default' action

expression  : expr 
            | expr + expression

expr    : VAR | STR

args  : ε
        | expr ' ' args
```


## 12/5 完成静态部分
### 实现lexer 
accomplished

------
### 实现configLoader?
设计config格式

验证

函数返回值
### 仿照示例程序实现praser
accomplished and tessted....
静态设计部分已完成
测试脚本框架已实现
缺少测试用extended的python脚本
缺少完整的强dsl脚本
---
# 12/11
## 设计完成interpreter的部分细节

检验脚本是否合法
accomplished...
实现主要关键字
accomplished...

保存执行顺序和全局变量（没有局部变量）
varTable accomplished...
exec order accomplished...

### 得到parser的分析树
### 设计脚本应答时的数据结构和指针
---
# 12/12
### 单线程下完成分析
accomplished...
### 完成 call脚本编写和测试
调用extended中python脚本

- 规范接口
  - 通过yaml文件录入扩展函数所在文件夹。
  - call funcName args* 为在脚本中的输入格式
  - 要求输入的参数均为字符串，
  - 输出也为字符串，存放在$ret中
  - 需要新增扩展函数时，向extended中Exteded.py内写入新函数即可，注意输入输出规范
  - 也支持使用新的python文件，但需要修改yaml的路径值
  - 当检查到pyhon文件内不含有call调用的函数时，会报告函数缺失错误
- 解析脚本
  - importlib读入python文件，在运行时检查调用是否合法
- 传递参数
  - funcName *args
- 返回参数
  - $ret

accomplished...
# 12/13
## 测试和注释
自动化测试脚本，特别是dsl部分
## 文档
### 记号的说明只有文法，缺少面向用户的说明，缺少脚本的编写规范