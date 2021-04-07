"""
Documented bugs: When making the choice of a column and the move is on the top line, if the piece is of the same color as
                 the bottom piece of the column to the left, the bottom piece "disappears".
                 Steps to take:
                1. check if the behavior is the same for both user and computer moves - so far only computer moves are
                    confirmed to have this behavior ========= error occurs only at comp_move()
                2. check what is the moves_dict{} structure before and after this behavior by writing the contents to a
                    file after every move
                    consecutive moves:
                    17: (250, 650, <Surface(70x70x32 SW)>), 18: 0,
                    17: (250, 650, <Surface(70x70x32 SW)>), 18: (350, 150, <Surface(70x70x32 SW)>),
                    17: 0, 18: (350, 150, <Surface(70x70x32 SW)>), <<<=== 17 should not switch back to 0

                === After making a successful counter-move with the comp_move() function, another pair of moves is made 
                === first red, then yellow. This is possibly related to no return statement on comp_move() -> should
                === be fixed
                 
                 
                === After a winner is found and the game is reset by pressing "space" the pieces disappear but the lists
                === appear to be populated. Try a solution based on moves_dict to replace the lists col1 .. col7
                === Solved by redefinition of reset_game() function
"""

from random import choice
import pygame

f = open("log.txt", "a")

pygame.init()
clock = pygame.time.Clock()
# window:
size = (700, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")
running = True


# Define some colors
BACKGROUND = (172, 204, 227)
WHITE = (200, 200, 200)
# YELLOW = (255, 242, 0)
# RED = (189, 15, 15)
ARROWBLUE = (65, 65, 107)

# Define images
red = pygame.image.load("C:\\Users\\alex_\\MyPythonScripts\\Connect4\\red70px.png")
yellow = pygame.image.load("C:\\Users\\alex_\\MyPythonScripts\\Connect4\\yellow70px.png")
blue = pygame.image.load("C:\\Users\\alex_\\MyPythonScripts\\Connect4\\bluebar.png")

# Define global scope variables
moves_dict = {} # will keep track of what moves were made
for i in range(42):
    moves_dict[i] = 0

col1, col2, col3, col4, col5, col6, col7 = [], [], [], [], [], [], [] # will keep track of how the columns are filled
move_count = 0
computer_moves = [(col1, 1), (col2, 2), (col3, 3), (col4, 4), (col5, 5), (col6, 6), (col7, 7)]


# Define the functions used
def reset_game():
    for i in range(42):
        moves_dict[i] = 0
    global move_count
    global running
    global col1, col2, col3, col4, col5, col6, col7
    move_count = 0
    col1 *= 0
    col2 *= 0
    col3 *= 0
    col4 *= 0
    col5 *= 0
    col6 *= 0
    col7 *= 0
    running = True


def set_piece(x, col):
    """
    :param x: will be called as one of the lists col1 .. col7
    :param col: will be an int value 1 to 7
    :return: will return tuple of coords and color for move or nothing if list is full (len(x) >= 6)
    will set color based on turn
    """
    global move_count
    if len(x) < 6:
        move_count += 1
        x.append(1)
        x_coord = col * 100 - 50
        y_coord = 750 - len(x) * 100
        color = red if move_count % 2 else yellow
        # populate the moves_dict with key: value pairs such that key in range(0, 42) and values are tuples(x_coord,
        # y_coord, color)
        moves_dict[6*(col-1)+6-len(x)] = (x_coord, y_coord, color)
        # for i in moves_dict:
        #     print(i, moves_dict[i][0], moves_dict[i][1], moves_dict[i][2])


def is_winner():
    """
    :return: True if win condition is found, else False
    except covers IndexError and KeyError
    """
    # vertical win cases:
    for i in [0, 1, 2, 6, 7, 8, 12, 13, 14, 18, 19, 20,
              24, 25, 26, 30, 31, 32, 36, 37, 38]:
        try:
            if moves_dict[i][2] == moves_dict[i+1][2] == moves_dict[i+2][2] == moves_dict[i+3][2]:
                return True
        except IndexError:
            continue
        except TypeError:
            continue
    # horizontal win cases:
    for i in range(24):
        try:
            if moves_dict[i][2] == moves_dict[i+6][2] == moves_dict[i+12][2] == moves_dict[i+18][2]:
                return True
        except IndexError:
            continue
        except TypeError:
            continue
    # first diagonal win cases:
    for i in [0, 1, 2, 6, 7, 8, 12, 13, 14, 18, 19, 20]:
        try:
            if moves_dict[i][2] == moves_dict[i+7][2] == moves_dict[i+14][2] == moves_dict[i+21][2]:
                return True
        except IndexError:
            continue
        except TypeError:
            continue
    # second diagonal win cases:
    for i in [18, 19, 20, 24, 25, 26, 30, 31, 32, 36, 37, 38]:
        try:
            if moves_dict[i][2] == moves_dict[i-5][2] == moves_dict[i-10][2] == moves_dict[i-15][2]:
                return True
        except IndexError:
            continue
        except TypeError:
            continue
    return False


def is_draw():
    if len(col1) == len(col2) == len(col3) == len(col4) == len(col5) == len(col6) == len(col7) == 6:
        return True
    return False


def player_score():
    """
    Should display on top of the window text related to Player 1 and Player 2,
    which turn it is, and the current score (games won)
    """


def comp_move():
    """
    Should look at the moves_dict and find a chance of winning in 1 move,
    Else check if opponent is 1 move away from win and block
    Else compute the most favorable move for a chance of winning
    :return: - None
    Should call set_piece() with the move decided and then break out of the function
    """
    # the loop below will check if computer can win in the next move
    pygame.time.wait(700)

    for i in computer_moves:
        moves_dict[6*(i[1]-1)+6-len(i[0])-1] = (0, 0, yellow)
        if is_winner():
            moves_dict[6 * (i[1] - 1) + 6 - len(i[0]) - 1] = 0
            set_piece(i[0], i[1])
            return True
        else:
            moves_dict[6 * (i[1] - 1) + 6 - len(i[0])-1] = 0

    # the loop below will check if opponent can win in the next move and block him
    for i in computer_moves:
        moves_dict[6*(i[1]-1)+6-len(i[0])-1] = (0, 0, red)
        if is_winner():
            moves_dict[6 * (i[1] - 1) + 6 - len(i[0]) - 1] = 0
            set_piece(i[0], i[1])
            return True
        else:
            moves_dict[6 * (i[1] - 1) + 6 - len(i[0])-1] = 0

    # the loop below will compute the best move for the current position:
    # as it's come to my attention there are over 4 trillion cases to consider, I will randomize the move
    else:
        i = choice(computer_moves)
        set_piece(i[0], i[1])
        return True


def mouse_click(m):
    if m[0] in range(5, 91) and m[1] in range(90, 696):
        set_piece(col1, 1)
    elif m[0] in range(105, 196) and m[1] in range(90, 696):
        set_piece(col2, 2)
    elif m[0] in range(205, 296) and m[1] in range(90, 696):
        set_piece(col3, 3)
    elif m[0] in range(305, 396) and m[1] in range(90, 696):
        set_piece(col4, 4)
    elif m[0] in range(405, 496) and m[1] in range(90, 696):
        set_piece(col5, 5)
    elif m[0] in range(505, 596) and m[1] in range(90, 696):
        set_piece(col6, 6)
    elif m[0] in range(605, 696) and m[1] in range(90, 696):
        set_piece(col7, 7)

def moves_layout():
    """
    :return: A string of all the moves currently made on the board, taken from the moves_dict
    This is used strictly for writing the info in the log file for debugging
    """
    return '\n' + str(moves_dict) + '\n\n' + str(col1) + '\n' + str(col2) + '\n' + str(col3) + '\n' + str(col4) + \
           '\n' + str(col5) + '\n' + str(col6) + '\n' + str(col7) + '\n'


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            f.close()
            pygame.quit()
        # --- Game logic should go here
        if not running or is_draw():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and running:
            if not move_count % 2:
                mouse = pygame.mouse.get_pos()  # returns tuple of coords x and y
                mouse_click(mouse)
                f.write(moves_layout())
                if is_winner():
                    f.write("Winner! \n")
                    running = False

        elif move_count >= 1 and move_count % 2 and running:
            if comp_move():
                f.write("Computer move: \n" + moves_layout())
            if is_winner():
                f.write("Winner! \n")
                running = False
    # --- Drawing code should go here
    screen.fill(WHITE)

    for i in range(1, 8):
        try:
            screen.blit(blue, ((i - 1) * 100, 90))
        except:
            f.write("Failed in displaying blue bar")
            pygame.draw.rect(screen, BACKGROUND, [(i - 1) * 100 + 5, 90, 90, 605], 0)
        for j in range(2, 8):
            pygame.draw.circle(screen, ARROWBLUE, (i * 100 - 50, j * 100 - 50), 37, 2)
            pygame.draw.circle(screen, BACKGROUND, (i * 100 - 50, j * 100 - 50), 35)

    for i in moves_dict:
        try:
            screen.blit(moves_dict[i][2], (moves_dict[i][0]-35, moves_dict[i][1]-35))
        except:
            f.write("Failed in displaying a disk")
            continue


    # --- Update the screen
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)
