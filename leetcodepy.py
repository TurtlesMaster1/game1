
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution(object):
    
    
    def worker(root, total):
        
        total = total + 1

        if not root.left == None and root.right == None:

            self.worker(root.right,total)
            self.worker(root.left,total)
        array.append(total)

    def maxDepth(self,root):
        array = []
        
        worker(root, 1)

        array = array.sort

        return array[len(array) - 1]