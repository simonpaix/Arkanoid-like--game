#Nome : Mariana Simon Paixão
#Ano: 2011

# -*- coding: cp1252 -*-


from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from Tkinter import *
import random
import time

# dimensoes do canvas
LARGURA_CANVAS = 400
ALTURA_CANVAS = 600

# dimensoes da raquete
LARGURA_RAQUETE = 60
ALTURA_RAQUETE = 10

# distancia da raquete ao chao
DISTANCIA_Y_RAQUETE = 30

# numero de tijolos por linha
TIJOLOS_POR_LINHA = 10

# número de linhas de tijolos
LINHAS_DE_TIJOLOS = 10

# separação entre tijolos
SEPARACAO_ENTRE_TIJOLOS = 4

# largura de um tijolo
LARGURA_TIJOLO = (LARGURA_CANVAS - (TIJOLOS_POR_LINHA - 1) *
SEPARACAO_ENTRE_TIJOLOS) / TIJOLOS_POR_LINHA

# altura de um tijolo
ALTURA_TIJOLO = 8

# raio da bola em pixels
RAIO_BOLA = 10

# distancia da linha de tijolos superior ao topo
DISTANCIA_Y_TIJOLO = 70

# número de tentativas
TENTATIVAS = 3

#intervalo de animação
DELAY = 0.01

#número de tijolos no canvas
TIJOLOS= TIJOLOS_POR_LINHA* LINHAS_DE_TIJOLOS   

# xo é a coordenada x da coluna 1, permanece constante
x0= (LARGURA_CANVAS - LARGURA_TIJOLO * TIJOLOS_POR_LINHA -
(TIJOLOS_POR_LINHA-1)*SEPARACAO_ENTRE_TIJOLOS)/2.0

#x começa com o valor de x0 mas é incrementado para dar origem a novos tijolos
x = x0
y = DISTANCIA_Y_TIJOLO

#contador que determina a cor da linha de retangulos, a partir da lista
n = 0 

#componentes da velocidade da bola:
vy = 3

vx = random.uniform(1.0, 3.0)
if random.choice([True, False])==True:
    vx = -vx
#aceleração da bola ao tocar nos tijolos:
ACELERACAO=1.02

#sons do jogo:

tocouTIJOLO= 'C:\Windows\Media\Savanna\Windows Default.wav'
tocouRAQUETE='C:\Windows\Media\Windows User Account Control.wav' 
BOLAfora= "C:\Windows\Media\Speech Sleep.wav"
perdeuJogo= "C:\Windows\Media\Raga\Windows Critical Stop.wav"
ganhouJogo= "C:\Windows\Media\tada.wav"


def setup():
    global x,y,n,x1,y1,RAQUETE,BOLA,TEXTO1,TEXTO2,TEXTO3

    #Construir as linhas de tijolos:
    for i in range (LINHAS_DE_TIJOLOS):
        for j in range(TIJOLOS_POR_LINHA) :
            cores=['red','orange','yellow','green','cyan']
            cor= cores[n]
            canvas.create_rectangle( x,y, x + LARGURA_TIJOLO,y+ALTURA_TIJOLO,fill=cor)
            x= x + SEPARACAO_ENTRE_TIJOLOS + LARGURA_TIJOLO
        x=x0
        y= y+ SEPARACAO_ENTRE_TIJOLOS + ALTURA_TIJOLO
        if i%2!=0:    #a cor muda nas linhas ímpares,
            n+=1      # ou seja, ela muda a cada 2 linhas

    #Criar a raquete:
    x1= (LARGURA_CANVAS-LARGURA_RAQUETE)/2
    y1= ALTURA_CANVAS - DISTANCIA_Y_RAQUETE
    RAQUETE = canvas.create_rectangle(x1,y1,x1+LARGURA_RAQUETE,y1-ALTURA_RAQUETE,fill='black')

    #Criar a bola:
    BOLA= canvas.create_oval(LARGURA_CANVAS/2 - RAIO_BOLA,ALTURA_CANVAS/2-RAIO_BOLA,
                       LARGURA_CANVAS/2+RAIO_BOLA, ALTURA_CANVAS/2+RAIO_BOLA, fill='black')

    #Texto que instrui o jogador a iniciar o jogo:
    TEXTO1= canvas.create_text(LARGURA_CANVAS/2 , ALTURA_CANVAS/2 +2*RAIO_BOLA+ 20,
                                       font=('Times New Roman', 36),
                                       text = 'Clique para começar',)

    #mostra ao jogador a quantidade restante de tijolos:
    TEXTO2 = canvas.create_text( SEPARACAO_ENTRE_TIJOLOS,
                             ALTURA_CANVAS-SEPARACAO_ENTRE_TIJOLOS,
                             text = 'TIJOLOS: %3d ' % (TIJOLOS),
                             anchor=SW, font=('Times New Roman', 14),fill='maroon')

    #mostra ao jogador a quantidade restante de tentativas:
    TEXTO3= canvas.create_text( LARGURA_CANVAS-SEPARACAO_ENTRE_TIJOLOS, ALTURA_CANVAS- SEPARACAO_ENTRE_TIJOLOS,
                                text=  'TENTATIVAS: ' + str(TENTATIVAS), anchor=SE, font=('Times New Roman', 14),fill='blue')
    

    
    


def IniciouRodada():
    global BOLA, TENTATIVAS,vy,vx,TIJOLOS
    while TIJOLOS!=0:
        moveBOLA()
        verificaObjColidido()
        if getY(BOLA)>=ALTURA_CANVAS:
            TENTATIVAS-=1
            canvas.itemconfig(TEXTO3, text = 'TENTATIVAS: ' + str(TENTATIVAS))
            tocaSom(BOLAfora)
            if TENTATIVAS!=0:
                canvas.delete(BOLA)
                BOLA= canvas.create_oval(LARGURA_CANVAS/2 - RAIO_BOLA,ALTURA_CANVAS/2-RAIO_BOLA,
                           LARGURA_CANVAS/2+RAIO_BOLA, ALTURA_CANVAS/2+RAIO_BOLA, fill='black')
                vy=3
                vx=random.uniform(1.0, 3.0)
                if random.choice([True, False])==True:
                    vx = -vx
                break 
            else:
                gameOver()
                break
    if TIJOLOS==0:
        gameWon()
        

def moveBOLA():
    global vx,vy
    canvas.move(BOLA, vx,vy)
    canvas.update() 
    time.sleep(DELAY)
    if getY(BOLA)<=2*RAIO_BOLA:
        vy=-vy
    elif getX(BOLA) <= 2*RAIO_BOLA or getX(BOLA)>=LARGURA_CANVAS:
        vx=-vx
        
 
    


def getX(objeto):
    [x0, y0, x1, y1] = canvas.coords(objeto)
    return x1

def getY(objeto):
    [x0, y0, x1, y1] = canvas.coords(objeto)
    return y1
        
def moveuMouse(e):
    global x1
    canvas.move(RAQUETE, e.x-LARGURA_RAQUETE/2 - x1 ,0 ) #move a raquete na horizontal
    x1=e.x-LARGURA_RAQUETE/2    
    if getX(RAQUETE)>=LARGURA_CANVAS:
        canvas.move(RAQUETE,LARGURA_CANVAS - getX(RAQUETE),0)
        x1=LARGURA_CANVAS-LARGURA_RAQUETE #garante que a raquete não saia pela lateral direita do canvas    
    elif getX(RAQUETE) <=LARGURA_RAQUETE: #garante que a raquete não saia pela lateral esquerda do canvas  
        canvas.move(RAQUETE, LARGURA_RAQUETE - getX(RAQUETE),0)
        x1=0

def clicouMouse(e): 
    global TEXTO1
    canvas.delete(TEXTO1)
    if not gameOver() and not gameWon():
        IniciouRodada()
      
    
def verificaObjColidido():
    global vy, TIJOLOS
    objColidido = detectaColisoes()
    if objColidido != None:
        vy=-vy *ACELERACAO
        if objColidido != RAQUETE:
            canvas.delete(objColidido)
            tocaSom(tocouTIJOLO)
            TIJOLOS-=1
            canvas.itemconfig(TEXTO2, text = 'TIJOLOS: %3d ' % (TIJOLOS))
        else:
            dif = getY(BOLA)- (ALTURA_CANVAS- DISTANCIA_Y_RAQUETE - ALTURA_RAQUETE) 
            canvas.move(BOLA,0, -dif)               
            tocaSom(tocouRAQUETE)
    
        

def detectaColisoes():
    global lista
    [xb0, yb0, xb1, yb1] = canvas.coords(BOLA)
    lista = canvas.find_overlapping(xb0, yb0, xb1, yb1)
    if len(lista)>1:
        if lista[0] != BOLA  and lista[0] != TEXTO2 and lista[0] !=TEXTO3:
            return lista [0]
    else:
        return None

def gameWon():
    if TIJOLOS==0:
        canvas.delete(BOLA)    
        canvas.create_text(LARGURA_CANVAS/2, ALTURA_CANVAS/2,
                                           font=('Comic Sans', 36),
                                           text = 'Parabéns,',fill='pink')

        canvas.create_text(LARGURA_CANVAS/2, ALTURA_CANVAS/2+ 100,
                                           font=('Comic Sans', 36),
                                           text = 'Você é bom!!',fill='pink')

        canvas.create_text(LARGURA_CANVAS/2,ALTURA_CANVAS/2 +200,
                                           text = 'em breve níveis mais difíceis..',
                                           font=('Comic Sans', 14))
        tocaSom(ganhouJogo)
        return True

def gameOver():
    if TENTATIVAS==0:
        canvas.delete(BOLA)
        canvas.create_text(LARGURA_CANVAS/2, ALTURA_CANVAS/2,
                                       font=('Courrier', 36),
                                       text = 'GAME OVER')
        tocaSom(perdeuJogo)
        return True

def tocaSom(file):
    PlaySound(file, SND_FILENAME|SND_ASYNC)
    
canvas = Canvas(width=LARGURA_CANVAS, height=ALTURA_CANVAS,
background='white')
canvas.pack(fill=BOTH,expand=YES)

setup()

canvas.bind("<Motion>", moveuMouse)
canvas.bind("<ButtonPress>", clicouMouse)

mainloop()
