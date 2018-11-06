class Bintree:
    def __init__(self,_value=None,_left=None,_right=None):
        self.value = value
        self.left = _left
        self.right = _right

    def setLeft(self,_left):
        if self.left:
            print("Warning: overwriting node")
        self.left = _left

    def setRight(self,_right):
        if self.right:
            print("Warning: overwriting node")
        self.right = _right

class Huffman:
    def __init__(self,pset):
        
