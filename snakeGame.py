#Author: Pierre Akladios

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    rows = 16
    w = 400
    #constructor
    def __init__(self,start,dirnx=1,dirny=0,color=(251, 255, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
    
    def move(self, dirnx, dirny):
        """moving the cubes"""
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        distance = self.w//self.rows
        #drawing the rectangle that is smaller than the size of the square to be able to see the borders
        pygame.draw.rect(surface, self.color, (self.pos[0]*distance+1, self.pos[1]*distance+1, distance-2, distance-2))
        if eyes:
            centre = distance//2
            radius = 3
            circleMiddleLeft = (self.pos[0]*distance+centre-radius,self.pos[1]*distance+7)
            circleMiddleRight = (self.pos[0]*distance + distance - radius*2, self.pos[1]*distance+7)
            pygame.draw.circle(surface, (25, 85, 181), circleMiddleLeft, radius)
            pygame.draw.circle(surface, (25, 85, 181), circleMiddleRight, radius)

class Snake(object):
    body = []
    turns = {} #dict where keys = position of the head and values= which direction the snake turns
    #constructor
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos) #creating the head of the snake
        self.body.append(self.head) #making the head part of the body
        #keeping track of which direction the snake is moving
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get() :
            #quitting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                
            #gets from a dictionnary of all keys the keys if they were pressed
            keys = pygame.key.get_pressed()

            #changing direction according to the key that is clicked
            for key in keys:
                #coordinates in pygame
                #top left corner = (0,0)
                #negative values go left and positive to the right
                #negative values go up and positive values go down
                if keys[pygame.K_LEFT]:
                
                    self.dirnx = -1
                    self.dirny = 0
                    #[:] makes a copy of the position
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]#adding to the dictionary

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): #getting index and cube object from the body
            p = c.pos[:] # getting the position of each cube
            #checking if p is part of the keys in the turn list
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])#turn at the value of the key
                #checking if all of the body has already passed
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                #checking if the head have reached the limits of the board
                if c.dirnx == -1 and c.pos[0] <= 0:#left edge
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: #right edge
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: #bottom edge
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: #top edge
                    c.pos = (c.pos[0], c.rows-1)
                else: c.move(c.dirnx,c.dirny) #keep moving normaly
                      
    def reset(self, pos):
        '''
        (coordinates)-> None
        getting rid of the body of the snake to restart the game
        '''
        self.head = Cube(pos)
        body = []
        self.body.append(self.head)
        turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        '''
        add cube after the tail of the snake depending on which direction the snack is moving
        (None)->None
        '''
        tail = self.body[-1]
        dirnx = tail.dirnx
        dirny = tail.dirny
        #checking what direction the snake is moving in
        if dirnx == 1 and dirny == 0:#moving right
            self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
        elif dirnx == -1 and dirny == 0:#moving left
            self.body.append(Cube((tail.pos[0]+1,tail.pos[1])))
        elif dirnx == 0 and dirny == 1:#moving down
             self.body.append(Cube((tail.pos[0],tail.pos[1]-1)))
        elif dirnx == 0 and dirny == 1:#moving up
             self.body.append(Cube((tail.pos[0],tail.pos[1]+1)))

        #making the cube move in the same direction as the rest of the body
        self.body[-1].dirnx = dirnx
        self.body[-1].dirny = dirny
             

    def draw(self, surface):
        '''drawing the snake'''
        for i, c in enumerate(self.body): #enumerate = itirate over the index and the value
            if i ==0: # drawing the eyes on the head
                c.draw(surface,True)
            else: # drawing the body
                c.draw(surface)
                            
def drawGrid(w, rows, surface):
    sizeBetween = w//rows #size of each square
    x=0
    y=0
    for i in range(rows):
        x+=sizeBetween
        y+=sizeBetween
        #drawing lines to make the grid
        pygame.draw.line(surface, (0,0,0), (x,0), (x,w))#vertical
        pygame.draw.line(surface, (0,0,0), (0,y), (w,y))#horizontal
        
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((255,255,255)) #coloring the background
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, snake):
    '''
    generating random cubes on the board for the snake to eat
    (int,snake)->(tuple)
    '''
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        #making sure that the snack will not appear on the body can be done with a for loop
        #A lambda function can take any number of arguments, but can only have one expression. typically used as an anonymous function inside another function
        #filter returns filtered items according to certain conditions.
        if len(list(filter(lambda a: a.pos == (x,y), positions))) >0:
            continue #go through the loop again
        else:
            break
    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows,s, snack
    width = 400
    rows = 16
    win = pygame.display.set_mode((width, width))
    s = Snake((251, 255, 0), (8,8))
    snack = Cube(randomSnack(rows, s), color =(255,0,0))
    flag = True

    clock = pygame.time.Clock() #clock to control the speed of the frames

    while flag:
        pygame.time.delay(40) #delay
        clock.tick(8) #blocks/second
        s.move()
        #cehcking if the head of the snack has hit the snack
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(rows, s), color =(255,0,0))

        #checking if the head collided with the body
        for x in range(len(s.body)):
            #The map() function executes a specified function for each item in a iterable. The item is sent to the function as a parameter.
            #map(function, iterables) as many iterables as parameters in the function
            if s.body[x].pos in list(map(lambda a:a.pos, s.body[x+1:])):
                print("Score: " + str(len(s.body)))
                #message_box("Loser!", "Play again if you want")
                s.reset((8,8))
                break
                
        redrawWindow(win)

main()



