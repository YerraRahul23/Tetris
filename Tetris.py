import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 950
HEIGHT = 700
PLAY_WIDTH = 450  # 15 blocks wide
PLAY_HEIGHT = 600  # 20 blocks tall
BLOCK_SIZE = 30

# Position the play area in the center
TOP_LEFT_X = (WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = HEIGHT - PLAY_HEIGHT

# Tetromino shapes
SHAPES = [
    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],  # O
    [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']],  # I
    [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....']],  # T
    [['.....',
      '.00..',
      '..00.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],  # S
    [['.....',
      '..00.',
      '.00..',
      '.....',
      '.....'],
     ['.....',
      '.0...',
      '.00..',
      '..0..',
      '.....']]   # Z
]

COLORS = [
    (255, 255, 0),  # Yellow (O)
    (0, 255, 255),  # Cyan (I)
    (128, 0, 128),  # Purple (T)
    (0, 255, 0),    # Green (S)
    (255, 0, 0)     # Red (Z)
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(15)] for _ in range(20)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x],
                           (TOP_LEFT_X + x * BLOCK_SIZE,
                            TOP_LEFT_Y + y * BLOCK_SIZE,
                            BLOCK_SIZE, BLOCK_SIZE), 0)

def draw_window(surface, grid, score):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))
    
    # Draw score
    score_label = pygame.font.SysFont('comicsans', 30).render(f'Score: {score}', 1, (255, 255, 255))
    surface.blit(score_label, (TOP_LEFT_X + PLAY_WIDTH + 10, TOP_LEFT_Y + 20))
    
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0),
                    (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)
    pygame.display.update()

def draw_game_over(surface, score):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 60)
    game_over_label = font.render('Game Over', 1, (255, 255, 255))
    score_label = font.render(f'Score: {score}', 1, (255, 255, 255))
    surface.blit(game_over_label, (WIDTH // 2 - game_over_label.get_width() // 2, HEIGHT // 3))
    surface.blit(score_label, (WIDTH // 2 - score_label.get_width() // 2, HEIGHT // 2 - 50))

    # Restart button
    button_font = pygame.font.SysFont('comicsans', 40)
    button_text = button_font.render('Restart', 1, (255, 255, 255))
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
    pygame.draw.rect(surface, (0, 128, 0), button_rect)
    pygame.draw.rect(surface, (255, 255, 255), button_rect, 2)
    surface.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                              button_rect.y + (button_rect.height - button_text.get_height()) // 2))
    
    pygame.display.update()
    return button_rect

def valid_space(piece, grid):
    accepted_pos = [[(x, y) for x in range(15) if grid[y][x] == (0,0,0)] for y in range(20)]
    accepted_pos = [pos for sub in accepted_pos for pos in sub]
    
    formatted = convert_shape_format(piece)
    
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))
    
    return positions

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    
    return inc

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    while True:  # Outer loop for restarting
        locked_positions = {}
        grid = create_grid(locked_positions)
        
        change_piece = False
        run = True
        current_piece = Piece(7, 0, random.choice(SHAPES))
        next_piece = Piece(7, 0, random.choice(SHAPES))
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.27
        score = 0

        while run:
            grid = create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            clock.tick()

            if fall_time/1000 > fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not valid_space(current_piece, grid) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        current_piece.rotation += 1
                        if not valid_space(current_piece, grid):
                            current_piece.rotation -= 1

            shape_pos = convert_shape_format(current_piece)

            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_piece.color

            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = Piece(7, 0, random.choice(SHAPES))
                change_piece = False
                score += clear_rows(grid, locked_positions) * 10

            draw_window(screen, grid, score)

            if check_lost(locked_positions):
                run = False

        # Game over screen with restart button
        button_rect = draw_game_over(screen, score)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        waiting = False  # Restart the game

if __name__ == "__main__":
    main()
