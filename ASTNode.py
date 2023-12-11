class MyASTNode:
    def __init__(self,type,*childs):
        self.type=type
        self.childs=list(childs)

    def printTree(self,depth=0):
        '''
        打印AST结点构成的树
        '''
        print('-'*depth,end='')
        print(self.type)
        for child in self.childs:
            child.printTree(depth=depth+1)
