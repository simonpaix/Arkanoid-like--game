#dev: Mariana Simon Paixão
#year: 2011

# -*- coding: cp1252 -*-



import pygame, sys
from pygame import mixer
from tkinter import *
import random
import time

#pygame.init()

# ------------------Sound Music Mixer Code --------------------------
#pygame.mixer.init(44100, -16,2,2048)# setup mixer to avoid sound lag


#sounds:
def soundSetup():
  try:
      pygame.mixer.music.load('media/airplane-landing.wav')#load music
      touchBRICK= pygame.mixer.Sound('media/crash.wav')
      touchRACKET=pygame.mixer.Sound('media/slap.wav')
      BALLout= pygame.mixer.Sound('media/fire.wav')
      lostGame= pygame.mixer.Sound('media/scream.wav')
      wonGame=  pygame.mixer.Sound('media/thunder.wav')

  except:
    errorHandle()
     

def errorHandle():
   print ("error: sound not available ")
   pass


def gameSetup():
    global x,y,colourCount,x1,y1,RACKET,BALL,TEXT1,TEXT2,TEXT3,WIDTH_CANVAS,HEIGHT_CANVAS,WIDTH_RACKET,HEIGHT_RACKET,DISTANCE_Y_RACKET,BRICKS_PER_ROW,ROWS_OF_BRICKS,ESPACE_BETWEEN_BRICKS,WIDTH_BRICK,HEIGHT_BRICK,BALL_RADIUS,DISTANCE_Y_BRICK,LIFES,DELAY,BRICKS,x0,x,y,vy,vx,ACCELERATION
     

    # RACKET dimensions
    WIDTH_RACKET = 60
    HEIGHT_RACKET = 10

    #  RACKET distance
    DISTANCE_Y_RACKET = 30

    # BRICKs per row
    BRICKS_PER_ROW = 10

    # rows
    ROWS_OF_BRICKS = 10

    # espace
    ESPACE_BETWEEN_BRICKS = 4

    # WIDTH  BRICK
    WIDTH_BRICK = (WIDTH_CANVAS - (BRICKS_PER_ROW - 1) *
    ESPACE_BETWEEN_BRICKS) / BRICKS_PER_ROW

    # HEIGHT  BRICK
    HEIGHT_BRICK = 8

    #  ball radius in pixels
    BALL_RADIUS = 10

    # DISTANCE from top
    DISTANCE_Y_BRICK = 70

    # tries
    LIFES = 3

    #delay
    DELAY = 0.01

    #total bricks in canvas
    BRICKS= BRICKS_PER_ROW* ROWS_OF_BRICKS   

    # x0 is coordinate x of first row, remains constant
    x0= (WIDTH_CANVAS - WIDTH_BRICK * BRICKS_PER_ROW -
    (BRICKS_PER_ROW-1)*ESPACE_BETWEEN_BRICKS)/2.0

    #x is initialized with x0, but increases to create new bricks
    x = x0
    y = DISTANCE_Y_BRICK



    #speed components, BALL:
    vy = 3

    vx = random.uniform(1.0, 3.0)
    if random.choice([True, False])==True:
        vx = -vx
    #BALL acceleration when it touches a  BRICK:
    ACCELERATION=1.02

    colourCount=0
    
    #cleans canvas for a new game
    canvas.delete('all')

    #build BRICKs rows:
    for i in range (ROWS_OF_BRICKS):
        for j in range(BRICKS_PER_ROW) :
            colours=['red','orange','yellow','green','cyan']
            colour= colours[colourCount]
            canvas.create_rectangle( x,y, x + WIDTH_BRICK,y+HEIGHT_BRICK,fill=colour)
            x= x + ESPACE_BETWEEN_BRICKS + WIDTH_BRICK
        x=x0
        y= y+ ESPACE_BETWEEN_BRICKS + HEIGHT_BRICK
        if i%2!=0:    #a colour muda nas linhas ímpares,
            colourCount+=1      # ou seja, ela muda a cada 2 linhas

    #Create RACKET:
    x1= (WIDTH_CANVAS-WIDTH_RACKET)/2
    y1= HEIGHT_CANVAS - DISTANCE_Y_RACKET
    RACKET = canvas.create_rectangle(x1,y1,x1+WIDTH_RACKET,y1-HEIGHT_RACKET,fill='black')

    #Create BALL:
    BALL= canvas.create_oval(WIDTH_CANVAS/2 - BALL_RADIUS,HEIGHT_CANVAS/2-BALL_RADIUS,
                       WIDTH_CANVAS/2+BALL_RADIUS, HEIGHT_CANVAS/2+BALL_RADIUS, fill='black')

    #TEXT instructions:
    TEXT1= canvas.create_text(WIDTH_CANVAS/2 , HEIGHT_CANVAS/2 +2*BALL_RADIUS+ 20,
                                       font=('Times New Roman', 26),
                                       text = 'Click to start',)

    #remaining BRICKS:
    TEXT2 = canvas.create_text( ESPACE_BETWEEN_BRICKS,
                             HEIGHT_CANVAS-ESPACE_BETWEEN_BRICKS,
                             text = 'BRICKS: %3d ' % (BRICKS),
                             anchor=SW, font=('Times New Roman', 14),fill='maroon')

    #remaining LIFEs:
    TEXT3= canvas.create_text( WIDTH_CANVAS-ESPACE_BETWEEN_BRICKS, HEIGHT_CANVAS- ESPACE_BETWEEN_BRICKS,
                                text=  'LIFES: ' + str(LIFES), anchor=SE, font=('Times New Roman', 14),fill='blue')
    

    
    


def StartedRound():
    global BALL, LIFES,vy,vx,BRICKS
    while BRICKS!=0:
        moveBALL()
        verifiesObjCollision()
        if getY(BALL)>=HEIGHT_CANVAS:
            LIFES-=1
            canvas.itemconfig(TEXT3, text = 'LIFES: ' + str(LIFES))
            #BALLout.play()
            if LIFES!=0:
                canvas.delete(BALL)
                BALL= canvas.create_oval(WIDTH_CANVAS/2 - BALL_RADIUS,HEIGHT_CANVAS/2-BALL_RADIUS,
                           WIDTH_CANVAS/2+BALL_RADIUS, HEIGHT_CANVAS/2+BALL_RADIUS, fill='black')
                vy=3
                vx=random.uniform(1.0, 3.0)
                if random.choice([True, False])==True:
                    vx = -vx
                break 
            else:
                gameOver()
                break
    if BRICKS==0:
        gameWon()
        

def moveBALL():
    global vx,vy
    canvas.move(BALL, vx,vy)
    canvas.update() 
    time.sleep(DELAY)
    if getY(BALL)<=2*BALL_RADIUS:
        vy=-vy
    elif getX(BALL) <= 2*BALL_RADIUS or getX(BALL)>=WIDTH_CANVAS:
        vx=-vx
        
 
    


def getX(object):
    [x0, y0, x1, y1] = canvas.coords(object)
    return x1

def getY(object):
    [x0, y0, x1, y1] = canvas.coords(object)
    return y1
        
def movedMouse(e):
    global x1
    canvas.move(RACKET, e.x-WIDTH_RACKET/2 - x1 ,0 ) #moves RACKET horizontally
    x1=e.x-WIDTH_RACKET/2    
    if getX(RACKET)>=WIDTH_CANVAS:
        canvas.move(RACKET,WIDTH_CANVAS - getX(RACKET),0)
        x1=WIDTH_CANVAS-WIDTH_RACKET #RACKET never goes beyond canvas width  on the right
    elif getX(RACKET) <=WIDTH_RACKET: #RACKET nnever goes   beyond canvas width on the left 
        canvas.move(RACKET, WIDTH_RACKET - getX(RACKET),0)
        x1=0

def clickedMouse(e): 
    global TEXT1
    canvas.delete(TEXT1)
    if not gameOver() and not gameWon():
        StartedRound()

    else:
      gameSetup()

      
    
def verifiesObjCollision():
    global vy, BRICKS
    objCollision = detectsCollisions()
    if objCollision != None:
        vy=-vy *ACCELERATION
        if objCollision != RACKET:
            canvas.delete(objCollision)
            #touchBRICK.play()
            BRICKS-=1
            canvas.itemconfig(TEXT2, text = 'BRICKS: %3d ' % (BRICKS))
        else:
            dif = getY(BALL)- (HEIGHT_CANVAS- DISTANCE_Y_RACKET - HEIGHT_RACKET) 
            canvas.move(BALL,0, -dif)               
            #touchRACKET.play()
    
        

def detectsCollisions():
    global list
    [xb0, yb0, xb1, yb1] = canvas.coords(BALL)
    list = canvas.find_overlapping(xb0, yb0, xb1, yb1)
    if len(list)>1:
        if list[0] != BALL  and list[0] != TEXT2 and list[0] !=TEXT3:
            return list [0]
    else:
        return None

def gameWon():
    if BRICKS==0:
        canvas.delete(BALL)    
        canvas.create_text(WIDTH_CANVAS/2, HEIGHT_CANVAS/2,
                                           font=('Comic Sans', 26),
                                           text = 'Congrats,',fill='pink')

        canvas.create_text(WIDTH_CANVAS/2, HEIGHT_CANVAS/2+ 100,
                                           font=('Comic Sans', 26),
                                           text = 'You are awesome!!',fill='pink')

        canvas.create_text(WIDTH_CANVAS/2,HEIGHT_CANVAS/2 +200,
                                           text = 'click to restart..',
                                           font=('Comic Sans', 14))
        #wonGame.play()
        return True

def gameOver():
    if LIFES==0:
        canvas.delete(BALL)
        canvas.create_text(WIDTH_CANVAS/2, HEIGHT_CANVAS/2,
                                       font=('Courrier', 36),
                                       text = 'GAME OVER')
        #lostGame.play()
        return True

#def playsSound(file):
 #   PlaySound(file, SND_FILENAME|SND_ASYNC)


def canvasSetup():
  global canvas, WIDTH_CANVAS, HEIGHT_CANVAS
  # canvas dimensions
  WIDTH_CANVAS = 400
  HEIGHT_CANVAS = 600



  canvas = Canvas(width=WIDTH_CANVAS, height=HEIGHT_CANVAS,
  background='white')
  canvas.pack(fill=BOTH,expand=YES)
  canvas.bind("<Motion>", movedMouse)
  canvas.bind("<ButtonPress>", clickedMouse)


def main():

  canvasSetup()
  soundSetup()
  gameSetup()


main()

mainloop()
