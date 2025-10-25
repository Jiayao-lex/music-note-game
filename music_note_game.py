import pygame
import sys
import random
import os
import math
import pathlib
import numpy as np

# --- 公共配置 ---
WIDTH, HEIGHT = 900, 600
WHITE = (250, 250, 255)
BLACK = (30, 30, 30)
RED = (220, 60, 60)
BLUE = (80, 120, 220)

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Note Recognition Game")
clock = pygame.time.Clock()

# --- 音频生成函数 ---
def generate_tone(frequency, duration=0.5, sample_rate=22050):
    """生成指定频率的正弦波音调"""
    n_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, n_samples, False)
    # 生成正弦波
    wave = np.sin(frequency * 2 * np.pi * t)
    # 添加包络线（淡入淡出）避免爆音
    fade_len = int(0.05 * sample_rate)  # 50ms淡入淡出
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    wave[:fade_len] *= fade_in
    wave[-fade_len:] *= fade_out
    # 转换为16位整数
    wave = (wave * 32767).astype(np.int16)
    # 创建立体声（复制单声道）
    stereo_wave = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound(stereo_wave)

# 音符到频率的映射（A4 = 440Hz）
NOTE_FREQUENCIES = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
    'G5': 783.99, 'A5': 880.00,
    # 低音谱号音符
    'E2': 82.41, 'F2': 87.31, 'G2': 98.00, 'A2': 110.00, 'B2': 123.47,
    'C3': 130.81, 'D3': 146.83, 'E3': 164.81,
    'F3': 174.61, 'G3': 196.00, 'A3': 220.00, 'B3': 246.94
}

# 预生成所有音符的声音
print("Generating note sounds...")
NOTE_SOUNDS = {note: generate_tone(freq) for note, freq in NOTE_FREQUENCIES.items()}
print("Sound generation complete!")


# --- 烟花粒子类 ---
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = 60  # 存活帧数
        self.gravity = 0.15
        
    def update(self):
        self.vx *= 0.98
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / 60))
            size = max(1, int(4 * (self.life / 60)))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        colors = [(255, 50, 50), (50, 255, 50), (50, 50, 255), 
                  (255, 255, 50), (255, 50, 255), (50, 255, 255)]
        color = random.choice(colors)
        for _ in range(50):
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.life > 0]
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
    
    def is_finished(self):
        return len(self.particles) == 0

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
    fireworks = []  # 烟花列表
    last_firework_score = 0  # 上次触发烟花的分数
    # 不自动播放初始音符，等待用户交互
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
        text = font.render(f"Score: {score} | Which note? Press 1-7 (C=1, D=2...) | Press SPACE to hear", True, BLACK)
        screen.blit(text, (40, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                # 按空格键播放当前音符
                if event.key == pygame.K_SPACE:
                    if note_names[current_note] in NOTE_SOUNDS:
                        NOTE_SOUNDS[note_names[current_note]].play()
                if pygame.K_1 <= event.key <= pygame.K_7:
                    guess = event.key - pygame.K_1
                    if note_labels[guess] == note_labels[current_note]:
                        score += 1
                        feedback = font.render("Correct!", True, RED)
                        # 答对后播放当前音符（反馈音）
                        if note_names[current_note] in NOTE_SOUNDS:
                            NOTE_SOUNDS[note_names[current_note]].play()
                        current_note = random.choice(range(len(note_names)))
                        # 每得10分触发烟花
                        if score % 10 == 0 and score > last_firework_score:
                            for _ in range(3):  # 同时发射3个烟花
                                fw_x = random.randint(200, WIDTH - 200)
                                fw_y = random.randint(150, 350)
                                fireworks.append(Firework(fw_x, fw_y))
                            last_firework_score = score
                    else:
                        # 答错后播放正确的音符（让用户听到正确答案）
                        if note_names[current_note] in NOTE_SOUNDS:
                            NOTE_SOUNDS[note_names[current_note]].play()
                        feedback = font.render(f"Wrong! It was {note_labels[current_note]}", True, RED)
                    feedback_time = pygame.time.get_ticks()
        if feedback and pygame.time.get_ticks() - feedback_time < 1000:
            feedback_rect = feedback.get_rect(center=(WIDTH // 2, HEIGHT - 40))
            screen.blit(feedback, feedback_rect)
        # 更新和绘制烟花
        for firework in fireworks:
            firework.update()
            firework.draw(screen)
        fireworks = [fw for fw in fireworks if not fw.is_finished()]
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
    
    # 低音谱号标准音符位置
    # 从下到上：第1线=G2, 第2线=B2, 第3线=D3, 第4线=F3, 第5线=A3
    note_names = ['E2', 'F2', 'G2', 'A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4']
    note_positions = [
        line_y(0) + LINE_SPACING,     # E2 下加一线
        space_y(-1) + LINE_SPACING,   # F2 下加一间（第1线下方的间）
        line_y(0),                    # G2 第1线
        space_y(0),                   # A2 第1间
        line_y(1),                    # B2 第2线
        space_y(1),                   # C3 第2间
        line_y(2),                    # D3 第3线
        space_y(2),                   # E3 第3间
        line_y(3),                    # F3 第4线
        space_y(3),                   # G3 第4间
        line_y(4),                    # A3 第5线
        space_y(4),                   # B3 第5线上方的间
        line_y(4) - LINE_SPACING      # C4 上加一线
    ]
    score = 0
    current_note = random.randint(0, len(note_names)-1)
    running = True
    feedback = None
    feedback_time = 0
    fireworks = []  # 烟花列表
    last_firework_score = 0  # 上次触发烟花的分数
    # 不自动播放初始音符，等待用户交互
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
        font2 = pygame.font.Font(None, 32)
        text = font2.render(f"Score: {score} | Keys 1-7 = C~B | Current octave shown | Press SPACE to hear", True, BLACK)
        screen.blit(text, (40, 20))
        font3 = pygame.font.Font(None, 28)
        info = font3.render("C=1  D=2  E=3  F=4  G=5  A=6  B=7", True, BLUE)
        screen.blit(info, (40, 60))
        # 显示当前音符名称（用于调试）
        debug_font = pygame.font.Font(None, 24)
        debug_text = debug_font.render(f"Current: {note_names[current_note]}", True, (100, 100, 100))
        screen.blit(debug_text, (40, 90))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                # 按空格键播放当前音符
                if event.key == pygame.K_SPACE:
                    if note_names[current_note] in NOTE_SOUNDS:
                        NOTE_SOUNDS[note_names[current_note]].play()
                if pygame.K_1 <= event.key <= pygame.K_7:
                    guess = event.key - pygame.K_1  # 0=C, 1=D, 2=E, 3=F, 4=G, 5=A, 6=B
                    # 获取当前音符的字母名称（忽略八度）
                    current_note_name = note_names[current_note]
                    note_letter = current_note_name[0]  # 取第一个字符，如 'C3' -> 'C'
                    
                    # 将字母转换为数字 (C=0, D=1, E=2, F=3, G=4, A=5, B=6)
                    note_to_num = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}
                    correct = note_to_num.get(note_letter, -1)
                    
                    if guess == correct:
                        score += 1
                        feedback = font2.render("Correct!", True, (0,180,0))
                        feedback_time = pygame.time.get_ticks()
                        # 答对后播放当前音符（反馈音）
                        if note_names[current_note] in NOTE_SOUNDS:
                            NOTE_SOUNDS[note_names[current_note]].play()
                        current_note = random.randint(0, len(note_names)-1)
                        # 每得10分触发烟花
                        if score % 10 == 0 and score > last_firework_score:
                            for _ in range(3):  # 同时发射3个烟花
                                fw_x = random.randint(200, WIDTH - 200)
                                fw_y = random.randint(150, 350)
                                fireworks.append(Firework(fw_x, fw_y))
                            last_firework_score = score
                    else:
                        # 答错后播放正确的音符（让用户听到正确答案）
                        if note_names[current_note] in NOTE_SOUNDS:
                            NOTE_SOUNDS[note_names[current_note]].play()
                        feedback = font2.render(f"Wrong! {note_names[current_note]}", True, RED)
                        feedback_time = pygame.time.get_ticks()
        if feedback and pygame.time.get_ticks() - feedback_time < 1000:
            feedback_rect = feedback.get_rect(center=(WIDTH // 2, HEIGHT - 40))
            screen.blit(feedback, feedback_rect)
        # 更新和绘制烟花
        for firework in fireworks:
            firework.update()
            firework.draw(screen)
        fireworks = [fw for fw in fireworks if not fw.is_finished()]
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
