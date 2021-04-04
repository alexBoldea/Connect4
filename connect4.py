import pygame

pygame.init()

# Define some colors
BACKGROUND = (172, 204, 227)
WHITE = (255, 255, 255)
YELLOW = (255, 242, 0)
RED = (189, 15, 15)
ARROWBLUE = (65, 65, 107)

moves_dict = {}

size = (700, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")

carryOn = True
clock = pygame.time.Clock()

col1, col2, col3, col4, col5, col6, col7 = [], [], [], [], [], [], []
move_count = 0


def set_piece(x, col):
    """
    :param x: will be called as one of the lists col1 .. col7
    :param col: will be an int value 1 to 7
    :return: will return tuple of coords and color for move or nothing if list is full (len(x) >= 6)
    will set color based on turn
    """
    global move_count
    move_count += 1
    x.append(1)
    if len(x) > 6:
        return None
    else:
        x_coord = col * 100 - 50
        y_coord = 750 - len(x) * 100
        color = YELLOW if move_count % 2 else RED
        # populate the moves_dict with key: value pairs such that key in range(0, 42) and values are tuples(x_coord, y_coord, color)
        moves_dict[6*(col-1)+6-len(x)] = (x_coord, y_coord, color)
        # for i in moves_dict:
        #     print(i, moves_dict[i][0], moves_dict[i][1], moves_dict[i][2])



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
    # --- Drawing code should go here
    screen.fill(WHITE)

    for i in range(1, 8):
        pygame.draw.rect(screen, BACKGROUND, [(i - 1) * 100 + 5, 90, 90, 605], 0)
        for j in range(2, 8):
            pygame.draw.circle(screen, ARROWBLUE, (i * 100 - 50, j * 100 - 50), 40, 5)

    for i in moves_dict:
        pygame.draw.circle(screen, moves_dict[i][2], (moves_dict[i][0], moves_dict[i][1]), 35)


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
