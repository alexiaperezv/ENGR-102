import numpy as np
import math
import pygame
import sys

# Global variables:

# rows: determines the number of rows in our game board
horizontal_count = 6
# columns determines the number of columns in our game board
vertical_count = 7
# players, these are both variables that represent each player
player_one = 1
player_two = 0

# Colors these are global variables that will be used as our colors, because pygame required RGB code to determine
# colors.
GREY = (169,169,169)
BLACK = (0,0,0)
MAROON = (128,0,0)
WHITE = (225,225,225)


# Function definitions


def create_board(): #this function creates an array for the game board using all zeros
    board = np.zeros((horizontal_count,vertical_count))
    return board


def place_piece(game_board,row,column,piece): # this function places a specific piece at a specific location in the
    # game board.
    game_board[row][column] = piece


def a_valid_location(game_board,column): # this function makes sure that the location where a piece is being dropped
    # is actually a valid location. This is also a function replacing all the try and except statements,
    # instead of using try and except a bunch of times we just used this function and an if statement
    # to see if a move was allowed.
    return game_board[horizontal_count-1][column] == 0


def get_nextrow(game_board,column): # gets next open row (so if someone drops a piece in a column and then the next user
    # drops their piece in the same column, it'll place the second user's piece on top of the first.
    try:
        for i in range(horizontal_count):
            if game_board[i][column] == 0:
                return i
    except:
        pass


def show_board(game_board): # This function will display the board.
    print(np.flip(game_board,0)) # We flip the array to ensure that the 1st index will be at the bottom
    # instead of the top, that way when we drop the pieces the first one will go all the way down.


def winning_move(game_board,piece): # Checks to see if a specific move made by one of the players is a
    # winning move or not.
    # we first check all horizontal locations: this block of code checks to see if there are 4
    # pieces belonging to one user in a row in every row in the game board.
    for i in range(vertical_count-3):
        for j in range(horizontal_count):
            if game_board[j][i] == piece and game_board[j][i+1] == piece \
                    and game_board[j][i+2] == piece and game_board[j][i+3] == piece:
                return True
    # we now check for the vertical locations: this does the same as the previous block of code except
    # it checks every column instead of every row in the game board.
    for i in range(vertical_count):
        for j in range(horizontal_count-3):
            if game_board[j][i] == piece and game_board[j+1][i] == piece \
                    and game_board[j+2][i] == piece and game_board[j+3][i] == piece:
                return True
    # now we check for positive slope diagonal: same thing as previous blocks but diagonally and going up.
    for i in range(vertical_count-3):
        for j in range(horizontal_count-3):
            if game_board[j][i] == piece and game_board[j+1][i+1] == piece \
                    and game_board[j+2][i+2] == piece and game_board[j+3][i+3] == piece:
                return True
    # last we check for negative slope diagonal: same thing again but diagonally and going down.
    for i in range(vertical_count-3):
        for j in range(3,horizontal_count):
            if game_board[j][i] == piece and game_board[j-1][i+1] == piece \
                    and game_board[j-2][i+2] == piece and game_board[j-3][i+3] == piece:
                return True


def make_board(game_board): # Makes a graphic board (background is grey,
    # leaves a row on top open to have a sliding piece and also displays the winner at the end of the game.)
    for i in range(vertical_count):
        for j in range(horizontal_count):
            pygame.draw.rect(screen,GREY,(i*sq_size,j*sq_size+sq_size,sq_size,sq_size)) #pygame function that draws a rectangle
            pygame.draw.circle(screen,BLACK,(int(i*sq_size+sq_size/2),int(j*sq_size+sq_size+sq_size/2)),RADIUS) #pygame function that draws a circle
            # inside of the previously drawn rectangle (our rectangle actually looks more like a square.)
            # both of the previous functions make the board with circle spots in every column where a piece can be dropped.
            # if a spot is open the circle will be black, once a piece is dropped we implement the next few lines of code:
    for i in range(vertical_count):
        for j in range(horizontal_count):
            try:
                if game_board[j][i] == 1:
                    # if player 1 drops a piece, depending on which column they click on, the piece will be dropped in the
                    # lowest available row and the black circle will be filled with player 1's color (Maroon)
                    pygame.draw.circle(screen, MAROON,
                                   (int(i * sq_size + sq_size / 2), height-int(j * sq_size + sq_size / 2)), RADIUS)
                elif game_board[j][i]== 2:
                    # if player 2 drops a piece, depending on which column they click on, the piece will be dropped in the
                    # lowest available row and the black circle will be filled with player 2's color (White)
                    pygame.draw.circle(screen,WHITE,(int(i*sq_size+sq_size/2),height-int(j*sq_size+sq_size/2)),RADIUS)
            except:
                pass
    pygame.display.update()


# Game code:
# This is where the actual game code happens, all the code before this was creating functions and setting up the board
# this part is where we actually code how to play the game.

game_board = create_board() # This line creates the board using previously defined function that creates board.
game_over = False # Controls when the game is over, we will change it to True if a player wins or if the user
# clicks exit screen
turn = 0 # Switches for every user's turn

show_board(game_board) # displays board using one of our previously defined function

pygame.init() # We downloaded a module that has built in functions which help us make the graphics for the game
# previous line initializes the game graphics module.

sq_size = 100
width = vertical_count*sq_size
height = (horizontal_count+1)*sq_size

size = (width,height)
RADIUS = int(sq_size/2-5)

screen = pygame.display.set_mode(size) # creates the screen where the board displays and the game is played (graphics)
make_board(game_board)
pygame.display.update()
font = pygame.font.SysFont('comicsans',75) # this is the font and size of the message that will be displayed once
# one of the players win.


while not game_over: # the code within this loop will run until the game is over.
    for event in pygame.event.get():

        if event.type == pygame.QUIT: # if user clicks the exit button, game screen closes.
            sys.exit()

        if event.type == pygame.MOUSEMOTION: # a circle is drawn wherever the mouse moves
            # (within black rectangle on top), once the user clicks over one column the circle disappears and
            # the lowest row black circle is filled with whicherver user's turn it is color.
            pygame.draw.rect(screen,BLACK,(0,0,width,sq_size))
            xpos = event.pos[0]
            try:
                if turn == 0:
                    pygame.draw.circle(screen,MAROON,(xpos,int(sq_size/2)),RADIUS)
                else:
                    pygame.draw.circle(screen, WHITE, (xpos, int(sq_size / 2)), RADIUS)
            except:
                pass
        pygame.display.update() # updates game screen to display all of the prev actions.

        if event.type == pygame.MOUSEBUTTONDOWN: # runs when user clicks somewhere
            pygame.draw.rect(screen, BLACK, (0, 0, width, sq_size)) # this is what actually deletes the circle from the
            # top dow to drop it in one of the columns
            # First we ask for player one where they want to drop their piece
            if turn == 0: # if its player 1's turn
                xpos = event.pos[0]
                column = int(math.floor(xpos/sq_size))

                if a_valid_location(game_board, column): #if its a valid location it draws a circle of the player's color
                    row = get_nextrow(game_board, column)
                    place_piece(game_board, row, column, 1)

                    if winning_move(game_board, 1): # if the move is a winning move, it displays a message in the
                        # black rectangle on top.
                        label = font.render('Player 1 wins!!!',1,MAROON)
                        screen.blit(label,(50,10))
                        game_over = True # ends game and exits
            # Now we ask player two where they want to drop their piece this is the same code as player 1 but changing
            # the values so it corresponds to player 2
            else:
                xpos = event.pos[0]
                column = int(math.floor(xpos/sq_size))

                if a_valid_location(game_board, column): #if its a valid location it draws a circle of the player's color
                    row = get_nextrow(game_board, column)
                    place_piece(game_board, row, column, 2)

                    if winning_move(game_board, 2): # if the move is a winning move, display message.
                        label = font.render('Player 2 wins!!!', 1, WHITE)
                        screen.blit(label, (50, 10))
                        game_over = True # end game and exit

            # displays board:
            show_board(game_board)
            make_board(game_board)
            # Alternates turns between 0 and 1
            turn += 1
            turn = turn % 2

            # closes game within 5 seconds once game_over becomes true (graphic part):
            if game_over:
                pygame.time.wait(5000)