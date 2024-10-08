import cv2
import numpy as np

SIZE = 300
SCALE = 0.8
SIZE3 = int(SIZE/3*SCALE)
BOARD = cv2.resize(cv2.imread('./assets/Board.png'), (SIZE, SIZE))
X = cv2.resize(cv2.imread('./assets/X.png', cv2.IMREAD_UNCHANGED), (SIZE3, SIZE3))
O = cv2.resize(cv2.imread('./assets/O.png', cv2.IMREAD_UNCHANGED), (SIZE3, SIZE3))

X_color = X[:, :, :3]
X_alpha = X[:, :, 3] / 255.0
O_color = O[:, :, :3]
O_alpha = O[:, :, 3] / 255.0

def putX(block):
    for c in range(0, 3):
        block[:, :, c] = block[:, :, c] * (1 - X_alpha) + X_color[:, :, c] * X_alpha
    return block

def putO(block):
    for c in range(0, 3):
        block[:, :, c] = block[:, :, c] * (1 - O_alpha) + O_color[:, :, c] * O_alpha
    return block

def drawBoard(board):
    currentBoard = BOARD.copy()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]==' ': continue
            posI = int((i+(1-SCALE)/2)*SIZE/3)
            posJ = int((j+(1-SCALE)/2)*SIZE/3)
            block = currentBoard[posI:posI+SIZE3, posJ:posJ+SIZE3]
            if board[i][j]=='X':
                currentBoard[posI:posI+SIZE3, posJ:posJ+SIZE3] = putX(block)
            if board[i][j]=='O':
                # overlay = cv2.addWeighted(currentBoard[i*SIZE//3:(i+1)*SIZE//3, j*SIZE//3:(j+1)*SIZE//3], 0.5, X, 0.5, -)
                currentBoard[posI:posI+SIZE3, posJ:posJ+SIZE3] = putO(block)
                pass
    cv2.imwrite('./currentBoard.jpg', currentBoard)
    return currentBoard

# cv2.imshow("board", drawBoard(["OOX", "X O", " XX"]))
# cv2.waitKey(0)