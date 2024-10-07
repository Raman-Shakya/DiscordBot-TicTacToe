import cv2

SIZE = 300 
SCALE = 0.6
SIZE3 = int(SIZE/3*SCALE)
BOARD = cv2.resize(cv2.imread('./assets/Board.png'), (SIZE, SIZE))
X = cv2.resize(cv2.imread('./assets/X.png'), (SIZE3, SIZE3))
O = cv2.resize(cv2.imread('./assets/O.png'), (SIZE3, SIZE3))

def drawBoard(board):
    currentBoard = BOARD.copy()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]==' ': continue
            posI = int((i+(1-SCALE)/2)*SIZE/3)
            posJ = int((j+(1-SCALE)/2)*SIZE/3)
            if board[i][j]=='X':
                currentBoard[posI:posI+SIZE3, posJ:posJ+SIZE3] = X
            if board[i][j]=='O':
                # overlay = cv2.addWeighted(currentBoard[i*SIZE//3:(i+1)*SIZE//3, j*SIZE//3:(j+1)*SIZE//3], 0.5, X, 0.5, -)
                currentBoard[posI:posI+SIZE3, posJ:posJ+SIZE3] = O
                pass
    cv2.imwrite('./currentBoard.jpg', currentBoard)
    return currentBoard