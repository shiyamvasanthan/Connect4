import pygame

#Initialize pygame
pygame.init()

#Setup the window
window = pygame.display.set_mode((700, 700))
window.fill((255, 255, 255))
pygame.display.set_caption('Connect 4')

#Connect 4 Grid: 6 rows, 7 columns
grid = [
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0],
]

#Game Colors
black = (0, 0, 0)
blue = (51, 102, 255)
white = (255, 255, 255)
red = (220, 0, 0)
yellow = (253, 222, 42)

#Set to true if it's the red player's turn, set to false if it's the yellow player's turn
red_player = True

#Set to true if the mouse is clicked, set to false otherwise
mouse_clicked = False

#Represents column numbers 0 to 6 in the grid array, set at -1 so when the game initially runs it doesn't draw anything on the screen
column = -1

#Represents row numbers 0 to 5 in the grid array
row = 5

#The value stored by each position on the grid, starts at 0 to show that there is no game piece, 1 represents red, 2 represents yellow
#1 represents a red piece, 2 represents a yellow piece
placeholder = 0

#If the game is over set this variable to true
end_game = False

#The winner is stored in this string, and will be displayed at the end
winner = ""

#Game font is arial bold size 160
arial = pygame.font.SysFont('Arial Bold', 160)

#Draw the game board function
def draw_board():
	#Draws the blue rectangle
	pygame.draw.rect(window, blue, (0, 100, 700, 600))

	#Draws the white circles 
	for y in range(6):
		for x in range(7):
			pygame.draw.circle(window, white, (x*100 + 50, y*100 + 150), 30)

#End screen function: Clear the screen with white, depending on winner, display that they won and update the screen
def end_screen():
    pygame.draw.rect(window, white, (0, 0, 700, 700))
    win = arial.render(winner + " Wins!", False, black)
    if winner == "Red":
        window.blit(win, (75, 250))
    else:
        window.blit(win, (5, 250))
    pygame.display.update()

#Draw the game board by calling the function. It's not in the main game loop else it will clear all the game pieces
draw_board()

#Main Game While Loop, run while the end_game variable is false
while not end_game:
	#Get the x and y position of the mouse
	(mx, my) = pygame.mouse.get_pos()

	#Check horizontal win conditions: Leftmost piece can be up to column 3 so range(4), every row so range(6)
	for c in range(4):
		for r in range(6):
			if (grid[r][c] == 1 and grid[r][c+1] == 1 and grid[r][c+2] == 1 and grid[r][c+3] == 1):
				winner = "Red"
				end_game = True
			elif (grid[r][c] == 2 and grid[r][c+1] == 2 and grid[r][c+2] == 2 and grid[r][c+3] == 2):
				winner = "Yellow"
				end_game = True	

	#Check vertical win conditions: Every column so range(7), topmost piece can be up to row 2 so range(3)
	for c in range(7):
		for r in range(3):
			if (grid[r][c] == 1 and grid[r+1][c] == 1 and grid[r+2][c] == 1 and grid[r+3][c] == 1):
				winner = "Red"
				end_game = True
			elif (grid[r][c] == 2 and grid[r+1][c] == 2 and grid[r+2][c] == 2 and grid[r+3][c] == 2):
				winner = "Yellow"
				end_game = True	
	
	#Check positive slope diagonal win conditions: Leftmost piece can be up to column 3 so range(4), bottommost piece can be from row 3 to 5 inclusive so range(3, 6) 
	for c in range(4):
		for r in range(3, 6):
			if (grid[r][c] == 1 and grid[r-1][c+1] == 1 and grid[r-2][c+2] == 1 and grid[r-3][c+3] == 1):
				winner = "Red"
				end_game = True
			elif (grid[r][c] == 2 and grid[r-1][c+1] == 2 and grid[r-2][c+2] == 2 and grid[r-3][c+3] == 2):
				winner = "Yellow"
				end_game = True	

	#Check negative slope diagonal win conditions: Rightmost piece can be from row 3 to 6 inclusive so range(3, 7), bottommost piece can be from row 3 to 5 inclusive so range(3, 6)
	for c in range(3, 7):
		for r in range(3, 6):
			if (grid[r][c] == 1 and grid[r-1][c-1] == 1 and grid[r-2][c-2] == 1 and grid[r-3][c-3] == 1):
				winner = "Red"
				end_game = True
			elif (grid[r][c] == 2 and grid[r-1][c-1] == 2 and grid[r-2][c-2] == 2 and grid[r-3][c-3] == 2):
				winner = "Yellow"
				end_game = True	
	
	#If the mouse is clicked
	if mouse_clicked == True:
		#Get the column number by floor dividing the x value of the mouse by 100
		column = mx//100

		#Check from row 5 all the way to row 0 if the column is empty, if it is, set the row variable to the highest row that's free
		for r in range(5, -1, -1):
			if grid[r][column] == 0:
				row = r
				break

		#If the board is empty on the specific row and column the user chooses to place the game piece
		if grid[row][column] == 0:	
			#If it's the red player's turn draw the red piece at the correct row and column, set the placeholder value to 1
			if red_player == True:
				pygame.draw.circle(window, red, (column*100 + 50, row*100 + 150), 30)
				placeholder = 1
				#Clear the space above the board and now draw the yellow player as it's now their turn
				red_player = False
				pygame.draw.rect(window, white, (0, 0, 700, 100))
				pygame.draw.circle(window, yellow, (mx, 50), 30)
			#If it's the yellow player's turn draw the yellow piece at the correct row and column, set the placeholder value to 2
			else:
				pygame.draw.circle(window, yellow, (column*100 + 50, row*100 + 150), 30)
				placeholder = 2
				#Clear the space above the board and now draw the red player as it's now their turn
				red_player = True
				pygame.draw.rect(window, white, (0, 0, 700, 100))
				pygame.draw.circle(window, red, (mx, 50), 30)

			#Set's the placeholder value to the grid value
			grid[row][column] = placeholder

		#Set the mouse clicked variable to false so it only registers one click at a time
		mouse_clicked = False

	#Update the screen
	pygame.display.update()

	#Throughout the entire program
	for event in pygame.event.get():
		#Check to see if the user exits the pygame window
		if event.type == pygame.QUIT:
			pygame.quit()
		#Check to see if the user clicks the mouse, if they do set mouse clicked variable to true
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_clicked = True
		#Check to see if the user moves the mouse from left to right, if they do, draw the red or yellow character above the board
		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(window, white, (0, 0, 700, 100))
			posx = event.pos[0]
			if red_player == True:
				pygame.draw.circle(window, red, (posx, 50), 30)
			else:
				pygame.draw.circle(window, yellow, (posx, 50), 30)

#Display the game for second, display the end screen for a second, then exit the pygame window
pygame.time.delay(1000)
end_screen()
pygame.time.delay(1000)
pygame.quit()