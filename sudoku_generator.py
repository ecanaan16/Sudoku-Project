import math,random,sys
import pygame
"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

def draw_game_start(screen):
    #fonts/texts for title, buttons, and subtitle
    start_title_font = pygame.font.Font(None,100)
    button_font = pygame.font.Font(None,70)
    subtitle_font = pygame.font.Font(None,80)

    #creating board object
    #board.select(5,6)
    screen.fill("lightblue")
    #
    # #testing draw method

    #title
    title_surf = start_title_font.render("Welcome to Sudoku", 0,"black")
    title_rect = title_surf.get_rect(
        center =(width//2,height//2-300)
    )
    screen.blit(title_surf, title_rect)

    #subtitle
    subtitle_surf = subtitle_font.render("Select Game Mode: ", 0, "black")
    subtitle_rect = subtitle_surf.get_rect(center = (width//2, height//2-200))
    screen.blit(subtitle_surf, subtitle_rect)

    #button text
    easy_text = button_font.render("EASY", 0, "white")
    medium_text = button_font.render("MEDIUM", 0, "white")
    hard_text = button_font.render("HARD", 0, "white")

    easy_surf = pygame.Surface((easy_text.get_size()[0] + 50, easy_text.get_size()[1] + 20))
    easy_surf.fill("black")
    easy_surf.blit(easy_text,(25,10))
    medium_surf = pygame.Surface((medium_text.get_size()[0] + 50, medium_text.get_size()[1] + 20))
    medium_surf.fill("black")
    medium_surf.blit(medium_text,(25,10))
    hard_surf = pygame.Surface((hard_text.get_size()[0] + 50, hard_text.get_size()[1] + 20))
    hard_surf.fill("black")
    hard_surf.blit(hard_text,(25,10))

    easy_button = easy_surf.get_rect(
        center = (width//2-250,height//2-100)

    )

    medium_button = medium_surf.get_rect(
        center = (width//2,height//2-100)

    )
    hard_button = hard_surf.get_rect(
        center = (width//2+250, height//2-100)
    )
    screen.blit(easy_surf, easy_button)
    screen.blit(medium_surf, medium_button)
    screen.blit(hard_surf, hard_button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    print("difficulty easy")
                    game_menu(screen)
                elif medium_button.collidepoint(event.pos):
                    print("difficulty medium")
                    game_menu(screen)
                elif hard_button.collidepoint(event.pos):
                    print("difficulty hard")
                    game_menu(screen)
            pygame.display.update()
def game_menu(screen):

    button_font = pygame.font.Font(None,70)
    screen.fill("lightblue")
    pygame.draw.line(screen, "black", (0,900),(900,900))
    #game button text
    reset_text = button_font.render("reset", 0, "white")
    restart_text = button_font.render("restart", 0, "white")
    exit_text = button_font.render("exit", 0, "white")
    #game button box
    reset_surf = pygame.Surface((reset_text.get_size()[0] + 50, reset_text.get_size()[1] + 20))
    reset_surf.fill("black")
    reset_surf.blit(reset_text,(25,10))
    restart_surf = pygame.Surface((restart_text.get_size()[0] + 50, restart_text.get_size()[1] + 20))
    restart_surf.fill("black")
    restart_surf.blit(restart_text,(25,10))
    exit_surf = pygame.Surface((exit_text.get_size()[0] + 50, exit_text.get_size()[1] + 20))
    exit_surf.fill("black")
    exit_surf.blit(exit_text,(25,10))
    reset_button = reset_surf.get_rect(
        center = (width//2-250, 950)
    )
    restart_button = restart_surf.get_rect(
        center = (width//2, 950)
    )
    exit_button = exit_surf.get_rect(
        center = (width//2+250, 950)
    )
    screen.blit(reset_surf, reset_button)
    screen.blit(restart_surf, restart_button)
    screen.blit(exit_surf, exit_button)
    board = Board(900, 900, screen, "hard")
    board.draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):

                    print("reset")
                    return
                elif restart_button.collidepoint(event.pos):
                    print("restart")
                    draw_game_start(screen)
                    return
                elif exit_button.collidepoint(event.pos):
                    sys.exit()

            pygame.display.update()



class Cell:
    def __init__(self, value, row, col, screen, width=100, height=100):
        self.value = value  # Final value (0 if empty)
        self.sketched_value = 0  # Temporary value (pencil-in)
        self.row = row
        self.col = col
        self.screen = screen
        self.width = width
        self.height = height
        self.selected = False  # Is this the selected cell?

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = self.col * self.width
        y = self.row * self.height

        # Background
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.width, self.height))

        # Draw sketched value in gray (if no final value)
        if self.sketched_value != 0 and self.value == 0:
            sketch_font = pygame.font.SysFont("arial", 24)
            sketch_text = sketch_font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(sketch_text, (x + 5, y + 5))

        # Draw final value in black
        if self.value != 0:
            val_font = pygame.font.SysFont("arial", 48)
            val_text = val_font.render(str(self.value), True, (0, 0, 0))
            text_rect = val_text.get_rect(center=(x + self.width // 2, y + self.height // 2))
            self.screen.blit(val_text, text_rect)

        # Draw border
        border_color = (255, 0, 0) if self.selected else (0, 0, 0)
        pygame.draw.rect(self.screen, border_color, (x, y, self.width, self.height), 3 if self.selected else 1)

class Board:
    def __init__(self, width, height, screen, difficulty):
#         #Constructor for the Board class.
#         #screen is a window from PyGame.
#         #difficulty is a variable to indicate if the user chose easy medium, or hard.
        self.width = width
        self.height = height
        self.screen = screen

        #creating array for board
        self.board = self.initialize_board()
        self.difficulty = difficulty

    def initialize_board(self):
        return [["-" for i in range(9)] for j in range(9)]

    def draw(self):
#         #Draws an outline of the Sudoku grid, with bold lines to delineate the 3x3 boxes.
#         #Draws every cell on this board.
        for i in range(1, 9):

            if i % 3 == 0:
                pygame.draw.line(
                    screen,
                    (0,0,0),
                    (0, i * 100),
                    (self.width, i * 100),
                    15
                )

            else:

                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (0, i * 100),
                    (self.width, i * 100),
                    5
                )

        for i in range(1, 9):

            if i % 3 == 0:
                pygame.draw.line(
                    screen,
                    (0,0,0),
                    (i * 100, 0),
                    (i * 100, self.height),
                    15
                )
            else:
                pygame.draw.line(
                    screen,
                    (0,0,0),
                    (i * 100, 0),
                    (i * 100, self.height),
                    5
                )


    def select(self, row, col):
# #         #Marks the cell at (row, col) in the board as the current selected cell.
# # 	    #Once a cell has been selected, the user can edit its value or sketched value.
            self.selected = (row,col)






#     def click(self, row, col):
#         #If a tuple of (x,y) coordinates is within the displayed board,
#         # this function returns a tuple of the (row, col) of the cell which was clicked.
#         # Otherwise, this function returns None.
#     def clear(self):
#         #Clears the value cell.
#         # Note that the user can only remove the cell values and
#         # sketched values that are filled by themselves.
#     def sketch(self, value):
#         #Sets the sketched value of the current selected cell equal to the user entered value.
#         # It will be displayed at the top left corner of the cell using the draw() function.
#     def place_number(self, value):
#         #Sets the value of the current selected cell equal to the user entered value.
#         # Called when the user presses the Enter key.
#     def reset_to_original(self):
#         #Resets all cells in the board to their original values
#         # (0 if cleared, otherwise the corresponding digit).
#     def def is_full(self):
#         #Returns a Boolean value indicating whether the board is full or not.
#     def update_board(self):
#         #Updates the underlying 2D board with the values in all cells.
#     def find_empty(self):
#         #Finds an empty cell and returns its row and col as a tuple (x,y)
#
#     def check_board(self):
#         #Check whether the Sudoku board is solved correctly.
# #
#
#
#
# class SudokuGenerator:
#     '''
# 	create a sudoku board - initialize class variables and set up the 2D board
# 	This should initialize:
# 	self.row_length		- the length of each row
# 	self.removed_cells	- the total number of cells to be removed
# 	self.board			- a 2D list of ints to represent the board
# 	self.box_length		- the square root of row_length
#
# 	Parameters:
#     row_length is the number of rows/columns of the board (always 9 for this project)
#     removed_cells is an integer value - the number of cells to be removed
#
# 	Return:
# 	None
#     '''
#     def __init__(self, row_length, removed_cells):
#         pass
#         #initializes the screen (length and cells to remove once reset)
#         #removed_cells determined by difficulty
#     '''
# 	Returns a 2D python list of numbers which represents the board
#
# 	Parameters: None
# 	Return: list[list]
#     '''
#     def get_board(self):
#         pass
#
#     '''
# 	Displays the board to the console
#     This is not strictly required, but it may be useful for debugging purposes
#
# 	Parameters: None
# 	Return: None
#     '''
#     def print_board(self):
#         pass
#
#     '''
#      # loop through rows
#
# 	Determines if num is contained in the specified row (horizontal) of the board
#     If num is already in the specified row, return False. Otherwise, return True
# 	Parameters:
# 	row is the index of the row we are checking
# 	num is the value we are looking for in the row
#
# 	Return: boolean
#     '''
#     def valid_in_row(self, row, num):
#         pass
#     #num is the empty cells where the user is inputing a number
#     '''
#     # loop through columns
#
# 	Determines if num is contained in the specified column (vertical) of the board
#     If num is already in the specified col, return False. Otherwise, return True
#
# 	Parameters:
# 	col is the index of the column we are checking
# 	num is the value we are looking for in the column
#
# 	Return: boolean
#     '''
#     def valid_in_col(self, col, num):
#         pass
#
#     '''
# 	Determines if num is contained in the 3x3 box specified on the board
#     If num is in the specified box starting at (row_start, col_start), return False.
#     Otherwise, return True
#
# 	Parameters:
# 	row_start and col_start are the starting indices of the box to check
# 	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
# 	num is the value we are looking for in the box
#
# 	Return: boolean
#     '''
#     #loop through the boxes
#     def valid_in_box(self, row_start, col_start, num):
#         pass
#
#     '''
#     Determines if it is valid to enter num at (row, col) in the board
#     This is done by checking that num is unused in the appropriate, row, column, and box
#
# 	Parameters:
# 	row and col are the row index and col index of the cell to check in the board
# 	num is the value to test if it is safe to enter in this cell
#
# 	Return: boolean
#     '''
#     def is_valid(self, row, col, num):
#         pass
#
#     '''
#     Fills the specified 3x3 box with values
#     For each position, generates a random digit which has not yet been used in the box
#
# 	Parameters:
# 	row_start and col_start are the starting indices of the box to check
# 	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
#
# 	Return: None
#     '''
#     def fill_box(self, row_start, col_start):
#         pass
#
#     '''
#     Fills the three boxes along the main diagonal of the board
#     These are the boxes which start at (0,0), (3,3), and (6,6)
#
# 	Parameters: None
# 	Return: None
#     '''
#     def fill_diagonal(self):
#         pass
#
#     '''
#     DO NOT CHANGE
#     Provided for students
#     Fills the remaining cells of the board
#     Should be called after the diagonal boxes have been filled
#
# 	Parameters:
# 	row, col specify the coordinates of the first empty (0) cell
#
# 	Return:
# 	boolean (whether or not we could solve the board)
#     '''
#     def fill_remaining(self, row, col):
#         if (col >= self.row_length and row < self.row_length - 1):
#             row += 1
#             col = 0
#         if row >= self.row_length and col >= self.row_length:
#             return True
#         if row < self.box_length:
#             if col < self.box_length:
#                 col = self.box_length
#         elif row < self.row_length - self.box_length:
#             if col == int(row // self.box_length * self.box_length):
#                 col += self.box_length
#         else:
#             if col == self.row_length - self.box_length:
#                 row += 1
#                 col = 0
#                 if row >= self.row_length:
#                     return True
#
#         for num in range(1, self.row_length + 1):
#             if self.is_valid(row, col, num):
#                 self.board[row][col] = num
#                 if self.fill_remaining(row, col + 1):
#                     return True
#                 self.board[row][col] = 0
#         return False
#
#     '''
#     DO NOT CHANGE
#     Provided for students
#     Constructs a solution by calling fill_diagonal and fill_remaining
#
# 	Parameters: None
# 	Return: None
#     '''
#     def fill_values(self):
#         self.fill_diagonal()
#         self.fill_remaining(0, self.box_length)
#
#     '''
#     Removes the appropriate number of cells from the board
#     This is done by setting some values to 0
#     Should be called after the entire solution has been constructed
#     i.e. after fill_values has been called
#
#     NOTE: Be careful not to 'remove' the same cell multiple times
#     i.e. if a cell is already 0, it cannot be removed again
#
# 	Parameters: None
# 	Return: None
#     '''
#     def remove_cells(self):
#         pass
#
# '''
# DO NOT CHANGE
# Provided for students
# Given a number of rows and number of cells to remove, this function:
# 1. creates a SudokuGenerator
# 2. fills its values and saves this as the solved state
# 3. removes the appropriate number of cells
# 4. returns the representative 2D Python Lists of the board and solution
#
# Parameters:
# size is the number of rows/columns of the board (9 for this project)
# removed is the number of cells to clear (set to 0)
#
# Return: list[list] (a 2D Python list to represent the board)
# '''
# def generate_sudoku(size, removed):
#     sudoku = SudokuGenerator(size, removed)
#     sudoku.fill_values()
#     board = sudoku.get_board()
#     sudoku.remove_cells()
#     board = sudoku.get_board()
#     return board

if __name__ == "__main__":
    #sets up main menu
    width = 900
    height = 900
    game_over = False
    pygame.init()
    screen = pygame.display.set_mode((900,1000))
    pygame.display.set_caption("Sudoku")
    draw_game_start(screen)
    game_menu(screen)
    #Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()