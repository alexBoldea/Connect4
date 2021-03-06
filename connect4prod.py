"""
Documented bugs: === FIXED ===
                 When calling comp_move(), if a column is full and the column to the left has one piece at the bottom,
                 that piece will disappear.

                 === FIXED ===
                 After making a successful counter-move with the comp_move() function, another pair of moves is made
                 first red, then yellow. This is possibly related to no return statement on comp_move()

                 === FIXED ===
                 After a winner is found and the game is reset by pressing "space" the pieces disappear but the lists
                 appear to be populated. Try a solution based on moves_dict to replace the lists col1 .. col7
                 Solved by redefinition of reset_game() function
"""
import sys, os
from random import choice
import pygame

pygame.init()
clock = pygame.time.Clock()
# window:
size = (700, 700)
screen = pygame.display.set_mode(size)

player_score = 0
computer_score = 0


def display_score():
    game_font = pygame.font.Font('04B_19.TTF',32)
    text = game_font.render("PLAYER 1: " + str(player_score) + "      Evil Computer: " + str(computer_score),
                            True, (240, 87, 22))
    score_rect = text.get_rect(center=(350, 40))
    pygame.display.set_caption("Connect 4")
    screen.blit(text, score_rect)


# Define some colors
BACKGROUND = (172, 204, 227)
WHITE = (200, 200, 200)
ARROWBLUE = (65, 65, 107)

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Define images
red_url = resource_path("red70px.png")
red = pygame.image.load(red_url)
yellow_url = resource_path("yellow70px.png")
yellow = pygame.image.load(yellow_url)
blue_url = resource_path("bluebar.png")
blue = pygame.image.load(blue_url)

# Define global scope variables
moves_dict = {} # will keep track of what moves were made
for _ in range(42):
    moves_dict[_] = 0


col1, col2, col3, col4, col5, col6, col7 = [], [], [], [], [], [], [] # will keep track of how the columns are filled
move_count = 0
computer_moves = [(col1, 1), (col2, 2), (col3, 3), (col4, 4), (col5, 5), (col6, 6), (col7, 7)]
running = True


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


def is_winner():
    """
    :return: True if win condition is found, else False
    except covers IndexError and TypeError (integer instead of tuple in dict.values())
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


def score():
    """
    Should display on top of the window text related to Player 1 and Player 2 the current score (games won)
    """
    global player_score, computer_score
    if move_count % 2:
        player_score += 1
    else:
        computer_score += 1


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

    for i in computer_moves: # this will pass through the 7 possible moves
        if len(i[0]) > 5:       # this condition should fix the "disappearing piece" bug
            continue
        if moves_dict[(i[1]-1)*6 + 6 - len(i[0]) - 1] == 0:   # (i[1] takes the values 1 to 7 inclusive
                                                              # -1 takes the values 0 to 6 inclusive
                                                              # )*6 times 6 takes the values 0, 6, ... 36
                                                              # +6 takes the values 6, 12, ... 42
                                                              # -len(i[0]) takes the value of the length of i[0] (can be 0 to 6)

                                                              # this needs to be checked, if the column is already full( len = 6)
                                                              # then the move is invalid and i should be skipped

                                                              # -1] to be able to start from the bottom (e.g. position 5)

            moves_dict[6*(i[1]-1)+6-len(i[0])-1] = (0, 0, yellow) # checks for computer win possibility
            if is_winner():
                set_piece(i[0], i[1])
                return True
            else:
                moves_dict[6*(i[1]-1)+6-len(i[0])-1] = (0, 0, red) # checks for user win and blocks it
                if is_winner():
                    set_piece(i[0], i[1])
                    return True
                else:
                    moves_dict[6 * (i[1] - 1) + 6 - len(i[0])-1] = 0

    # the code below will compute the best move for the current position:
    # as it's come to my attention there are over 4 trillion cases to consider, I will randomize the move
    else:
        j = choice(computer_moves)
        while len(j[0]) > 5:
            j = choice(computer_moves) # this ensures the function set_piece() is called for a valid move
        set_piece(j[0], j[1])
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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # --- Game logic should go here
        if not running or is_draw():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and running:
            if not move_count % 2:
                mouse = pygame.mouse.get_pos()  # returns tuple of coords x and y
                mouse_click(mouse)
                if is_winner():
                    score()
                    running = False

        elif move_count >= 1 and move_count % 2 and running:
            comp_move()
            if is_winner():
                score()
                running = False
    # --- Drawing code should go here
    screen.fill(WHITE)
    for i in range(1, 8):
        try:
            screen.blit(blue, ((i - 1) * 100, 90))
        except:
            pygame.draw.rect(screen, BACKGROUND, [(i - 1) * 100 + 5, 90, 90, 605], 0)
        for j in range(2, 8):
            pygame.draw.circle(screen, ARROWBLUE, (i * 100 - 50, j * 100 - 50), 37, 2)
            pygame.draw.circle(screen, BACKGROUND, (i * 100 - 50, j * 100 - 50), 35)

    for i in moves_dict:
        try:
            screen.blit(moves_dict[i][2], (moves_dict[i][0]-35, moves_dict[i][1]-35))
        except:
            continue

    # --- Update the screen
    display_score()
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)
