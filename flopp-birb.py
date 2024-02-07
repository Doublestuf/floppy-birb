import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Floppy Birb")
pygame.display.set_icon(pygame.image.load("icon.png"))

#set up music
pygame.mixer_music.load("song.wav")
pygame.mixer_music.set_volume(0.5)
pygame.mixer_music.play(loops=-1)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

YELLOW = (255, 255, 100)
LIGHTBLUE = (100, 160, 200)
DARKGREEN = (50, 100, 50)

#images
bird_image = pygame.image.load("flapp.png")
top_pipe_image = pygame.image.load("pipe.png")
bottom_pipe_image = pygame.transform.flip(pygame.image.load("pipe.png"), 0, 1) #flip the pipe image

#background
title_background = pygame.image.load("titlescreen.png")

#sounds
select_sound = pygame.mixer.Sound("select.wav")
jump_sound = pygame.mixer.Sound("jump.wav")
death_sound = pygame.mixer.Sound("die.wav")
score_sound = pygame.mixer.Sound("score.wav")

# Bird properties
bird_width = 40
bird_height = 30
bird_x = SCREEN_WIDTH // 2 - bird_width // 2
bird_y = SCREEN_HEIGHT // 2 - bird_height // 2
bird_speed = 0
gravity = 0.25
jump_strength = -6

# Pipe properties
pipe_width = 50
pipe_gap = 150
pipe_frequency = 100
pipe_list = []
score_pipes = []

# Score
score = 0
font = pygame.font.Font(None, 50)
outline_font = pygame.font.Font(None, 52)

# Function to draw text on screen
def draw_text(text, font: pygame.font.Font, color, x, y):
    outline_surface = font.render(text, True, BLACK)
    outline_surface.set_alpha(40)
    
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    
    screen.blit(outline_surface, text_rect.move(-2, 0))
    # screen.blit(outline_surface, text_rect.move(2, 0))
    # screen.blit(outline_surface, text_rect.move(0, -2))
    screen.blit(outline_surface, text_rect.move(0, 2))
    
    screen.blit(text_surface, text_rect)

# Function to generate pipes
def create_pipe():
    random_pipe_y = random.randint(pipe_gap, SCREEN_HEIGHT - pipe_gap)
    bottom_pipe_rect = pygame.Rect(SCREEN_WIDTH + 100, random_pipe_y + pipe_gap // 2, pipe_width, SCREEN_HEIGHT - random_pipe_y - pipe_gap // 2)
    top_pipe_rect = pygame.Rect(SCREEN_WIDTH + 100, 0, pipe_width, random_pipe_y - pipe_gap // 2)
    return bottom_pipe_rect, top_pipe_rect

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= 2
    return pipes

# Function to draw pipes
def draw_pipes(top_pipes, bottom_pipes):
    for pipe in top_pipes:
        rect = top_pipe_image.get_rect()
        rect.topleft = pipe.topleft
        screen.blit(top_pipe_image, rect)
    
    for pipe in bottom_pipes:
        rect = top_pipe_image.get_rect()
        rect.bottomleft = pipe.bottomleft
        screen.blit(bottom_pipe_image, rect)

# Function to check collision
def check_collision(pipes):
    global bird_y, bird_speed, score

    for pipe in pipes:
        if pipe.colliderect(bird_rect):
            return True

    if bird_y <= 0 or bird_y >= SCREEN_HEIGHT - bird_height:
        return True

    return False

#save and get highscore for death screen
def save_highscore():
        write_file = open('highscore.txt', 'w')
        write_file.write(str(score))
    
def get_highscore():
    read_file = open('highscore.txt', 'r')
    saved_score = int(read_file.read())
    read_file.close()
    
    if score > saved_score:
        save_highscore()
        return score
    return saved_score

# Title screen
title_font = pygame.font.Font(None, 60)
title_text = title_font.render("Floppy Birb", True, WHITE)
title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

instructions_font = pygame.font.Font(None, 40)
instructions_text = instructions_font.render("Press Space to Start", True, WHITE)
instructions_text_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

# Game states
title_screen = True
game_running = False
game_over = False

# Game Over screen
game_over_font = pygame.font.Font(None, 60)
game_over_text = game_over_font.render("Game Over", True, WHITE)
game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

restart_font = pygame.font.Font(None, 40)
restart_text = restart_font.render("Press Space to Restart", True, WHITE)
restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if title_screen:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                title_screen = False
                game_running = True
                select_sound.play()
        elif game_running:
            if (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP)) or event.type == pygame.MOUSEBUTTONDOWN:
                bird_speed = jump_strength
                jump_sound.play()
        elif game_over:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONUP:
                game_over = False
                game_running = True
                bird_y = SCREEN_HEIGHT // 2 - bird_height // 2
                bird_speed = 0
                pipe_list = []
                score_pipes = []
                score = 0
                select_sound.play()

    if title_screen:
        screen.fill(LIGHTBLUE)
        draw_text("Floppy Birb", title_font, WHITE, title_text_rect.centerx, title_text_rect.y)
        draw_text("Press SPACE to start", instructions_font, WHITE, instructions_text_rect.centerx, instructions_text_rect.y)
    elif game_running:
        # Move bird
        bird_speed += gravity
        bird_y += bird_speed

        # Bird rectangle
        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

        # Generate pipes
        frequency = random.randrange(pipe_frequency + 50, pipe_frequency + 100) if random.choice([True, False]) else random.randrange(pipe_frequency, pipe_frequency + 50)
        if len(pipe_list) == 0 or pipe_list[-1].x < SCREEN_WIDTH - frequency:
            pipes = create_pipe()
            score_pipes.append(pipes[0])
            pipe_list.extend(pipes)

        # Move pipes
        pipe_list = move_pipes(pipe_list)

        # Remove off-screen pipes
        pipe_list = [pipe for pipe in pipe_list if pipe.right > 0]

        # Draw background
        screen.fill(LIGHTBLUE)

        # Draw pipes
        draw_pipes(score_pipes, [pipe for pipe in pipe_list if pipe not in score_pipes])

        # Draw bird
        rect = bird_image.get_rect()
        rect.center = bird_rect.center
        
        screen.blit(bird_image, rect)

        # Draw score
        draw_text(f"Score: {score}", font, WHITE, SCREEN_WIDTH // 2, 50)

        # Check collision
        if check_collision(pipe_list):
            # Game over
            game_running = False
            game_over = True
            death_sound.play()

        # Check for score
        for pipe in score_pipes: 
            if pipe.x + pipe.width == bird_x:
                score += 1
                score_sound.play()
    elif game_over:
        screen.fill(LIGHTBLUE)
        highscore = get_highscore()
        draw_text(f"Highscore: {highscore}", instructions_font, WHITE, title_text_rect.centerx, title_text_rect.y - 100)
        draw_text("Game Over", game_over_font, WHITE, game_over_text_rect.centerx, game_over_text_rect.y)
        draw_text("Press SPACE to Restart", restart_font, WHITE, restart_text_rect.centerx, restart_text_rect.y)

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)
