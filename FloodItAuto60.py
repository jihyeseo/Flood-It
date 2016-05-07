#
# In development by Jihye Sofia Seo https://www.linkedin.com/in/jihyeseo
# forked from the code of Al Sweigart  
# http://inventwithpython.com/pygame/chapter10.html 
# whose books are very helpful for learning Python and PyGame. Many thanks!
# Main change is that his version uses flood fill algorithm, which could not run for large boards.
# This file modified the algorithm. 
#
# Flood-It is an NP hard problem http://arxiv.org/abs/1001.4420 for 3 colors or more. 
# The goal of this project is to find an efficient algorithm for autoplay.
#
# Any comments are welcome at jihyeseo@post.harvard.edu 
# upload: May 7 2016 Berlin Germany
#

import random, sys, webbrowser, copy, pygame
from pygame.locals import *
 
#sys.setrecursionlimit(1000000)
 
#FPS = 30
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
boxSize = 20
PALETTEGAPSIZE = 5
PALETTESIZE = 30
 
boardWidth = 30
boardHeight = 30 

# Creates a board data structure with random colors for each box.
board = []


conqueredAt = [[False for y in range(boardHeight)] for x in range(boardWidth)] 
neverQueue = [[False for y in range(boardHeight)] for x in range(boardWidth)] 
 
conqueredAt[0][0] = True 


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


maxDepth = [0,0,0]

def buildQueue(): # add only boundaries
    floodQueue = Queue()  
    for x in range(boardWidth):
        for y in range(boardHeight):
            if (neverQueue[x][y] == False) & (conqueredAt[x][y] == True): 
                noFrontier = True 
                if (x > 0) :
                    noFrontier = noFrontier & (conqueredAt[x-1][y]) 
                if (x < boardWidth - 1):
                    noFrontier = noFrontier & (conqueredAt[x+1][y]) 
                if (y > 0):
                    noFrontier = noFrontier & (conqueredAt[x][y-1])
                if (y < boardHeight - 1):
                    noFrontier = noFrontier & (conqueredAt[x][y+1])                     
                if noFrontier :
                    neverQueue[x][y] = True
                else: 
                    floodQueue.enqueue([x, y])     
                    
    return floodQueue
        
#            R    G    B
WHITE    = (255, 255, 255)
DARKGRAY = ( 70,  70,  70)
BLACK    = (  0,   0,   0)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
# The first color in each scheme is the background color, the next six are the palette colors.
COLORSCHEMES = ((150, 200, 255),   
                (97, 215, 164)  ,  #lightGr  
                (23, 149, 195) , # light ocean 
                (147, 3, 167) , # purple
                (241, 109, 149), # jindalle 
                (255, 180, 115), # tangerine
                (166, 147, 0)     # tangerine?  
                )
bgColor = COLORSCHEMES[0]
paletteColors =  COLORSCHEMES[1:]
counters = []

def main():
    global FPSCLOCK, DISPLAYSURF
    
    counter = 0
    
    
    pygame.init() 
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Flood it')
    generateRandomBoard(boardWidth, boardHeight)
    lastPaletteClicked = None

    while True: # main game loop
        paletteClicked = None

        # Draw the screen.
        DISPLAYSURF.fill(bgColor) 
        drawBoard() 
        drawPalettes()
        pygame.display.update()
        
        for event in pygame.event.get(KEYUP): # get all the KEYUP events
            if event.key == K_ESCAPE:
                pygame.quit() # terminate if the KEYUP event was for the Esc key
                sys.exit()          
            elif event.key == K_1:
                paletteClicked = 0   
            elif event.key == K_2:
                paletteClicked = 1 
            elif event.key == K_3:
                paletteClicked = 2  
            elif event.key == K_4:
                paletteClicked = 3  
            elif event.key == K_5:
                paletteClicked = 4  
            elif event.key == K_6:
                paletteClicked = 5                   
          #  pygame.event.post(event) # put the other KEYUP event objects back
        
        paletteClicked = computerPicks() 
        pygame.time.wait(200)
        if paletteClicked != None and paletteClicked != lastPaletteClicked:
            # a palette button was clicked that is different from the
            # last palette button clicked (this check prevents the player
            # from accidentally clicking the same palette twice)
            lastPaletteClicked = paletteClicked
            #if board[0][0] != paletteClicked  :            
            if floodFill(board[0][0], paletteClicked, buildQueue()):
                counter += 1  
                counters.append(counter)
                print(counter, maxDepth)
            else :  
                counters.append(counter)
                print(counters)
            drawBoard()
            pygame.display.update()
         #   FPSCLOCK.tick(FPS) 
       # pygame.display.update()
        #FPSCLOCK.tick(FPS)

def computerPicks():  
    x = maxDepth[1] 
    y = maxDepth[2]
    if (x < 28 ) & (y < 28):    
        if x > y :
            for inc in range(3):
                if board[x][y] != board[x][y+inc]:
                    return board[x][y+inc]
        for inc in range(3):
            if board[x][y] != board[x+inc][y]:
                return board[x+inc][y]
        return board[x + random.randint(0,2)][y+random.randint(0,2)]
    else:
        return None
    
def generateRandomBoard(width, height):    
    for x in range(width):
        column = []
        for y in range(height): 
            column.append(random.randint(0, len(paletteColors) - 1))
        board.append(column) 

def drawBoard():
    for x in range(boardWidth):
        for y in range(boardHeight):
            left, top = leftTopPixelCoordOfBox(x, y) 
            pygame.draw.rect(DISPLAYSURF, (paletteColors[board[x][y]]), (left, top, boxSize, boxSize))
    DISPLAYSURF.blit(DISPLAYSURF, (0, 0))

def drawPalettes():
    # Draws the six color palettes at the left of the screen.
    numColors = len(paletteColors)
    textSize = 30
    font = pygame.font.Font(None, textSize)
    for i in range(numColors):
        top = 10 + (i * PALETTESIZE) + (i * PALETTEGAPSIZE)
        left = 10
        pygame.draw.rect(DISPLAYSURF, paletteColors[i], (left, top, PALETTESIZE, PALETTESIZE))
        textImg = font.render( str((i+1) % 10), 1, bgColor)
        DISPLAYSURF.blit( textImg, (left+10 +0*(PALETTESIZE/2-textSize/2),top+7 +0*(PALETTESIZE/2-textSize/2)))
        
def floodFill(teamColor, newColor, queue): 
    changed = False 
    while(queue.isEmpty() == False):
        checkHere = queue.dequeue()      
        (x,y) = (checkHere[0],checkHere[1])
      
        board[x][y] = newColor 
        conqueredAt[x][y] = True   
        
        if x > 0 :
            (X,Y) = (x-1,y) 
            if (board[X][Y] == teamColor) & (conqueredAt[X][Y] == False): 
                queue.enqueue([X, Y]) # on box to the left
                changed = True
        if x < boardWidth - 1:
            (X,Y) = (x+1,y) 
            if (board[X][Y] == teamColor) & (conqueredAt[X][Y] == False): 
                queue.enqueue([X, Y])     # on box to the right
                changed = True
                if (maxDepth[0] < x+1+y) & ( x - y < 5) & (y - x <5 ) :
                    maxDepth[0] = x+1+y
                    maxDepth[1] = x+1
                    maxDepth[2] = y
        if y > 0:
            (X,Y) = (x,y-1) 
            if (board[X][Y] == teamColor) & (conqueredAt[X][Y] == False): 
                queue.enqueue([X, Y])   # on box to up
                changed = True
        if y < boardHeight - 1:
            (X,Y) = (x,y+1) 
            if (board[X][Y] == teamColor) & (conqueredAt[X][Y] == False): 
                queue.enqueue([X, Y])         # on box to down
                changed = True
                if (maxDepth[0] < x+1+y)  & ( x - y < 5) & (y - x < 5 ):
                    maxDepth[0] = x+1+y
                    maxDepth[1] = x
                    maxDepth[2] = y+1
    for x in range(boardWidth):
        for y in range(boardHeight):
            if conqueredAt[x][y] == True :
                board[x][y] = newColor
    return changed 

def leftTopPixelCoordOfBox(boxx, boxy):
    # Returns the x and y of the left-topmost pixel of the xth & yth box.
    xmargin = int((WINDOWWIDTH - (boardWidth * boxSize)) / 2 + 23)
    ymargin = int((WINDOWHEIGHT - (boardHeight * boxSize)) / 2 )
    return (boxx * boxSize + xmargin, boxy * boxSize + ymargin)

if __name__ == '__main__':
    main()
