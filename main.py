import pygame
import random
import math

width = 700
height = 700
cellSize = 100

turnToPlay = "Computer"
#computerTurnCounter = 0
#playerTurnCounter = 0
turn = 0

playerSelectedPieceArr = []
computerSelectedPieceArr = []

run = True
selectedPiece = None

bestMove = None

board = [
    [1,0,0,0,0,0,2],
    [0,0,0,0,0,0,0],
    [1,0,0,0,0,0,2],
    [0,0,0,0,0,0,0],
    [2,0,0,0,0,0,1],
    [0,0,0,0,0,0,0],
    [2,0,0,0,0,0,1]
    ]

def drawBoard():
    for i in range(0,7):
        for j in range(0,7):
            pygame.draw.rect(backSurface, 'black', pygame.Rect(j * cellSize, i * cellSize, cellSize, cellSize), 1)


def drawPieces():
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if(val == 1):
                pygame.draw.polygon(backSurface, 'red', ((j * cellSize + 50, i * cellSize + 25), (j * cellSize + 25, i * cellSize + 75), (j * cellSize + 75, i * cellSize + 75)))
            if(val == 2):
                pygame.draw.circle(backSurface, 'red', (j * cellSize + 50, i * cellSize + 50), 25)


def findPossibleMoves(selectedPiece):
    row, column = selectedPiece[0], selectedPiece[1]
    possibleMoves = []
    
    if 7 > row + 1 >= 0 and board[row+1][column] != 1 and board[row+1][column] != 2:
        possibleMoves.append((row+1, column))
    if 0 <= row - 1 < 7 and board[row-1][column] != 1 and board[row-1][column] != 2:
        possibleMoves.append((row-1, column))
    if 7 > column + 1 >= 0 and board[row][column+1] != 1 and board[row][column+1] != 2:
        possibleMoves.append((row, column+1))
    if 0 <= column - 1 < 7 and board[row][column-1] != 1 and board[row][column-1] != 2:
        possibleMoves.append((row, column-1))

    for row, column in possibleMoves:
        board[row][column] = 3


def drawPossibleMoves():
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if(val == 3):
                pygame.draw.circle(backSurface, 'gray', (j * cellSize + 50, i * cellSize + 50), 5)


def MoveSelectedPiece(selectedPiece, mouseX, mouseY):
    row, column = selectedPiece
    board[row][column] = 0
    board[mouseY][mouseX] = 2

    selectedPieceNewPos = mouseY, mouseX

    playerSelectedPieceArr.append(selectedPieceNewPos)
    
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if(val == 3):
                board[i][j] = 0


def checkCapture():

    deletedPieces = []

    count = 0
    i = 0

    for x, row in enumerate(board):
        for y, value in enumerate(row):
            if value == 2: # Iterating for all the circles

                newPositionColumn = y
                newPositionRow = x

                #Checking right of the piece
                for i in range(newPositionColumn + 1, 8):
                    if i != 7:
                        if board[newPositionRow][i] == 2:
                            for j in range(newPositionColumn + 1, i):
                                if board[newPositionRow][j] == 1:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionColumn + 1, i):
                                if board[newPositionRow][j] == 1:
                                    count += 1


                if (i - newPositionColumn) - 1 == count:
                    for k in range(newPositionColumn + 1, i):
                        #board[newPositionRow][k] = 0
                        deletedPieces.append((newPositionRow, k, 1))

                count = 0

                #Checking left of the piece
                for i in range(newPositionColumn - 1, -2, -1):
                    if i != -1:
                        if board[newPositionRow][i] == 2:
                            for j in range(newPositionColumn - 1, i, -1):
                                if board[newPositionRow][j] == 1:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionColumn - 1, i, -1):
                                if board[newPositionRow][j] == 1:
                                    count += 1


                if (newPositionColumn - i) - 1 == count:
                    for k in range(newPositionColumn - 1, i, -1):
                        deletedPieces.append((newPositionRow, k, 1))

                count = 0

                #Checking up of the piece
                for i in range(newPositionRow - 1, -2, -1):
                    if i != -1:
                        if board[i][newPositionColumn] == 2:
                            for j in range(newPositionRow - 1, i, -1):
                                if board[j][newPositionColumn] == 1:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionRow - 1, i, -1):
                                if board[j][newPositionColumn] == 1:
                                    count += 1

                if (newPositionRow - i) - 1 == count:
                    for k in range(newPositionRow - 1, i, -1):
                        #board[k][newPositionColumn] = 0
                        deletedPieces.append((k, newPositionColumn, 1))
                count = 0

                #Checking down of the piece
                for i in range(newPositionRow + 1, 8):
                    if i != 7:
                        if board[i][newPositionColumn] == 2:
                            for j in range(newPositionRow + 1, i):
                                if board[j][newPositionColumn] == 1:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionRow + 1, i):
                                if board[j][newPositionColumn] == 1:
                                    count += 1

                if (i - newPositionRow) - 1 == count:
                    for k in range(newPositionRow + 1, i):
                        deletedPieces.append((k, newPositionColumn, 1))

                count = 0

            elif value == 1:  # Iterating for all the triangles

                newPositionColumn = y
                newPositionRow = x

                #Checking right of the piece
                for i in range(newPositionColumn + 1, 8):
                    if i != 7:
                        if board[newPositionRow][i] == 1:
                            for j in range(newPositionColumn + 1, i):
                                if board[newPositionRow][j] == 2:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionColumn + 1, i):
                                if board[newPositionRow][j] == 2:
                                    count += 1


                if (i - newPositionColumn) - 1 == count:
                    for k in range(newPositionColumn + 1, i):
                        deletedPieces.append((newPositionRow, k, 2))

                count = 0

                #Checking left of the piece
                for i in range(newPositionColumn - 1, -2, -1):
                    if i != -1:
                        if board[newPositionRow][i] == 1:
                            for j in range(newPositionColumn - 1, i, -1):
                                if board[newPositionRow][j] == 2:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionColumn - 1, i, -1):
                                if board[newPositionRow][j] == 2:
                                    count += 1


                if (newPositionColumn - i) - 1 == count:
                    for k in range(newPositionColumn - 1, i, -1):
                        deletedPieces.append((newPositionRow, k, 2))

                count = 0

                #Checking up of the piece
                for i in range(newPositionRow - 1, -2, -1):
                    if i != -1:
                        if board[i][newPositionColumn] == 1:
                            for j in range(newPositionRow - 1, i, -1):
                                if board[j][newPositionColumn] == 2:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionRow - 1, i, -1):
                                if board[j][newPositionColumn] == 2:
                                    count += 1

                if (newPositionRow - i) - 1 == count:
                    for k in range(newPositionRow - 1, i, -1):
                        deletedPieces.append((k, newPositionColumn, 2))
                count = 0

                #Checking down of the piece
                for i in range(newPositionRow + 1, 8):
                    if i != 7:
                        if board[i][newPositionColumn] == 1:
                            for j in range(newPositionRow + 1, i):
                                if board[j][newPositionColumn] == 2:
                                    count += 1
                            break
                    else:
                        for j in range(newPositionRow + 1, i):
                                if board[j][newPositionColumn] == 2:
                                    count += 1

                if (i - newPositionRow) - 1 == count:
                    for k in range(newPositionRow + 1, i):
                        deletedPieces.append((k, newPositionColumn, 2))

                count = 0



    for row, column, deletedPiece in deletedPieces:
        board[row][column] = 0


    return deletedPieces


def undoCapture(deletedPieces):

    for row, column,deletedPiece in deletedPieces:
        board[row][column] = deletedPiece


def evaluateBoard():
    eval = 0

    for i, row in enumerate(board):
        for j, val in enumerate(row):

            if i == 0:
                if val == 1:
                    eval -= 1
                elif val == 2:
                    eval += 1

            if i == 6:
                if val == 1:
                    eval -= 1
                elif val == 2:
                    eval += 1

            if j == 0:
                if val == 1:
                    eval -= 1
                elif val == 2:
                    eval += 1

            if j == 6:
                if val == 1:
                    eval -= 1
                elif val == 2:
                    eval += 1

            if val == 1:
                eval += 3
            elif val == 2:
                eval -= 3


    return eval


def findAllPossibleMoves(player):

    possibleMoves = []
    pieces = []

    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 1 and player == "Computer":
                pieces.append((i, j))
            elif val == 2 and player == "Player":
                pieces.append((i, j))


    for piece in pieces:
        row, column = piece
    
        if 7 > row + 1 >= 0 and board[row+1][column] != 1 and board[row+1][column] != 2:
            possibleMoves.append((piece, row+1, column))
        if 0 <= row - 1 < 7 and board[row-1][column] != 1 and board[row-1][column] != 2:
            possibleMoves.append((piece, row-1, column))
        if 7 > column + 1 >= 0 and board[row][column+1] != 1 and board[row][column+1] != 2:
            possibleMoves.append((piece, row, column+1))
        if 0 <= column - 1 < 7 and board[row][column-1] != 1 and board[row][column-1] != 2:
            possibleMoves.append((piece, row, column-1))


    return possibleMoves


def makeMove(piece, move, player):
    row, column = piece
    targetRow, targetColumn = move

    if player == "Computer":
        board[targetRow][targetColumn] = 1
    elif player == "Player":
        board[targetRow][targetColumn] = 2
    else:
        print("Error")

    board[row][column] = 0

    return piece


def undoMove(piece, move, player):
    row, column = piece
    playedRow, playedColumn = move

    if player == "Computer":
        board[row][column] = 1
    elif player == "Player":
        board[row][column] = 2

    board[playedRow][playedColumn] = 0
    

def checkWinner():

    computerPieces = 0
    playerPieces = 0

    for row in board:
        for val in row:
            if val == 1:
                computerPieces += 1
            elif val == 2:
                playerPieces += 1

    if computerPieces == 0:
        return "Player"
    
    if playerPieces == 0:
        return "Computer"

    if turn == 50:
        if computerPieces == playerPieces:
            return "Draw"
        elif computerPieces > playerPieces:
            return "Computer"
        elif computerPieces < playerPieces:
            return "Player"

    return False


def minimax(depth, isMaximizingPlayer, treeDepth = 0):  # Maximizing player is ai

    if depth == 0 or checkWinner() != False:
        return evaluateBoard()

    if isMaximizingPlayer:
        maxEval = -math.inf
        #temp = -math.inf
        possibleMoves = findAllPossibleMoves("Computer")

        for piece, row, column in possibleMoves:

            #print(board)

            makeMove(piece, (row,column), "Computer")
            #print(f"Computer made move: ({piece}), {row}, {column}")
            deletedPieces = checkCapture()

            #if deletedPieces:
                #print(f"DeletedPieces: {deletedPieces}")

            eval = minimax(depth - 1, False, treeDepth + 1)

            #print(eval)

            undoCapture(deletedPieces)
            undoMove(piece, (row,column), "Computer")

            #maxEval = max(maxEval, eval)

            #if deletedPieces:
                #print(f"Board after undoes: {board}")

            if treeDepth == 0 and eval > maxEval:
                maxEval = eval
                global bestMove
                bestMove = (piece, row, column)
                #print(f"Best Move: {bestMove}")
                #temp = maxEval
                
            elif eval > maxEval:
                maxEval = eval

        return maxEval
    
    else:
        minEval = math.inf
        possibleMoves = findAllPossibleMoves("Player")

        for piece, row, column in possibleMoves:

            #print(board)
            
            makeMove(piece, (row,column), "Player")
            #print(f"Player made move: ({piece}), {row}, {column}")
            deletedPieces = checkCapture()

            #if deletedPieces:
                #print(f"DeletedPieces: {deletedPieces}")

            eval = minimax(depth - 1, True, treeDepth + 1)
            #print(eval)

            undoCapture(deletedPieces)
            undoMove(piece, (row,column), "Player")
            minEval = min(minEval, eval)

        return minEval


def computerMove():
    
    global bestMove

    res = minimax(5, True)

    if bestMove:    
        makeMove(bestMove[0], (bestMove[1], bestMove[2]), "Computer")
    else:
        print("No valid move")

    print("Best Value: ", res)
    print("------------------------")

    bestMove = None
    
    '''global computerTurnCounter
    computerTurnCounter += 1

    if (computerTurnCounter != 2):
        computerMove()'''



pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()

backSurface = pygame.Surface((width, height))


while turn <= 50:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and turn != 0:
            mouseX, mouseY = pygame.mouse.get_pos()
            mouseX = mouseX // 100
            mouseY = mouseY // 100
            if board[mouseY][mouseX] == 2:

                if len(playerSelectedPieceArr) != 0:
                    for piece in playerSelectedPieceArr:
                        if piece != (mouseY, mouseX):
                            selectedPiece = mouseY, mouseX
                else:
                    selectedPiece = mouseY, mouseX
                    
                for i, row in enumerate(board):
                    for j, val in enumerate(row):
                        if(val == 3):
                            board[i][j] = 0

            elif board[mouseY][mouseX] == 3:

                '''circleCount = 0

                for i, row in enumerate(board):
                    for j, val in enumerate(row):
                        if board[i][j] == 2:
                            circleCount += 1'''

                MoveSelectedPiece(selectedPiece, mouseX, mouseY)
                checkCapture()
                #playerTurnCounter += 1

                #if playerTurnCounter == 2 or circleCount < 2:
                #playerTurnCounter = 0
                turn += 1
                turnToPlay = "Computer"
                playerSelectedPieceArr.clear()
                
                
                if turnToPlay == "Computer":
                    computerMove()
                    checkCapture()
                    turn += 1
                    computerTurnCounter = 0
                    turnToPlay = "Player"


                selectedPiece = None

        elif event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
            computerMove()
            checkCapture()
            #computerTurnCounter = 0
            turn += 1
            turnToPlay = "Player"

           

    backSurface.fill('white')            

    drawBoard()
    drawPieces()

    if selectedPiece:
        findPossibleMoves(selectedPiece)
        drawPossibleMoves()

    screen.blit(backSurface, (0,0))
    pygame.display.update()
    #clock.tick(60)



print("Game over ", turn)