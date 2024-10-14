import cv2
import numpy as np

SIZE = 300
SCALE = 0.8
SIZE3 = int(SIZE/3*SCALE)

BOARD = None
X = None
O = None
X_color = None
X_alpha = None
O_color = None
O_alpha = None

def readImages():
    global BOARD, X, O, X_color, X_alpha, O_color, O_alpha
    BOARD = cv2.resize(cv2.imread('./assets/Board.png'), (SIZE, SIZE))
    X = cv2.resize(cv2.imread('./assets/X.png', cv2.IMREAD_UNCHANGED), (SIZE3, SIZE3))
    O = cv2.resize(cv2.imread('./assets/O.png', cv2.IMREAD_UNCHANGED), (SIZE3, SIZE3))

    X_color = X[:, :, :3]
    if X.shape[2] == 4: X_alpha = X[:, :, 3] / 255.0
    else: X_alpha = np.ones(X_color.shape[:2], dtype=np.float32)
    O_color = O[:, :, :3]
    if O.shape[2] == 4: O_alpha = O[:, :, 3] / 255.0
    else: O_alpha = np.ones(O_color.shape[:2], dtype=np.float32)

    drawHelp()


def resetImages():
    cv2.imwrite('./assets/Board.png', cv2.imread('./assets/BoardDefault.png'))
    cv2.imwrite('./assets/X.png', cv2.imread('./assets/XDefault.png', cv2.IMREAD_UNCHANGED))
    cv2.imwrite('./assets/O.png', cv2.imread('./assets/ODefault.png', cv2.IMREAD_UNCHANGED))
    readImages()

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
    cv2.imwrite('./tempAssets/currentBoard.jpg', currentBoard)
    return currentBoard


def drawHelp():
    currentBoard = BOARD.copy()
    avg = np.average(currentBoard, axis=(0, 1, 2))
    if avg > 192:
        color = (25, 25, 25)
    else:
        color = (230, 230, 230)
    fontSize = 40
    scale = SIZE3 / 40
    for move in range(1, 10):
        i = (((move-1) % 3) + 0.5) * SIZE/3 - fontSize/2
        j = ((2 - (move-1) // 3 + 0.5)) * SIZE / 3 + fontSize/2
        cv2.putText(currentBoard, str(move), (int(i), int(j)), cv2.FONT_HERSHEY_SIMPLEX,
                   scale, color, 5, cv2.LINE_AA)
        
    cv2.imwrite('./tempAssets/helpBoard.jpg', currentBoard)
    return currentBoard


readImages()
# cv2.imshow("board", drawHelp())
# cv2.waitKey(0)