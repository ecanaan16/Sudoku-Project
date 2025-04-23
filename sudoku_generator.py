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
    screen.fill("lightblue")

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
                    return "easy"
                elif medium_button.collidepoint(event.pos):
                    print("difficulty medium")
                    return "medium"
                elif hard_button.collidepoint(event.pos):
                    print("difficulty hard")
                    return "hard"
            pygame.display.update()


#track 0
#test values that replaces the 0
def game_menu(screen):
    button_font = pygame.font.Font(None,70)
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

    return reset_button, restart_button, exit_button



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
        pygame.draw.rect(self.screen, border_color, (x, y, self.width, self.height), 3 if self.selected else 3)

class Board:
    def __init__(self, width, height, screen, difficulty):
#         #Constructor for the Board class.
#         #screen is a window from PyGame.
#         #difficulty is a variable to indicate if the user chose easy medium, or hard.
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty


        if self.difficulty == "easy":
            self.board_arr = generate_sudoku(9,30)


        elif self.difficulty == "medium":
            self.board_arr = generate_sudoku(9, 40)
        else:
            self.board_arr = generate_sudoku(9, 50)

        self.empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.board_arr[i][j] == 0:
                    self.empty_cells.append((i,j))

        self.cells = [[Cell(self.board_arr[i][j], i, j, self.screen) for j in range(9)] for i in range(9)]



    def draw(self):
#         #Draws an outline of the Sudoku grid, with bold lines to delineate the 3x3 boxes.
#         #Draws every cell on this board.

        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw()

        for i in range(1, 9):

            if i % 3 == 0:
                pygame.draw.line(
                    self.screen,
                    (0,0,0),
                    (0, i * 100),
                    (self.width, i * 100),
                    15
                )

            else:

                pygame.draw.line(
                    self.screen,
                    (0, 0, 0),
                    (0, i * 100),
                    (self.width, i * 100),
                    3
                )

        for i in range(1, 9):

            if i % 3 == 0:
                pygame.draw.line(
                    self.screen,
                    (0,0,0),
                    (i * 100, 0),
                    (i * 100, self.height),
                    15
                )
            else:
                pygame.draw.line(
                    self.screen,
                    (0,0,0),
                    (i * 100, 0),
                    (i * 100, self.height),
                    3
                )




    def select(self, row, col):
# #         #Marks the cell at (row, col) in the board as the current selected cell.
# # 	    #Once a cell has been selected, the user can edit its value or sketched value.
        self.selected_cell = self.cells[row][col]

        self.selected_cell.selected = True

        self.selected_cell.draw()

#click event will trigger click method passing the click coord as arguments

    def click(self, row, col):
#         #If a tuple of (x,y) coordinates is within the displayed board,
#         # this function returns a tuple of the (row, col) of the cell which was clicked.
#         # Otherwise, this function returns None.

        #should also include boarders
        if 0<=row<=900 and 0<=col<=900:

            coord = (row//100,col//100)

        #if function is not Null call select and pass coord as arguments
            return coord

    def clear(self):
#         #Clears the value cell.
#         # Note that the user can only remove the cell values and
#         # sketched values that are filled by themselves.


        self.selected_cell.set_cell_value(0)

    #changes the selected cell value
    #keeps value as 0 still unitl the number is placed
    #call draw again to update the cell with the sketch
    def sketch(self, value):
#         #Sets the sketched value of the current selected cell equal to the user entered value.
#         # It will be displayed at the top left corner of the cell using the draw() function.

        self.selected_cell.set_sketched_value(value)
        self.selected_cell.draw()


    def place_number(self, value):
#         #Sets the value of the current selected cell equal to the user entered value.
#         # Called when the user presses the Enter key.
        self.selected_cell.set_cell_value(value)


    def reset_to_original(self):
#         #Resets all cells in the board to their original values
#         # (0 if cleared, otherwise the corresponding digit).

        #should revert to og board
        for each_coord in self.empty_cells:
            print(each_coord)
            self.board_arr[each_coord[0]][each_coord[1]] = 0
            self.cells[each_coord[0]][each_coord[1]].value = 0



    def is_full(self):
#         #Returns a Boolean value indicating whether the board is full or not.

        if self.find_empty() is None:
            return True
        return False

    def update_board(self):
#         #Updates the underlying 2D board with the values in all cells.

        for i in range(9):
            for j in range(9):
                self.board_arr[i][j] = self.cells[i][j].value

    def find_empty(self):
#         #Finds an empty cell and returns its row and col as a tuple (x,y)

        for i in range(9):
            for j in range(9):
                if self.board_arr[i][j] == 0:
                    coord = (i,j)
                    return coord

    def check_board(self):
#         #Check whether the Sudoku board is solved correctly.
        #compare board with solution board

        while len(self.empty_cells) > 0:
            coord = self.empty_cells[0]
            for col in range(9):
                if col == coord[1]:
                    continue

                if self.board_arr[coord[0]][col] == self.board_arr[coord[0]][coord[1]]:
                    #print("false 1")
                    return False

            for row in range(9):

                if row == coord[0]:
                    continue

                if self.board_arr[row][coord[1]] == self.board_arr[coord[0]][coord[1]]:
                    #print("false 2")
                    return False

            box = ((coord[0]//3) *3, (coord[1]//3)*3)

            # for i in range(3):
            #     for j in range(3):
            #
            #         if box[0] * 3 + i == coord[0] and box[1]*3+j == coord[1]:
            #             continue
            #
            #         if self.board_arr[box[0] * 3 + i][box[1]*3+j] == self.board_arr[coord[0]][coord[1]]:
            #             return False
            for row in range(box[0], box[0] + 3):
                for col in range(box[1], box[1] + 2):
                    if row == coord[0] and col == coord[1]:
                        continue
                    if self.board_arr[row][col] == self.board_arr[coord[0]][coord[1]]:
                        #print(f"row: {row}, col: {col}, value: {self.board_arr[row][col]}")
                        #print("false 3")
                        return False



            self.empty_cells = self.empty_cells[1:]

            return True




# #
#
#
#
class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = int(math.sqrt(row_length))
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.solution_board = [[0 for _ in range(row_length)] for _ in range(row_length)]


    '''
        Returns a 2D python list of numbers which represents the board

        Parameters: None
        Return: list[list]
        '''

    def get_board(self):
        return self.board

    '''
    Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

    Parameters: None
    Return: None
    '''

    def print_board(self):
        for i in range(self.row_length):
            for j in range(self.row_length):
                if j == self.row_length - 1:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")

    '''
    Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

    Parameters:
    row is the index of the row we are checking
    num is the value we are looking for in the row

    Return: boolean
    '''

    def valid_in_row(self, row, num):
        for col in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    '''
    Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

    Parameters:
    col is the index of the column we are checking
    num is the value we are looking for in the column

    Return: boolean
    '''

    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    '''
    Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

    Parameters:
    row_start and col_start are the starting indices of the box to check
    i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
    num is the value we are looking for in the box

    Return: boolean
    '''

    def valid_in_box(self, start_row, start_col, num):
        for row in range(start_row, start_row + self.box_length):
            for col in range(start_col, start_col + self.box_length):
                if self.board[row][col] == num:
                    return False
        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

    Parameters:
    row and col are the row index and col index of the cell to check in the board
    num is the value to test if it is safe to enter in this cell

    Return: boolean
    '''

    def is_valid(self, row, col, num):
        if not self.valid_in_row(row, num):
            return False
        if not self.valid_in_col(col, num):
            return False
        box_row = (row // self.box_length) * self.box_length
        box_col = (col // self.box_length) * self.box_length
        if not self.valid_in_box(box_row, box_col, num):
            return False
        return True

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

    Parameters:
    row_start and col_start are the starting indices of the box to check
    i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

    Return: None
    '''

    def fill_box(self, row_start, col_start):
        numbers = list(range(1, self.row_length + 1))
        for i in range(self.box_length):
            for j in range(self.box_length):
                index = random.randrange(len(numbers))
                self.board[row_start + i][col_start + j] = numbers.pop(index)

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

    Parameters: None
    Return: None
    '''

    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

    Parameters:
    row, col specify the coordinates of the first empty (0) cell

    Return:
    boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

    Parameters: None
    Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called

    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

    Parameters: None
    Return: None
    '''

    def remove_cells(self):
        removed_coords = []
        while len(removed_coords) <= self.removed_cells:

            random_row = random.randint(0,8)
            random_col = random.randint(0,8)
            random_coord = (random_row, random_col)

            if random_coord not in removed_coords:
                removed_coords.append(random_coord)
                self.board[random_row][random_col] = 0

    '''
    DO NOT CHANGE
    Provided for students
    Given a number of rows and number of cells to remove, this function:
    1. creates a SudokuGenerator
    2. fills its values and saves this as the solved state
    3. removes the appropriate number of cells
    4. returns the representative 2D Python Lists of the board and solution

    Parameters:
    size is the number of rows/columns of the board (9 for this project)
    removed is the number of cells to clear (set to 0)

    Return: list[list] (a 2D Python list to represent the board)
    '''


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    for each_row in sudoku.get_board():
        print(each_row)
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


"TESTS________________________________"

if __name__ == "__main__":
    # test_generator = SudokuGenerator(9, 30)
    # test_generator.fill_values()

    print("Trying to call get_board()...")
    try:
        #user_board = test_generator.print_board()
        print("Success! get_board() returned:")
    except Exception as e:
        print("Error:", e)
    # sets up main menu
    width = 900
    height = 900
    game_over = False
    pygame.init()
    screen = pygame.display.set_mode((900, 1000))
    pygame.display.set_caption("Sudoku")

    # Event loop
    running = True

    while running:
        difficulty = draw_game_start(screen)
        user_board = Board(900, 900, screen, difficulty)
        in_game = True
        selected_cell = user_board.cells[0][0]
        selected = False
        sketched = False
        screen.fill("lightblue")
        user_board.draw()
        while in_game:

            reset_button, restart_button, exit_button = game_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board_pos = (0,0)

                    if reset_button.collidepoint(event.pos):
                        print("reset")
                    elif restart_button.collidepoint(event.pos):
                        print("restart")
                        in_game = False
                    elif exit_button.collidepoint(event.pos):
                        sys.exit()


                    else:
                        x, y = event.pos
                        board_pos = user_board.click(x, y)

                        if user_board.board_arr[board_pos[1]][board_pos[0]] == 0:
                            user_board.draw()
                            selected_cell.selected = False
                            selected_cell.draw()

                            user_board.select(board_pos[1], board_pos[0])
                            selected_cell = user_board.cells[board_pos[1]][board_pos[0]]
                            selected = True

                if event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:
                    if selected:
                        user_board.clear()
                        user_board.sketch(event.unicode)
                        sketched = True



                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if sketched:
                        user_board.place_number(int(user_board.selected_cell.sketched_value))
                        user_board.selected_cell.draw()
                        user_board.update_board()
                        user_board.selected_cell.sketched_value = ""


                        if user_board.is_full():
                            if user_board.check_board():
                                print("WE DID ITTTTTTT")

                            else:
                                print("FAILED")


            pygame.display.update()
