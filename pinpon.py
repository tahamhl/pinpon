import pygame
import sys

# Pygame'i başlat
pygame.init()

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Top özellikleri
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Padel özellikleri
PADEL_WIDTH = 10
PADEL_HEIGHT = 100
PADEL_SPEED = 7

# Skor
WINNING_SCORE = 5

# Ekran oluştur
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pinpon Oyunu')

# Font ayarları
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

def reset_ball():
    return SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SPEED_X, BALL_SPEED_Y

def draw_score(player1_score, player2_score):
    player1_text = font.render(str(player1_score), True, WHITE)
    player2_text = font.render(str(player2_score), True, WHITE)
    screen.blit(player1_text, (SCREEN_WIDTH // 4, 10))
    screen.blit(player2_text, (3 * SCREEN_WIDTH // 4, 10))

def show_winner(winner):
    text = font.render(f"Tebrikler, {winner} kazandı!", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

def ask_replay():
    screen.fill(BLACK)
    text = small_font.render("Yeniden oynamak ister misiniz? (E: Evet, H: Hayır)", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    maker_text = small_font.render("Yapımcı: Mehmet Taha Mehel", True, WHITE)
    maker_rect = maker_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
    screen.blit(maker_text, maker_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return True
                if event.key == pygame.K_h:
                    return False

def show_instructions():
    screen.fill(BLACK)
    instructions = [
        "Pinpon Oyunu Kuralları:",
        "1. Oyuncu 1: W ve S tuşlarını kullanarak hareket eder.",
        ""
        "2. Oyuncu 2: Yukarı ve Aşağı ok tuşlarını kullanarak hareket eder.",
        "3. Bir oyuncu topu kaçırdığında, diğer oyuncu bir puan kazanır.",
        "4. İlk 5 puana ulaşan oyuncu oyunu kazanır.",
        "Başlamak için herhangi bir tuşa basın..."
    ]
    y_offset = 100
    for line in instructions:
        instruction_text = small_font.render(line, True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(instruction_text, instruction_rect)
        y_offset += 40

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def game_loop():
    player1_score = 0
    player2_score = 0
    ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
    player1_padel_y = (SCREEN_HEIGHT // 2) - (PADEL_HEIGHT // 2)
    player2_padel_y = (SCREEN_HEIGHT // 2) - (PADEL_HEIGHT // 2)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # Tuşlara basıldığında hareketi kontrol et
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player1_padel_y > 0:
                player1_padel_y -= PADEL_SPEED
            if keys[pygame.K_s] and player1_padel_y < SCREEN_HEIGHT - PADEL_HEIGHT:
                player1_padel_y += PADEL_SPEED
            if keys[pygame.K_UP] and player2_padel_y > 0:
                player2_padel_y -= PADEL_SPEED
            if keys[pygame.K_DOWN] and player2_padel_y < SCREEN_HEIGHT - PADEL_HEIGHT:
                player2_padel_y += PADEL_SPEED

            # Topu hareket ettir
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Topun kenarlara çarpmasını kontrol et
            if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - BALL_SIZE:
                ball_speed_y = -ball_speed_y

            # Sol kenardan çıkarsa
            if ball_x <= 0:
                player2_score += 1
                if player2_score >= WINNING_SCORE:
                    show_winner("Oyuncu 2")
                    game_over = True
                else:
                    ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()

            # Sağ kenardan çıkarsa
            if ball_x >= SCREEN_WIDTH - BALL_SIZE:
                player1_score += 1
                if player1_score >= WINNING_SCORE:
                    show_winner("Oyuncu 1")
                    game_over = True
                else:
                    ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()

            # Topun padellere çarpmasını kontrol et
            if (ball_x <= PADEL_WIDTH and player1_padel_y < ball_y < player1_padel_y + PADEL_HEIGHT) or \
               (ball_x >= SCREEN_WIDTH - PADEL_WIDTH - BALL_SIZE and player2_padel_y < ball_y < player2_padel_y + PADEL_HEIGHT):
                ball_speed_x = -ball_speed_x

            # Ekranı siyaha boyayın
            screen.fill(BLACK)

            # Topu çizin
            pygame.draw.rect(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

            # Padelleri çizin
            pygame.draw.rect(screen, WHITE, (0, player1_padel_y, PADEL_WIDTH, PADEL_HEIGHT))
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - PADEL_WIDTH, player2_padel_y, PADEL_WIDTH, PADEL_HEIGHT))

            # Skoru çizin
            draw_score(player1_score, player2_score)

        # Ekranı güncelle
        pygame.display.flip()

        # FPS ayarlaması
        pygame.time.Clock().tick(60)

        if game_over:
            if ask_replay():
                game_loop()
            else:
                pygame.quit()
                sys.exit()

# Oyunu başlatmadan önce bilgi ekranını göster
show_instructions()

# Oyunu başlat
game_loop()
