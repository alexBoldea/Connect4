import pygame
pygame.init()

# Define some colors
BACKGROUND = (172, 204, 227)
WHITE = (255, 255, 255)
YELLOW = (255, 242, 0)
RED = (189, 15, 15)
ARROWBLUE = (65, 65, 107)

# Define global scope variables
moves_dict = {} # will keep track of what moves were made
size = (700, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")
carryOn = True
clock = pygame.time.Clock()
col1, col2, col3, col4, col5, col6, col7 = [], [], [], [], [], [], [] # will keep track of how the columns are filled
move_count = 0

# Define the functions used
def set_piece(x, col):
    """
    :param x: will be called as one of the lists col1 .. col7
    :param col: will be an int value 1 to 7
    :return: will return tuple of coords and color for move or nothing if list is full (len(x) >= 6)
    will set color based on turn
    """
    global move_count
    if len(x) >= 6:
        return None
    else:
        move_count += 1
        x.append(1)
        x_coord = col * 100 - 50
        y_coord = 750 - len(x) * 100
        color = RED if move_count % 2 else YELLOW
        # populate the moves_dict with key: value pairs such that key in range(0, 42) and values are tuples(x_coord, y_coord, color)
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
        except KeyError:
            continue
    # horizontal win cases:
    for i in range(24):
        try:
            if moves_dict[i][2] == moves_dict[i+6][2] == moves_dict[i+12][2] == moves_dict[i+18][2]:
                return True
        except IndexError:
            continue
        except KeyError:
            continue
    # first diagonal win cases:
    for i in [0, 1, 2, 6, 7, 8, 12, 13, 14, 18, 19, 20]:
        try:
            if moves_dict[i][2] == moves_dict[i+7][2] == moves_dict[i+14][2] == moves_dict[i+21][2]:
                return True
        except IndexError:
            continue
        except KeyError:
            continue
    # second diagonal win cases:
    for i in [18, 19, 20, 24, 25, 26, 30, 31, 32, 36, 37, 38]:
        try:
            if moves_dict[i][2] == moves_dict[i-5][2] == moves_dict[i-10][2] == moves_dict[i-15][2]:
                return True
        except IndexError:
            continue
        except KeyError:
            continue
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
    Should call set_piece() with the move decided
    """


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


while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        # --- Game logic should go here
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()  # returns tuple of coords x and y
            mouse_click(mouse)
            if is_winner():
                print("winner!")
                carryOn = False
    # --- Drawing code should go here
    screen.fill(WHITE)

    for i in range(1, 8):
        pygame.draw.rect(screen, BACKGROUND, [(i - 1) * 100 + 5, 90, 90, 605], 0)
        for j in range(2, 8):
            pygame.draw.circle(screen, ARROWBLUE, (i * 100 - 50, j * 100 - 50), 40, 5)

    for i in moves_dict:
        pygame.draw.circle(screen, moves_dict[i][2], (moves_dict[i][0], moves_dict[i][1]), 35)


    # --- Update the screen
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
