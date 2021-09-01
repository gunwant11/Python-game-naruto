import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1440, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("naruto vs sasuke!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (180, 10, 255)
BLUE = (75,75, 255)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 15
MAX_BULLETS = 10
PLAYER_WIDTH, PLAYER_HEIGHT = 120, 100

RASENGAN_HIT = pygame.USEREVENT + 1
CHIDORI_HIT = pygame.USEREVENT + 2

NARUTO_IMAGE = pygame.image.load(
    os.path.join('Assets', 'naruto2.png'))
NARUTO = pygame.transform.rotate(pygame.transform.scale(
    NARUTO_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)),0)

SASUKE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'sasuke2.png'))
SASUKE = pygame.transform.rotate(pygame.transform.scale(
    SASUKE_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)),0)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'bg.jpg')), (WIDTH, HEIGHT))


def draw_window(purple, blue, chidori, rasengan, Sasuke_health, Naruto_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    sasuke_health_text = HEALTH_FONT.render(
        "Health: " + str(Sasuke_health), 1, WHITE)
    naruto_health_text = HEALTH_FONT.render(
        "Health: " + str(Naruto_health), 1, WHITE)
    WIN.blit(sasuke_health_text, (WIDTH - sasuke_health_text.get_width() - 10, 10))
    WIN.blit(naruto_health_text, (10, 10))

    WIN.blit(NARUTO, (blue.x, blue.y))
    WIN.blit(SASUKE, (purple.x, purple.y))

    for bullet in chidori:
        pygame.draw.rect(WIN, PURPLE, bullet)

    for bullet in rasengan:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.display.update()


def Naruto_Movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0:  # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x:  # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0:  # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT - 15:  # DOWN
        blue.y += VEL


def Sasuke_Movement(keys_pressed, purple):
    if keys_pressed[pygame.K_LEFT] and purple.x - VEL > BORDER.x + BORDER.width:  # LEFT
        purple.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and purple.x + VEL + purple.width < WIDTH:  # RIGHT
        purple.x += VEL
    if keys_pressed[pygame.K_UP] and purple.y - VEL > 0:  # UP
        purple.y -= VEL
    if keys_pressed[pygame.K_DOWN] and purple.y + VEL + purple.height < HEIGHT - 15:  # DOWN
        purple.y += VEL


def handle_bullets(rasengan, chidori, blue, purple):
    for bullet in rasengan:
        bullet.x += BULLET_VEL
        if purple.colliderect(bullet):
            pygame.event.post(pygame.event.Event(CHIDORI_HIT))
            rasengan.remove(bullet)
        elif bullet.x > WIDTH:
            rasengan.remove(bullet)

    for bullet in chidori:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RASENGAN_HIT))
            chidori.remove(bullet)
        elif bullet.x < 0:
            chidori.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    purple = pygame.Rect(700, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    blue = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)

    chidori = []
    rasengan = []

    Sasuke_health = 20
    Naruto_health = 20

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(rasengan) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        blue.x + blue.width, blue.y + blue.height//3 - 3, 15, 10)
                    rasengan.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(chidori) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        purple.x, purple.y + purple.height//3 - 3, 15, 10)
                    chidori.append(bullet)
                    #BULLET_FIRE_SOUND.play()

            if event.type == CHIDORI_HIT:
                Sasuke_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == RASENGAN_HIT:
                Naruto_health -= 1
                #BULLET_HIT_SOUND.play()

        winner_text = ""
        if Sasuke_health <= 0:
            winner_text = "NARUTO Wins!"

        if Naruto_health <= 0:
            winner_text = "SASUKE Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        Naruto_Movement(keys_pressed, blue)
        Sasuke_Movement(keys_pressed, purple)

        handle_bullets(rasengan, chidori, blue, purple)

        draw_window(purple, blue, chidori, rasengan,
                    Sasuke_health, Naruto_health)

    main()


if __name__ == "__main__":
    main()
