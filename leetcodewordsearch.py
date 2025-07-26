class Solution(object):
    def exist(self, board, word):
        """
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """

        def add_edge(matrix, value=0):
            if not matrix:
                return []

            rows = len(matrix)
            cols = len(matrix[0])

    
            top_bottom = [value] * (cols + 2)

    
            new_matrix = [top_bottom] 
            for row in matrix:
                new_matrix.append([value] + row + [value])
            new_matrix.append(top_bottom)  

            return new_matrix
        print(board)
        board = add_edge(board)
        print(board)

        def checkadj(check, x,y):
            if board[x + 1][y] == check or board[x - 1][y] == check or board[x][y + 1] == check or board[x][y - 1] == check:
                return True
            return False
        lm = []

        for x in range(len(board)):
            for j in range(len(board[0])):
                if board[x][j] == word[0]:
                    lm.append([j,x])
        print(lm)
        

        for x in range(len(lm)):
            for j in range(len(word)):
                if checkadj(word[2], lm[x][0], lm[x][1]):
                    
                    return True
                
                return False



        