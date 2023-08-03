import pygame

# By Sharaf Eddine BOUKHEZER
# On 02/08/2023
# Maze game : MatahAdventure


pygame.init()

# Set up the game window
margin = 20
width, height = 560, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("MatahAdventure")

logo_image = pygame.image.load("matahadventure_logo.png")
pygame.display.set_icon(logo_image)

background_image = pygame.image.load("matahadventure.png")
background_image = pygame.transform.scale(background_image, (width, height))

# block and wall sizes
block_size = 40
wall_size = 2

# player settings
player_width, player_height = 20, 20
player_color = (255, 0, 0)  # Red
player_speed = block_size

# player initial position
player_x, player_y = 2 * block_size + margin + 10, 0 * block_size + margin + 10

# labyrinth settings
labyrinth_width = (width - 2 * margin) // block_size
labyrinth_height = (height - 2 * margin) // block_size
labyrinth = [[{"up": True, "down": True, "left": True, "right": True} for _ in range(labyrinth_width)] for _ in
             range(labyrinth_height)]


# blocks class
class Block:
    def __init__(self, up=True, down=True, right=True, left=True):
        self.up = up
        self.down = down
        self.right = right
        self.left = left


# create blocks
block_possibilities = [
    Block(up=False, down=False, right=False, left=False),
    Block(up=False),
    Block(left=False),
    Block(down=False),
    Block(right=False),
    Block(up=False, down=False),
    Block(left=False, right=False),
    Block(left=False, down=False),
    Block(up=False, right=False),
    Block(right=False, down=False),
    Block(up=False, left=False),
    Block(up=False, right=False, down=False),
    Block(left=False, right=False, down=False),
    Block(up=False, left=False, right=False),
    Block(up=False, left=False, down=False)
]


# draw labyrinth
def assign_block_configuration():
    labyrinth_structure = [
        [9, 6, 6, 12, 12, 6, 6, 2, 4, 7, 9, 6, 7],
        [8, 12, 2, 5, 1, 3, 9, 6, 7, 5, 5, 3, 5],
        [4, 13, 7, 8, 12, 13, 14, 9, 10, 5, 11, 10, 5],
        [9, 7, 8, 2, 5, 9, 10, 8, 6, 0, 10, 3, 5],
        [5, 8, 6, 7, 1, 8, 6, 2, 3, 1, 9, 0, 14],
        [5, 4, 7, 8, 6, 12, 6, 6, 13, 7, 5, 1, 5],
        [8, 7, 11, 12, 2, 8, 7, 9, 6, 14, 1, 3, 5],
        [9, 10, 5, 8, 6, 7, 1, 8, 7, 11, 6, 10, 5],
        [8, 6, 13, 2, 3, 8, 6, 7, 8, 0, 6, 7, 5],
        [9, 6, 6, 6, 13, 6, 6, 10, 3, 5, 4, 10, 5],
        [8, 6, 6, 6, 6, 6, 6, 6, 10, 8, 6, 6, 10]
    ]

    for row in range(labyrinth_height):
        for col in range(labyrinth_width):
            block_number = labyrinth_structure[row][col]
            labyrinth[row][col] = block_possibilities[block_number]


labyrinth = [[Block() for _ in range(labyrinth_width)] for _ in range(labyrinth_height)]
assign_block_configuration()

# Define the row and column of the winning block
winning_row, winning_col = 10, 7


def draw_game():
    window.blit(background_image, (0, 0))
    black = (0, 0, 0)
    # draw labyrinth
    for row in range(len(labyrinth)):
        for col in range(len(labyrinth[0])):
            x, y = col * block_size + margin, row * block_size + margin
            block = labyrinth[row][col]
            if block.up:
                pygame.draw.rect(window, black, (x, y, block_size, wall_size))
            if block.down:
                pygame.draw.rect(window, black, (x, y + block_size - wall_size, block_size, wall_size))
            if block.right:
                pygame.draw.rect(window, black, (x + block_size - wall_size, y, wall_size, block_size))
            if block.left:
                pygame.draw.rect(window, black, (x, y, wall_size, block_size))
            if row == 10 and col == 7:
                pygame.draw.rect(window, (0, 255, 0),
                                 (x + wall_size, y + wall_size, block_size - 2 * wall_size, block_size - 2 * wall_size))

    pygame.draw.rect(window, player_color, (player_x, player_y, player_width, player_height))

    pygame.display.update()


# Define the row and column of the winning block
winning_row, winning_col = 10, 7

# Game loop
running = True
moved_this_click = False  # Flag to track if the player has moved in the current click
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Calculate the potential new position based on key presses
    dx, dy = 0, 0
    block = labyrinth[(player_y - margin) // block_size][(player_x - margin) // block_size]

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and not moved_this_click and not block.up:
            player_y -= block_size
            moved_this_click = True
        elif event.key == pygame.K_DOWN and not moved_this_click and not block.down:
            player_y += block_size
            moved_this_click = True
        elif event.key == pygame.K_RIGHT and not moved_this_click and not block.right:
            player_x += block_size
            moved_this_click = True
        elif event.key == pygame.K_LEFT and not moved_this_click and not block.left:
            player_x -= block_size
            moved_this_click = True

    if event.type == pygame.KEYUP:
        moved_this_click = False

    # Check if the player has reached the winning block
    if (player_y - margin) // block_size == winning_row and (player_x - margin) // block_size == winning_col:
        print("Congratulations! You have won the game!")
        running = False

    draw_game()

# Quit Pygame and the program
pygame.quit()
