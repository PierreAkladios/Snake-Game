#Author: Pierre Akladios

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    rows = 0
    w = 0
    #constructor
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
    
    def move(self, dirnx, dirny):
        """moving the cubes"""
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos(self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        pass

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
                pygagme.quit()
                
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
        pass

    def addCube(self):
        pass

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
    global rows, width, s
    surface.fill((255,255,255)) #coloring the background
    s.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, items):
    pass

def message_box(subject, content):
    pass

def main():
    global width, rows,s
    width = 400
    rows = 16
    win = pygame.display.set_mode((width, width))
    s = Snake((251, 255, 0), (8,8))
    flag = True

    clock = pygame.time.Clock() #clock to control the speed of the frames

    while flag:
        pygame.time.delay(40) #delay
        clock.tick(8) #blocks/second
        redrawWindow(win)
    pass

main()



