
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    
    
def worker(root, total):
        
    total = total + 1

    if not root.left == None and root.right == None:

        worker(root.right,total)
        worker(root.left,total)
    array.append(total)

def maxDepth(root):
    
    array = []
        
    worker(root, 1)

    array = array.sort

    return array[len(array) - 1]

maxDepth([3,9,20,None,None,15,7])