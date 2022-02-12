import random
import copy
import numpy as np

def doesEmptyExist(grid):
    for i in range(4):
        for j in range(4):
            if(grid[i][j] == 0):
                return True
    return False

# 
def NextMoveMinimax(grid: list, depth: int, step: int, debug=False):
    if(depth <= 0): return (-1, grid)
    if(debug):
        print(f'function NextMoveMinimax depth: {depth}')
    # print('current board:')
    # printBoard(grid)
    startingUtility = findUtility(grid)

    # LEVEL +1 EXPAND OUR MOVES
    boardLeft = copy.deepcopy(grid)
    boardRight = copy.deepcopy(grid)
    boardUp = copy.deepcopy(grid)
    boardDown = copy.deepcopy(grid)
    goLeft(boardLeft)
    goRight(boardRight)
    goDown(boardDown)
    goUp(boardUp)


    uLeft = findUtility(boardLeft)
    uRight = findUtility(boardRight)
    uUp = findUtility(boardUp)
    uDown = findUtility(boardDown)

    if(uLeft == uRight and uLeft == uUp and uLeft == uDown and uLeft == startingUtility):
        # print('GAME OVER, BOARD CANNOT BE CHANGED')
        return (-100, grid)

    # TO EACH LEVEL +1 MOVES, MIN GOES NOW
    leftMinResult = minPlayerMoves(boardLeft, 0)
    rightMinResult = minPlayerMoves(boardRight, 0)
    upMinResult = minPlayerMoves(boardUp, 0)
    downMinResult = minPlayerMoves(boardDown, 0)

    if(debug):
        printBoards([boardLeft, boardRight, boardUp, boardDown])

    nextUtilityLeft = 1
    nextUtilityRight = 1
    nextUtilityUp = 1
    nextUtilityDown = 1

    if(leftMinResult == 0):
        # print('min player couldn\'t move on left')
        nextUtilityLeft = -1
    if(rightMinResult == 0):
        # print('min player couldn\'t move on right')
        nextUtilityRight = -1
    if(upMinResult == 0):
        # print('min player couldn\'t move on up')
        nextUtilityUp = -1
    if(downMinResult == 0):
        # print('min player couldn\'t move on down')
        nextUtilityDown = -1

    if(nextUtilityLeft > 0):
        if(debug):
            print(f'--depth {depth} NextMoveMinimax is called on Left')
        recursiveLeft = NextMoveMinimax(boardLeft, depth-1, step+1)
        nextUtilityLeft = findUtility(recursiveLeft[1])
        if(debug):
            print(f'--depth {depth} NextMoveMinimax on Left maxUtility is {nextUtilityLeft}')

    if(nextUtilityRight > 0):
        if(debug):
            print(f'--depth {depth} NextMoveMinimax is called on Right')
        recursiveRight = NextMoveMinimax(boardRight, depth-1, step+1)
        nextUtilityRight = findUtility(recursiveRight[1])
        if(debug):
            print(f'--depth {depth} NextMoveMinimax on Right maxUtility is {nextUtilityRight}')


    if(nextUtilityUp > 0):
        if(debug):
            print(f'--depth {depth} NextMoveMinimax is called on Up')
        recursiveUp = NextMoveMinimax(boardUp, depth-1, step+1)
        nextUtilityUp = findUtility(recursiveUp[1])
        if(debug):
            print(f'--depth {depth} NextMoveMinimax on Up maxUtility is {nextUtilityUp}')


    if(nextUtilityDown > 0):
        if(debug):
            print(f'--depth {depth} NextMoveMinimax is called on Down')
        recursiveDown = NextMoveMinimax(boardDown, depth-1, step+1)
        nextUtilityDown = findUtility(recursiveDown[1])
        if(debug):
            print(f'--depth {depth} NextMoveMinimax on Down maxUtility is {nextUtilityDown}')

    
    if(debug):
        print(f' -----depth {depth} about to make a decision:')
        print(f'nextUtilityLeft: {nextUtilityLeft}')
        print(f'nextUtilityRight: {nextUtilityRight}')
        print(f'nextUtilityUp: {nextUtilityUp}')
        print(f'nextUtilityDown: {nextUtilityDown}')

    # 0 = UP
    # 1 = DOWN
    # 2 = LEFT
    # 3 = RIGHT
    if(nextUtilityLeft >= nextUtilityRight and nextUtilityLeft >= nextUtilityUp and nextUtilityLeft >= nextUtilityDown):
        return (2, recursiveLeft[1])
    
    if(nextUtilityRight >= nextUtilityLeft and nextUtilityRight >= nextUtilityUp and nextUtilityRight >= nextUtilityDown):
        return (3, recursiveRight[1])
    
    if(nextUtilityUp >= nextUtilityLeft and nextUtilityUp >= nextUtilityDown and nextUtilityUp >= nextUtilityRight):
        return (0, recursiveUp[1])
    
    if(nextUtilityDown >= nextUtilityUp and nextUtilityDown >= nextUtilityLeft and nextUtilityDown >= nextUtilityRight):
        return (1, recursiveDown[1])
    
    # error
    return (55, board)
        


def NextMove(grid: list,step: int)->int:
    # once achieved 8192, end the game and rest, you have done enough.
    if(grid[0][3] >= 8192 and grid[0][2] >= 16):
        return 4
    if(grid[0][3] >= 2048 and grid[0][2] >= 512):
        return NextMoveMinimax(grid, 3, step, False)[0]

    return NextMoveMinimax(grid, 2, step, False)[0]
   

def goRight(grid):
    cols = [2,1,0]
    mergedThisStep = {}
    for row in range(4):
        for col in cols:
            if(grid[row][col] == 0):
                continue
            currCol = col
            while(currCol < 3 and grid[row][currCol+1] == 0):
                grid[row][currCol+1] = grid[row][currCol]
                grid[row][currCol] = 0
                currCol+=1
            if(currCol !=3 and grid[row][currCol+1] == grid[row][currCol] and (row,currCol+1) not in mergedThisStep):
                grid[row][currCol+1] = 2* grid[row][currCol]
                grid[row][currCol] = 0
                mergedThisStep[(row,currCol+1)] = 1

    


def goLeft(grid):
    cols = [1,2,3]
    mergedThisStep = {}
    for row in range(4):
        for col in cols:
            if(grid[row][col] == 0):
                continue
            currCol = col
            while(currCol > 0 and grid[row][currCol-1] == 0):
                grid[row][currCol-1] = grid[row][currCol]
                grid[row][currCol] = 0
                currCol-=1
            if(currCol != 0 and grid[row][currCol-1] == grid[row][currCol] and (row,currCol-1) not in mergedThisStep):
                grid[row][currCol-1] = 2* grid[row][currCol]
                grid[row][currCol] = 0
                mergedThisStep[(row,currCol-1)] = 1

def goUp(grid):
    rows = [1,2,3]
    mergedThisStep = {}
    for col in range(4):
        for row in rows:
            if(grid[row][col] == 0):
                continue
            currRow = row
            while(currRow > 0 and grid[currRow-1][col] == 0):
                grid[currRow-1][col] = grid[currRow][col]
                grid[currRow][col] = 0
                currRow-=1
            if(currRow !=0 and grid[currRow-1][col] == grid[currRow][col] and (currRow-1, col) not in mergedThisStep):
                grid[currRow-1][col] = 2*grid[currRow-1][col]
                grid[currRow][col] = 0
                mergedThisStep[(currRow-1, col)] = 1

    

def goDown(grid):
    rows = [2,1,0]
    mergedThisStep = {}
    for col in range(4):
        for row in rows:
            if(grid[row][col] == 0):
                continue
            currRow = row
            while(currRow < 3 and grid[currRow+1][col] == 0):
                grid[currRow+1][col] = grid[currRow][col]
                grid[currRow][col] = 0
                currRow+=1
            if(currRow != 3 and grid[currRow+1][col] == grid[currRow][col] and (currRow+1, col) not in mergedThisStep):
                grid[currRow+1][col] = 2*grid[currRow+1][col]
                grid[currRow][col] = 0
                mergedThisStep[(currRow+1, col)] = 1
    

def initGame():
    board = [
    # 0 1 2 3
        [0,0,0,0],
    # 4 5 6 7
        [0,0,0,0],
    # 8 9 10 11
        [0,0,0,0],
    # 12 13 14 15
        [0,0,0,0]
    ]
    addValue(board, 2)
    addValue(board, 2)
    # printBoard(board)
    # print(findUtility(board))
    return board

def printBoard(grid):
    for i in grid:
        print(i)

def printBoards(grids):
    topString = ""
    for i in range(len(grids)):
        topString += f'board{i}:\t   \t'
    print(topString)
    for rows in range(4):
        for i in grids:
            print(i[rows] ,end='\t')
        print()

def findUtility(grid):
    cellMultipliers = {
        3: 8192*16 + 29,
        2: 8192*8 + 27,
        1: 8192*4 + 25,
        0: 8192*2 + 23,
        4: 8192 + 21,
        5: 4096 + 19,
        6: 2048 + 17,   
        7: 1024 + 15,
        11: 256 + 13,
        10: 128 + 11,
        9: 64 + 9, 
        8: 32 + 7,
        12: 16 + 5,
        13: 8 + 3,
        14: 2*2 + 1,
        15: 2
    }
    score = 0
    for i in range(16):
        score+=cellMultipliers[i]*grid[i//4][i%4]
    
    for i in [1,2,3,5,6,7,9,10,11]:
        if(grid[i//4 - 1][i%4] ==  grid[i//4][i%4] ):
            score+=grid[i//4][i%4]**2
        if(grid[i//4][i%4 - 1] ==  grid[i//4][i%4] ):
            score+=grid[i//4][i%4]**2
    
    return score


# finds a empty slot, inserts a value there
def addValue(grid, val):
    # print(f'function addValue')
    possibleSlots = []
    ind = 0
    for i in grid:
        for j in i:
            if(j == 0):
                possibleSlots.append(ind)
            ind+=1
    
    print(f'possible slots to insert {val}: {possibleSlots}')
    # if no empty slot, return -1
    if(len(possibleSlots) == 0):
        return -1
     
    indexToInsert = np.random.choice(possibleSlots)
    print(indexToInsert)
    grid[indexToInsert//4][indexToInsert%4] = val
    return 1

# works like addValue, but always inserts a 2 to the smallest possible cell
def minPlayerMoves(grid, missesWanted = 0):
    missed = 0
    for i in [3,2,1,0,  4,5,6,7,  8,9,10,11,   12,13,14,15]:
        if(grid[i//4][i%4] == 0):
            if(missesWanted == missed):
                grid[i//4][i%4] = 2
                return 1
            else:
                missed+=1
    
    return 0

def playGame():
    print('function playGame')
    
    # while(True):
    #     printBoard(board)
    #     print(f"Press Key to pick move, level: {numMoves}")
    #     userKey = input() 
    #     print(userKey)
    #     # 0 = UP
    #     # 1 = DOWN
    #     # 2 = LEFT
    #     # 3 = RIGHT
    #     if(userKey == "0"):
    #         goUp(board)
    #     elif(userKey == "1"):
    #         goDown(board)
    #     elif(userKey == "2"):
    #         goLeft(board)
    #     elif(userKey == "3"):
    #         goRight(board)
    #     addValue(board, 2)
    #     numMoves+=1

if  __name__ == "__main__":
    numMoves = 0
    board = [
        [0, 0, 0, 0],
        [0, 0, 2, 0],
        [0, 4, 2, 0],
        [0, 0, 0, 0],

        # [16, 1024, 2048, 4096],
        # [256, 128, 64, 32],
        # [8, 16, 32, 4],
        # [0, 2, 2, 4],

        # [16, 1024, 2048, 4096],
        # [256, 128, 64, 32],
        # [8, 16, 32, 8],
        # [4, 4, 2, 0]

    ]
    # printBoard(board)
    # print(findUtility(board))
    # exit(1)

    print('starting board:')
    printBoard(board)
    suggestedMove = NextMove(board, numMoves)
    print(f'--------------------NextMoveMinmax returned {suggestedMove}')




    while(True):

        print(f'\n----- STEP {numMoves} -----\n')

        suggestedMove = NextMove(board, numMoves)
        
        printBoard(board)
        print(f'NextMoveMinmax returned {suggestedMove}')
        
        # input()

        # 0 = UP
        # 1 = DOWN
        # 2 = LEFT
        # 3 = RIGHT
        if(suggestedMove == 0):
            goUp(board)
        elif(suggestedMove == 1):
            goDown(board)
        elif(suggestedMove == 2):
            goLeft(board)
        elif(suggestedMove == 3):
            goRight(board)
        else:
            print("ERROR HAPPENED!")
            printBoard(board)
            exit(0)
        addValue(board, 2)
        numMoves+=1
