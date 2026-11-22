import pygame
import sys
import random
import os

# ==========================================
# 1. INISIALISASI PYGAME
# ==========================================

pygame.init()

try:
    pygame.mixer.init()
except pygame.error:
    pass

WIDTH = 600
HEIGHT = 400
HUD_HEIGHT = 40
WINDOW_HEIGHT = HEIGHT + HUD_HEIGHT

CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game - Dokterweb")

clock = pygame.time.Clock()

# ==========================================
# 2. FONT
# ==========================================

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)
title_font = pygame.font.SysFont("Arial", 48, bold=True)

# ==========================================
# 3. WARNA
# ==========================================

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

GREEN = (46, 204, 113)
DARK_GREEN = (30, 150, 80)
LIGHT_GREEN = (100, 230, 140)

RED = (231, 76, 60)
BLUE = (52, 152, 219)
GRAY = (150, 160, 170)

DARK_BG = (25, 35, 45)
GRID_COLOR = (38, 50, 62)
PANEL_COLOR = (35, 48, 60)

APPLE_RED = (235, 55, 65)
APPLE_GREEN = (80, 190, 90)

# ==========================================
# 4. SOUND EFFECT
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

eat_sound = None
game_over_sound = None

if pygame.mixer.get_init():

    try:
        eat_sound = pygame.mixer.Sound(
            os.path.join(BASE_DIR, "sounds", "eat.mp3")
        )

        game_over_sound = pygame.mixer.Sound(
            os.path.join(BASE_DIR, "sounds", "game_over.mp3")
        )

    except pygame.error as error:
        print("Sound tidak dapat dimuat:", error)


# ==========================================
# 5. GAME STATE
# ==========================================

game_state = "menu"

# ==========================================
# 6. TOMBOL MENU
# ==========================================

play_button = pygame.Rect(200, 170, 200, 50)
instruction_button = pygame.Rect(200, 235, 200, 50)
quit_button = pygame.Rect(200, 300, 200, 50)

back_button = pygame.Rect(200, 340, 200, 45)

restart_button = pygame.Rect(200, 245, 200, 50)
menu_button = pygame.Rect(200, 310, 200, 50)


# ==========================================
# 7. DATA PERMAINAN
# ==========================================

snake = []

direction = (CELL_SIZE, 0)

food = [0, 0]

score = 0

move_delay = 150

last_move_time = 0


# ==========================================
# 8. MEMBUAT MAKANAN
# ==========================================

def generate_food():

    while True:

        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)

        new_food = [x, y]

        if new_food not in snake:
            return new_food


# ==========================================
# 9. RESTART GAME
# ==========================================

def restart_game():

    global snake, direction, food
    global score, last_move_time

    snake = [
        [100, 100],
        [80, 100],
        [60, 100]
    ]

    direction = (CELL_SIZE, 0)

    score = 0

    food = generate_food()

    last_move_time = pygame.time.get_ticks()


# ==========================================
# 10. MENAMPILKAN TEKS
# ==========================================

def draw_text(text, font_style, color, x, y):

    text_surface = font_style.render(
        text,
        True,
        color
    )

    text_rect = text_surface.get_rect(
        center=(x, y)
    )

    screen.blit(text_surface, text_rect)


# ==========================================
# 11. MEMBUAT TOMBOL
# ==========================================

def draw_button(rect, text, color):

    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):

        button_color = tuple(
            min(channel + 25, 255)
            for channel in color
        )

    else:

        button_color = color

    pygame.draw.rect(
        screen,
        button_color,
        rect,
        border_radius=10
    )

    draw_text(
        text,
        font,
        WHITE,
        rect.centerx,
        rect.centery
    )


# ==========================================
# 12. MENU UTAMA
# ==========================================

def draw_menu():

    screen.fill(DARK_BG)

    draw_text(
        "SNAKE GAME",
        title_font,
        GREEN,
        WIDTH // 2,
        100
    )

    draw_text(
        "Belajar membuat game dengan Python",
        small_font,
        WHITE,
        WIDTH // 2,
        135
    )

    draw_button(
        play_button,
        "PLAY GAME",
        GREEN
    )

    draw_button(
        instruction_button,
        "INSTRUCTIONS",
        BLUE
    )

    draw_button(
        quit_button,
        "QUIT",
        RED
    )


# ==========================================
# 13. INSTRUCTIONS
# ==========================================

def draw_instructions():

    screen.fill(DARK_BG)

    draw_text(
        "HOW TO PLAY",
        title_font,
        GREEN,
        WIDTH // 2,
        70
    )

    instructions = [
        "1. Gunakan tombol panah keyboard",
        "   untuk menggerakkan ular.",
        "",
        "2. Tangkap makanan berwarna merah.",
        "",
        "3. Setiap makanan menambah 10 poin.",
        "",
        "4. Jangan menabrak dinding atau tubuh sendiri."
    ]

    y = 135

    for line in instructions:

        draw_text(
            line,
            small_font,
            WHITE,
            WIDTH // 2,
            y
        )

        y += 28

    draw_button(
        back_button,
        "BACK TO MENU",
        BLUE
    )


# ==========================================
# 14. BACKGROUND GRID
# ==========================================

def draw_grid():

    # Area permainan dimulai setelah panel skor

    screen.fill(DARK_BG)

    for x in range(0, WIDTH, CELL_SIZE):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, HUD_HEIGHT),
            (x, WINDOW_HEIGHT)
        )

    for y in range(0, HEIGHT + 1, CELL_SIZE):

        screen_y = y + HUD_HEIGHT

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, screen_y),
            (WIDTH, screen_y)
        )


# ==========================================
# 15. DESAIN APEL
# ==========================================

def draw_apple():

    x, y = food

    # Sesuaikan posisi apel dengan HUD

    screen_y = y + HUD_HEIGHT

    # Batang apel
    pygame.draw.line(
        screen,
        (120, 75, 35),
        (x + 10, screen_y + 5),
        (x + 10, screen_y + 1),
        3
    )

    # Daun apel
    pygame.draw.ellipse(
        screen,
        APPLE_GREEN,
        (x + 10, screen_y, 8, 5)
    )

    # Badan apel
    pygame.draw.circle(
        screen,
        APPLE_RED,
        (x + 10, screen_y + 12),
        8
    )

    # Highlight apel
    pygame.draw.circle(
        screen,
        (255, 130, 130),
        (x + 7, screen_y + 9),
        2
    )


# ==========================================
# 16. DESAIN ULAR
# ==========================================

def draw_snake():

    for index, segment in enumerate(snake):

        x, y = segment

        screen_y = y + HUD_HEIGHT

        if index == 0:

            # Kepala ular

            pygame.draw.rect(
                screen,
                LIGHT_GREEN,
                (
                    x,
                    screen_y,
                    CELL_SIZE,
                    CELL_SIZE
                ),
                border_radius=7
            )

            # Posisi mata mengikuti arah ular

            if direction == (CELL_SIZE, 0):

                eyes = [
                    (x + 14, screen_y + 5),
                    (x + 14, screen_y + 15)
                ]

            elif direction == (-CELL_SIZE, 0):

                eyes = [
                    (x + 6, screen_y + 5),
                    (x + 6, screen_y + 15)
                ]

            elif direction == (0, -CELL_SIZE):

                eyes = [
                    (x + 5, screen_y + 6),
                    (x + 15, screen_y + 6)
                ]

            else:

                eyes = [
                    (x + 5, screen_y + 14),
                    (x + 15, screen_y + 14)
                ]

            # Gambar mata

            for eye in eyes:

                pygame.draw.circle(
                    screen,
                    WHITE,
                    eye,
                    3
                )

                pygame.draw.circle(
                    screen,
                    BLACK,
                    eye,
                    1
                )

        else:

            # Tubuh ular

            pygame.draw.rect(
                screen,
                DARK_GREEN,
                (
                    x + 1,
                    screen_y + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                ),
                border_radius=5
            )


# ==========================================
# 17. SCORE PANEL
# ==========================================

def draw_score_panel():

    panel = pygame.Rect(
        0,
        0,
        WIDTH,
        HUD_HEIGHT
    )

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        panel
    )

    # Skor

    score_label = font.render(
        f"SCORE: {score}",
        True,
        WHITE
    )

    screen.blit(
        score_label,
        (15, 5)
    )

    # Petunjuk kontrol

    control_label = small_font.render(
        "ARROW KEYS: MOVE",
        True,
        GRAY
    )

    control_rect = control_label.get_rect(
        midright=(WIDTH - 15, HUD_HEIGHT // 2)
    )

    screen.blit(
        control_label,
        control_rect
    )


# ==========================================
# 18. GAMBAR GAME
# ==========================================

def draw_game():

    # Background grid
    draw_grid()

    # Apel
    draw_apple()

    # Ular
    draw_snake()

    # Panel skor
    draw_score_panel()


# ==========================================
# 19. GERAKAN ULAR
# ==========================================

def move_snake():

    global snake, food, score

    head_x, head_y = snake[0]

    new_head = [
        head_x + direction[0],
        head_y + direction[1]
    ]

    snake.insert(0, new_head)

    # Jika ular memakan apel

    if new_head == food:

        score += 10

        if eat_sound:
            eat_sound.play()

        food = generate_food()

    else:

        snake.pop()


# ==========================================
# 20. CEK TABRAKAN
# ==========================================

def check_collision():

    head = snake[0]

    # Tabrakan dengan dinding

    if (
        head[0] < 0
        or head[0] >= WIDTH
        or head[1] < 0
        or head[1] >= HEIGHT
    ):

        return True

    # Tabrakan dengan tubuh sendiri

    if head in snake[1:]:

        return True

    return False


# ==========================================
# 21. GAME OVER
# ==========================================

def draw_game_over():

    screen.fill(DARK_BG)

    draw_text(
        "GAME OVER",
        title_font,
        RED,
        WIDTH // 2,
        110
    )

    draw_text(
        f"Your Score: {score}",
        font,
        WHITE,
        WIDTH // 2,
        175
    )

    draw_button(
        restart_button,
        "RESTART",
        GREEN
    )

    draw_button(
        menu_button,
        "MAIN MENU",
        BLUE
    )


# ==========================================
# 22. MULAI GAME PERTAMA KALI
# ==========================================

restart_game()


# ==========================================
# 23. MAIN GAME LOOP
# ==========================================

running = True

while running:

    clock.tick(60)

    # --------------------------------------
    # EVENT HANDLING
    # --------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # EVENT MOUSE

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mouse_pos = event.pos

                # MENU UTAMA

                if game_state == "menu":

                    if play_button.collidepoint(mouse_pos):

                        restart_game()
                        game_state = "playing"

                    elif instruction_button.collidepoint(mouse_pos):

                        game_state = "instructions"

                    elif quit_button.collidepoint(mouse_pos):

                        running = False

                # INSTRUCTIONS

                elif game_state == "instructions":

                    if back_button.collidepoint(mouse_pos):

                        game_state = "menu"

                # GAME OVER

                elif game_state == "game_over":

                    if restart_button.collidepoint(mouse_pos):

                        restart_game()
                        game_state = "playing"

                    elif menu_button.collidepoint(mouse_pos):

                        game_state = "menu"

        # EVENT KEYBOARD

        if event.type == pygame.KEYDOWN:

            # MENU

            if game_state == "menu":

                if event.key == pygame.K_RETURN:

                    restart_game()
                    game_state = "playing"

            # INSTRUCTIONS

            elif game_state == "instructions":

                if event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_BACKSPACE
                ):

                    game_state = "menu"

            # PLAYING

            elif game_state == "playing":

                if (
                    event.key == pygame.K_UP
                    and direction != (0, CELL_SIZE)
                ):

                    direction = (0, -CELL_SIZE)

                elif (
                    event.key == pygame.K_DOWN
                    and direction != (0, -CELL_SIZE)
                ):

                    direction = (0, CELL_SIZE)

                elif (
                    event.key == pygame.K_LEFT
                    and direction != (CELL_SIZE, 0)
                ):

                    direction = (-CELL_SIZE, 0)

                elif (
                    event.key == pygame.K_RIGHT
                    and direction != (-CELL_SIZE, 0)
                ):

                    direction = (CELL_SIZE, 0)

            # GAME OVER

            elif game_state == "game_over":

                if event.key == pygame.K_r:

                    restart_game()
                    game_state = "playing"

                elif event.key == pygame.K_m:

                    game_state = "menu"

    # --------------------------------------
    # UPDATE GAME
    # --------------------------------------

    if game_state == "playing":

        current_time = pygame.time.get_ticks()

        if current_time - last_move_time >= move_delay:

            move_snake()

            last_move_time = current_time

            if check_collision():

                game_state = "game_over"

                if game_over_sound:
                    game_over_sound.play()

    # --------------------------------------
    # DRAW SCREEN
    # --------------------------------------

    if game_state == "menu":

        draw_menu()

    elif game_state == "instructions":

        draw_instructions()

    elif game_state == "playing":

        draw_game()

    elif game_state == "game_over":

        draw_game_over()

    pygame.display.update()


# ==========================================
# 24. KELUAR DARI GAME
# ==========================================

pygame.quit()
sys.exit()