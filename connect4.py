import pygame

#Initialize pygame
pygame.init()

#Setup the window
window = pygame.display.set_mode((700, 700))
window.fill((255, 255, 255))
pygame.display.set_caption('Connect 4')

#Game Colors
black = (0, 0, 0)
blue = (51, 102, 255)
white = (255, 255, 255)
red = (220, 0, 0)
yellow = (253, 222, 42)

#Number of rows
row = 6

#Number of columns
column = 7

#Set to true if it's the red player's turn, set to false if it's the yellow player's turn
red_player = True

#Winning Font
arial = pygame.font.SysFont('Arial Bold', 160)

#Tie Font
arial2 = pygame.font.SysFont('Arial Bold', 150)

#Draw the game board function
def draw_board():
	#Draws the blue rectangle
	pygame.draw.rect(window, blue, (0, 100, 700, 600))

	#Draws the white circles 
	for y in range(row):
		for x in range(column):
			pygame.draw.circle(window, white, (x*100 + 50, y*100 + 150), 30)

#Create 6 by 7 grid filled with zeros, return grid
def create_grid():
	grid = []
	for r in range(row):
		grid.append([])
		for c in range(column):
			grid[r].append(0)
	return grid 

#Check to see if there's an empty space on the grid
def empty_space(grid, row, column):
	if grid[row][column] == 0:	
		return True

#Set the value of the grid space to 1 representing red, or 2 representing yellow
def set_value(grid, row, column, placeholder):
	grid[row][column] = placeholder

#End screen function: Clear the screen with white, depending on winner, display that they won and update the screen
def end_screen(winner):
    pygame.draw.rect(window, white, (0, 0, 700, 700))
    win = arial.render(winner + " Wins!", False, black)
    tie = arial2.render(winner + " Wins!", False, black)

    if winner == "Red":
        window.blit(win, (75, 250))
    elif winner == "Yellow":
        window.blit(win, (5, 250))
    elif winner == "No One":
    	window.blit(tie, (10, 250))

    pygame.display.update()
    pygame.time.delay(1000)

#Checks to see if someone wins the game, return true if they do
def winning_condition(grid, placeholder):
	#Check horizontal lines: Leftmost piece can be up to column 3 so range(4), every row so range(6)
	for c in range(4):
		for r in range(6):
			if (grid[r][c] == placeholder and grid[r][c+1] == placeholder and grid[r][c+2] == placeholder and grid[r][c+3] == placeholder):
				return True

	#Check vertical lines: Every column so range(7), topmost piece can be up to row 2 so range(3)
	for c in range(7):
		for r in range(3):
			if (grid[r][c] == placeholder and grid[r+1][c] == placeholder and grid[r+2][c] == placeholder and grid[r+3][c] == placeholder):
				return True
	
	#Check positive slope diagonals: Leftmost piece can be up to column 3 so range(4), bottommost piece can be from row 3 to 5 inclusive so range(3, 6) 
	for c in range(4):
		for r in range(3, 6):
			if (grid[r][c] == placeholder and grid[r-1][c+1] == placeholder and grid[r-2][c+2] == placeholder and grid[r-3][c+3] == placeholder):
				return True

	#Check negative slope diagonals: Rightmost piece can be from row 3 to 6 inclusive so range(3, 7), bottommost piece can be from row 3 to 5 inclusive so range(3, 6)
	for c in range(3, 7):
		for r in range(3, 6):
			if (grid[r][c] == placeholder and grid[r-1][c-1] == placeholder and grid[r-2][c-2] == placeholder and grid[r-3][c-3] == placeholder):
				return True

#Create instance of grid
grid = create_grid()

#Draw the game board by calling the function. It's not in the main game loop else it will clear all the game pieces
draw_board()

#Main Game While Loop, run while the end_game variable is false
while True:		
	#Update the screen
	pygame.display.update()

	#Check for tie by creating a list to count the number of full spaces
	tie = []
	for r in range(6):
		for c in range(7):
			if empty_space(grid, r, c):
				continue
			else:
				tie.append(0)

	#If red wins display red as the winner
	if winning_condition(grid, 1):
		pygame.time.delay(1000)
		end_screen("Red")
		break
	#If yellow wins display yellow as the winner
	elif winning_condition(grid, 2):
		pygame.time.delay(1000)
		end_screen("Yellow")
		break
	#If the number of full spaces is 42 and no one won, the game is a tie
	elif len(tie) == 42 and winning_condition(grid, 1) != True and winning_condition(grid, 2) != True:
		pygame.time.delay(1000)
		end_screen("No One")
		break

	for event in pygame.event.get():
		#Check to see if the user exits the pygame window
		if event.type == pygame.QUIT:
			pygame.quit()
		#Check to see if the user moves the mouse from left to right, if they do, draw the red or yellow character above the board
		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(window, white, (0, 0, 700, 100))
			posx = event.pos[0]
			if red_player == True:
				pygame.draw.circle(window, red, (posx, 50), 30)
			else:
				pygame.draw.circle(window, yellow, (posx, 50), 30)
		#Check to see if the user clicks the mouse, if they do set mouse clicked variable to true
		if event.type == pygame.MOUSEBUTTONDOWN:
			#Get the column number by floor dividing the x value of the mouse by 100
			posx = event.pos[0]
			column = posx//100

			#Determine the next available row
			for r in range(5, -1, -1):
				if grid[r][column] == 0:
					row = r
					break
			
			#If the grid space is empty
			if empty_space(grid, row, column):
				#If it's the red player's turn
				if red_player == True:
					#Draw the red player, set the value of the grid space to 1
					pygame.draw.circle(window, red, (column*100 + 50, row*100 + 150), 30)
					set_value(grid, row, column, 1)

					#Clear the space above the board, draw the yellow player to show turn change
					pygame.draw.rect(window, white, (0, 0, 700, 100))
					pygame.draw.circle(window, yellow, (posx, 50), 30)
				#If it's the yellow player's turn
				else:
					#Draw the yellow player, set the value of the grid space to 2
					pygame.draw.circle(window, yellow, (column*100 + 50, row*100 + 150), 30)
					set_value(grid, row, column, 2)

					#Clear the space above the board, draw the red player to show turn change
					pygame.draw.rect(window, white, (0, 0, 700, 100))
					pygame.draw.circle(window, red, (posx, 50), 30)

				#Switch turns
				if red_player == True:
					red_player = False
				else:
					red_player = True
