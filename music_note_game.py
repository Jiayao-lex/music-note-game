import pygame
import sys
import random
import os
import math
import pathlib

# --- 公共配置 ---
WIDTH, HEIGHT = 900, 600
WHITE = (250, 250, 255)
BLACK = (30, 30, 30)
RED = (220, 60, 60)
BLUE = (80, 120, 220)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Note Recognition Game")
clock = pygame.time.Clock()

# Helper for PyInstaller --onefile: resource_path will return
# the path to bundled resources when running inside a PyInstaller
# executable, otherwise it returns the normal filesystem path.
def resource_path(relative_path):
    # if running as a PyInstaller bundle, sys._MEIPASS holds the temp folder
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- UI选择界面 ---
def draw_menu():
    # 渐变背景
    for y in range(HEIGHT):
        color = (220 - y//20, 230 - y//30, 255)
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))
    # 顶部英文提示（加粗加阴影）
    font = pygame.font.Font(None, 54)
    tip = font.render("Select one clef you want to practice.", True, (40,40,80))
    shadow = font.render("Select one clef you want to practice.", True, (180,180,220))
    screen.blit(shadow, (WIDTH//2 - tip.get_width()//2 + 2, 62))
    screen.blit(tip, (WIDTH//2 - tip.get_width()//2, 60))
    # 加载高音谱号和低音谱号图片（始终显示）
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    gclef_path = resource_path(os.path.join(assets_dir, 'g-clef.png'))
    fclef_path = resource_path(os.path.join(assets_dir, 'f-clef.png'))
    gclef_img = None
    fclef_img = None
    try:
        if os.path.exists(gclef_path):
            gclef_img = pygame.image.load(gclef_path).convert_alpha()
            scale_height = 80
            scale_width = int(gclef_img.get_width() * (scale_height / gclef_img.get_height()))
            gclef_img = pygame.transform.smoothscale(gclef_img, (scale_width, scale_height))
    except Exception as e:
        gclef_img = None
    try:
        if os.path.exists(fclef_path):
            fclef_img = pygame.image.load(fclef_path).convert_alpha()
            scale_height = 80
            scale_width = int(fclef_img.get_width() * (scale_height / fclef_img.get_height()))
            fclef_img = pygame.transform.smoothscale(fclef_img, (scale_width, scale_height))
    except Exception as e:
        fclef_img = None

    # 鼠标悬停高亮
    mx, my = pygame.mouse.get_pos()
    treble_rect = pygame.Rect(WIDTH//2-60, 220, 120, 80)
    bass_rect = pygame.Rect(WIDTH//2-60, 320, 120, 80)
    if treble_rect.collidepoint(mx, my):
        pygame.draw.rect(screen, (180,220,255,80), treble_rect, border_radius=18)
    if bass_rect.collidepoint(mx, my):
        pygame.draw.rect(screen, (180,220,255,80), bass_rect, border_radius=18)

    # 在按钮区域居中显示图片和说明文字
    if gclef_img:
        gclef_rect = gclef_img.get_rect()
        gclef_rect.centerx = WIDTH // 2
        gclef_rect.centery = 220 + 35
        screen.blit(gclef_img, gclef_rect)
    if fclef_img:
        fclef_rect = fclef_img.get_rect()
        fclef_rect.centerx = WIDTH // 2
        fclef_rect.centery = 320 + 35
        screen.blit(fclef_img, fclef_rect)

    pygame.display.flip()

    print("gclef_path:", gclef_path)
    if gclef_img:
        print("g-clef loaded and ready to display")
    else:
        print("g-clef NOT loaded")

    print("fclef_path:", fclef_path)
    if fclef_img:
        print("f-clef loaded and ready to display")
    else:
        print("f-clef NOT loaded")

def menu_loop():
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH//2-160 < x < WIDTH//2+160 and 220 < y < 290:
                    return 'treble'
                if WIDTH//2-160 < x < WIDTH//2+160 and 320 < y < 390:
                    return 'bass'
        clock.tick(30)

# --- 高音谱号识别功能（main.py核心） ---
def run_treble():
    STAFF_X = 120
    STAFF_Y = 300
    STAFF_W = 600
    LINE_SPACING = 20
    note_names = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5']
    note_labels = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A']
    note_positions = [STAFF_Y + LINE_SPACING * 5, STAFF_Y + LINE_SPACING * 4.5, STAFF_Y + LINE_SPACING * 4,
                      STAFF_Y + LINE_SPACING * 3.5, STAFF_Y + LINE_SPACING * 3, STAFF_Y + LINE_SPACING * 2.5,
                      STAFF_Y + LINE_SPACING * 2, STAFF_Y + LINE_SPACING * 1.5, STAFF_Y + LINE_SPACING * 1,
                      STAFF_Y + LINE_SPACING * 0.5, STAFF_Y, STAFF_Y - LINE_SPACING * 0.5, STAFF_Y - LINE_SPACING]
    score = 0
    current_note = random.choice(range(len(note_names)))
    running = True
    feedback = None
    feedback_time = 0
    # 不显示谱号图片
    while running:
        screen.fill(WHITE)
        for i in range(5):
            y = STAFF_Y + i * LINE_SPACING
            pygame.draw.line(screen, BLACK, (STAFF_X, y), (STAFF_X + STAFF_W, y), 2)
        note_x = STAFF_X + STAFF_W // 2
        note_y = note_positions[current_note]
        pygame.draw.circle(screen, BLACK, (note_x, int(note_y)), 10)
        pygame.draw.circle(screen, WHITE, (note_x, int(note_y)), 7)
        if current_note <= 1:
            for i in range(2 - current_note):
                y = STAFF_Y + LINE_SPACING * (5 - i)
                pygame.draw.line(screen, BLACK, (note_x - 18, y), (note_x + 18, y), 2)
        if current_note >= 9:
            for i in range(current_note - 8):
                y = STAFF_Y - LINE_SPACING * i
                pygame.draw.line(screen, BLACK, (note_x - 18, y), (note_x + 18, y), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score} | Which note? Press 1-7 (C=1, D=2...) | {note_names[current_note]}", True, BLACK)
        screen.blit(text, (40, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if pygame.K_1 <= event.key <= pygame.K_7:
                    guess = event.key - pygame.K_1
                    if note_labels[guess] == note_labels[current_note]:
                        score += 1
                        feedback = font.render("Correct!", True, RED)
                        current_note = random.choice(range(len(note_names)))
                    else:
                        feedback = font.render(f"Wrong! It was {note_labels[current_note]}", True, RED)
                    feedback_time = pygame.time.get_ticks()
        if feedback and pygame.time.get_ticks() - feedback_time < 1000:
            feedback_rect = feedback.get_rect(center=(WIDTH // 2, HEIGHT - 40))
            screen.blit(feedback, feedback_rect)
        pygame.display.flip()
        clock.tick(60)

# --- 低音谱号识别功能（main_bass.py核心） ---
def run_bass():
    STAFF_X = 120
    STAFF_W = 660
    LINE_SPACING = 32
    STAFF_LINES = 5
    STAFF_TOP = 220
    STAFF_BOTTOM = STAFF_TOP + (STAFF_LINES - 1) * LINE_SPACING
    def line_y(line_idx):
        return STAFF_BOTTOM - line_idx * LINE_SPACING
    def space_y(below_line_idx):
        return (line_y(below_line_idx) + line_y(below_line_idx+1)) / 2
    note_names = ['E2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4']
    note_positions = [
        line_y(0) + LINE_SPACING,   # E2 下加一线
        space_y(1),                 # C3 2间
        line_y(2),                  # D3 3线
        space_y(2),                 # E3 3间
        line_y(3),                  # F3 4线
        space_y(3),                 # G3 4间
        line_y(4),                  # A3 5线
        space_y(4),                 # B3 5线上加间
        line_y(4) - LINE_SPACING    # C4 上加一线
    ]
    score = 0
    current_note = random.randint(0, len(note_names)-1)
    running = True
    feedback = None
    feedback_time = 0
    # 低音谱号图片
    # 使用 assets 路径并兼容 PyInstaller
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    clef_img_path = resource_path(os.path.join(assets_dir, 'f-clef.png'))
    clef_img = None
    if os.path.exists(clef_img_path):
        try:
            clef_img = pygame.image.load(clef_img_path).convert_alpha()
            # 只保留黑色像素
            for x in range(clef_img.get_width()):
                for y in range(clef_img.get_height()):
                    r, g, b, a = clef_img.get_at((x, y))
                    if r < 40 and g < 40 and b < 40:
                        clef_img.set_at((x, y), (0, 0, 0, a))
                    else:
                        clef_img.set_at((x, y), (r, g, b, 0))
            # 缩放为240像素高
            scale_height = 240
            scale_width = int(clef_img.get_width() * (scale_height / clef_img.get_height()))
            clef_img = pygame.transform.smoothscale(clef_img, (scale_width, scale_height))
        except Exception as e:
            print(f"Failed to load clef image: {e}")
    while running:
        screen.fill(WHITE)
        for i in range(STAFF_LINES):
            y = line_y(i)
            pygame.draw.line(screen, BLACK, (STAFF_X, y), (STAFF_X + STAFF_W, y), 2)
        # 不显示谱号图片
        note_x = STAFF_X + STAFF_W // 2
        note_y = note_positions[current_note]
        pygame.draw.circle(screen, BLACK, (note_x, int(note_y)), 14)
        pygame.draw.circle(screen, WHITE, (note_x, int(note_y)), 10)
        if note_names[current_note] == 'E2':
            y = note_y
            pygame.draw.line(screen, BLACK, (note_x-22, y), (note_x+22, y), 2)
        if note_names[current_note] == 'C4':
            y = note_y
            pygame.draw.line(screen, BLACK, (note_x-22, y), (note_x+22, y), 2)
        font2 = pygame.font.Font(None, 36)
        text = font2.render(f"Score: {score} | 1-7 = C3~B3", True, BLACK)
        screen.blit(text, (40, 20))
        font3 = pygame.font.Font(None, 28)
        info = font3.render("C=1  D=2  E=3  F=4  G=5  A=6  B=7", True, BLUE)
        screen.blit(info, (40, 60))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if pygame.K_1 <= event.key <= pygame.K_7:
                    guess = event.key - pygame.K_1
                    if current_note == 0:
                        correct = 2  # E2 = 3 (E)
                    elif current_note == 8:
                        correct = 0  # C4 = 1 (C)
                    else:
                        correct = current_note - 1
                    if guess == correct:
                        score += 1
                        feedback = font2.render("Correct!", True, (0,180,0))
                        feedback_time = pygame.time.get_ticks()
                        current_note = random.randint(0, len(note_names)-1)
                    else:
                        feedback = font2.render(f"Wrong! {note_names[current_note]}", True, RED)
                        feedback_time = pygame.time.get_ticks()
        if feedback and pygame.time.get_ticks() - feedback_time < 1000:
            feedback_rect = feedback.get_rect(center=(WIDTH // 2, HEIGHT - 40))
            screen.blit(feedback, feedback_rect)
        pygame.display.flip()
        clock.tick(60)

# --- 主流程 ---
while True:
    mode = menu_loop()
    if mode == 'treble':
        run_treble()
    elif mode == 'bass':
        run_bass()
    else:
        break
pygame.quit()
