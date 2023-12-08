class MyASTNode:
    def __init__(self,type,*childs):
        self.type=type
        self.childs=list(childs)