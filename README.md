# robotDSL基于领域特定语言的客服机器人设计与实现
----
## 基本要求：
- 脚本语言的语法可以自由定义，只要语义上满足描述客服机器人自动应答逻辑的要求。
- 程序输入输出形式不限，可以简化为纯命令行界面。
- 应该给出几种不同的脚本范例，对不同脚本范例解释器执行之后会有不同的行为表现。
---
Anyway, it has begun...

---
具体内容见[document/document.md](https://github.com/xyc1719/robotDSL/blob/main/document/document.md)

developing.md中是开发时的备忘录

---
目录划分
- data 存放默认设置，用于补充config.yaml中缺省的内容
- document 文档
- extend 额外脚本的内容，用户可以在Extend.py中写入新的python函数以实现在DSL语法范围内不能实现的工作
- lib 程序运行依赖的python脚本（编写重点、难点）
- script DSL客服脚本存放位置
- testdata 测试时使用的数据
