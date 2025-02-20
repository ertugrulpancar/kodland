import pgzrun
from pygame import Rect
import random

# Ekran boyutları
WIDTH = 800
HEIGHT = 600
TITLE = "Platform Adventure"

# Oyun durumları
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Ses ayarları
sound_on = True


# Oyuncu sınıfı
class Player:
    def __init__(self):
        self.rect = Rect(50, HEIGHT - 100, 64, 64)
        self.velocity_y = 0
        self.jumping = False
        self.frame = 0
        self.animation_timer = 0
        self.facing_right = True
        self.alive = True
        self.state = "Idle"

    def update(self):
        # Yerçekimi
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        # Zemin kontrolü
        if self.rect.bottom > HEIGHT - 20:
            self.rect.bottom = HEIGHT - 20
            self.velocity_y = 0
            self.jumping = False

        # Animasyon güncelleme
        self.animation_timer += 1
        if self.animation_timer >= 8:
            self.frame = (self.frame + 1) % 6
            self.animation_timer = 0

    def jump(self):
        if not self.jumping:
            self.velocity_y = -12
            self.jumping = True


# Düşman sınıfı
class Enemy:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 48, 48)
        self.direction = 1
        self.frame = 0
        self.animation_timer = 0
        self.patrol_start = x
        self.patrol_end = x + 200
        self.state = "move"
        self.health = 100

    def update(self):
        self.rect.x += 2 * self.direction

        if self.rect.x >= self.patrol_end:
            self.direction = -1
        elif self.rect.x <= self.patrol_start:
            self.direction = 1

        if self.health <= 0:
            self.state = "death"
        elif self.health < 50:
            self.state = "damaged"
        else:
            self.state = "move"


# Oyun nesneleri
player = Player()
enemies = [
    Enemy(300, HEIGHT - 100),
    Enemy(500, HEIGHT - 100)
]

# Menü düğmeleri
start_button = Rect(WIDTH // 2 - 100, 200, 200, 50)
sound_button = Rect(WIDTH // 2 - 100, 300, 200, 50)
exit_button = Rect(WIDTH // 2 - 100, 400, 200, 50)


def update():
    global game_state, sound_on

    if game_state == PLAYING:
        player.update()

        # Klavye kontrolleri
        if keyboard.left:
            player.rect.x -= 5
            player.facing_right = False
        if keyboard.right:
            player.rect.x += 5
            player.facing_right = True
        if keyboard.up or keyboard.space:  # Space veya Up tuşu ile zıplama
            player.jump()

        for enemy in enemies:
            enemy.update()
            if player.rect.colliderect(enemy.rect):
                game_state = GAME_OVER

    # GAME OVER ekranında space tuşu kontrolü
    elif game_state == GAME_OVER:
        if keyboard.space:
            game_state = MENU
            # Oyuncuyu başlangıç pozisyonuna resetle
            player.rect.x = 50
            player.rect.y = HEIGHT - 100
            player.velocity_y = 0
            player.jumping = False


def draw():
    screen.clear()

    if game_state == MENU:
        screen.fill((100, 150, 200))
        screen.draw.filled_rect(start_button, (200, 200, 200))
        screen.draw.filled_rect(sound_button, (200, 200, 200))
        screen.draw.filled_rect(exit_button, (200, 200, 200))

        screen.draw.text("Start Game", center=(WIDTH // 2, 225), fontsize=32)
        screen.draw.text(f"Sound: {'On' if sound_on else 'Off'}",
                         center=(WIDTH // 2, 325), fontsize=32)
        screen.draw.text("Exit", center=(WIDTH // 2, 425), fontsize=32)

    elif game_state == PLAYING:
        screen.fill((200, 200, 255))

        # Oyuncu çizimi - basit dikdörtgen
        screen.draw.filled_rect(player.rect, (255, 0, 0))

        # Düşman çizimi - basit dikdörtgen
        for enemy in enemies:
            screen.draw.filled_rect(enemy.rect, (0, 0, 255))

    elif game_state == GAME_OVER:
        screen.fill((150, 0, 0))
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=64)
        screen.draw.text("Press SPACE to return to menu",
                         center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=32)


def on_mouse_down(pos):
    global game_state, sound_on

    if game_state == MENU:
        if start_button.collidepoint(pos):
            game_state = PLAYING
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
        elif exit_button.collidepoint(pos):
            quit()


pgzrun.go()