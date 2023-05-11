import tkinter as tk
import random
import time
from tkinter import ttk
from tkinter.messagebox import showinfo
import os

class Game:
	def __init__(self):
		#Init
		
		#Integers/floats
		self.score = 0 # Score
		self.speed = 4 # Speed
		self.timer = 100 # Spawns pipes
		self.jumpSpeed = 0 # The Vertical Speed
		self.mass = 1 # Default = 1, gravity multiplier
		self.trueScore = self.score # Increments in 0.5
		self.gameRoot = tk.Tk() # Game window
		self.gameRoot.geometry('450x450') # Initialising Window
		
		#Canvas
		
		self.gameCanvas = tk.Canvas(self.gameRoot, width=450,height=450,bg='blue')
		self.gameCanvas.pack()
		
		#Tkinter Elements
		self.shape = [self.gameCanvas.create_rectangle(10,10,60,60,fill='yellow')]
		self.scoreText = self.gameCanvas.create_text(450/2,15,text=str(self.score),fill="white",font=('Helvetica 30 bold'))
		self.gameRoot.bind('<space>', self.Jump)
		self.pipes = []

		self.running = True # Always starts as True
	def gravity(self):
		self.jumpSpeed -= 0.1 * self.mass *-1.5 # doesn't return
	def Jump(self,event):
		self.jumpSpeed = -4 # Jump event
		#print('jump speed = '+str(self.jumpSpeed)) #Debuging
	def UpdateSelf(self):
		if self.running == False:
			return 1
		self.gravity() # Does Gravity
		
		for i in self.shape: # Moves the shape
			self.gameCanvas.move(i,0,self.jumpSpeed)
		
		for i in self.pipes: # Moves the pipes
			self.gameCanvas.move(i,-self.speed,0)
		if self.timer == 100: #Spawns new pipe
			self.timer = 0 # resets the timer
			self.newPipe() # Adds a new pipe
		self.timer += 1 # Increments the timer by one
		self.collisions() # Does collisions
	def newPipe(self): # Adds a new pipe
		self.rand = random.randint(0,200) # Random offset
		self.pipes.append(self.gameCanvas.create_rectangle(450,450,495,400-self.rand,fill='green')) # Adds the bottom pipe
		self.pipes.append(self.gameCanvas.create_rectangle(450,0,495,400-self.rand-150,fill='green')) # Adds the top pipe
	def collisions(self): # Finds collisions
		pos = self.gameCanvas.coords(self.shape) # Returns x1, y1, x2, y2
		collision = self.gameCanvas.find_overlapping(pos[0],pos[1],pos[2],pos[3]) # returns a tuple of id's overlapping
		
		for i in self.pipes: # Goes through the pipes
			if i in collision: # Checks if the pipe ID is in the collision tuple
				self.end() # Ends the game
			if pos[2] > self.gameCanvas.coords(i)[0] and pos[2] < self.gameCanvas.coords(i)[0] + 4: # Adds score
				self.trueScore += 1/2 # Adds 0.5 to trueScore
				if self.trueScore % 1 == 0: # Checks if trueScore is divisible by one
					self.score = self.trueScore # Sets score to trueScore
					self.scoreUpdate() # Updates the score
				#print(self.score) # Debug
		
		if pos[3] >= 450: # Checks if it is on the floor
			self.end() # Ends the game
		
		if pos[3] <= 0: # Checks if it is too high
			self.end() # Ends the game
		#print(pos) # Debug
	def scoreUpdate(self): # Updates the score
		self.gameCanvas.itemconfig(self.scoreText,text=str(int(self.score))) # Changes the scoreText's text to score
	def end(self):
		
		self.destroy()
	def destroy(self):
		self.speed = 0 # Stops movement
		showinfo(message='Hello, thanks for trying my game, hope you enjoyed.',title='You died') # Shows this message
		self.gameRoot.destroy() # Destroys the window
game = Game()
while 1:
  if game.UpdateSelf():
    break
  canvas.update()
  time.sleep(0.01)
