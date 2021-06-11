import pygame
import os
pygame.font.init()
pygame.mixer.init()

dirpath = os.path.dirname(__file__)
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game!!!")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED_COLOR = (255,0,0)
YELLOW_COLOR = (255,220,0)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(dirpath, 'Assets', 'Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(dirpath, 'Assets', 'Assets_Gun+Silencer.mp3'))

YELLOW_HIT_RED = pygame.USEREVENT + 1
RED_HIT_YELLOW = pygame.USEREVENT + 2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(dirpath, 'Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(dirpath, 'Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join(dirpath, 'Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    yellow_health_text = HEALTH_FONT.render("Yellow Health: " + str(yellow_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Red Health: " + str(red_health),1, WHITE)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_COLOR, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED_COLOR, bullet)
    pygame.display.update()

def yellow_movement(keys_pressed, yellow):
    if (keys_pressed[pygame.K_a]) and (yellow.x - VEL> 0):
        yellow.x -= VEL
    if (keys_pressed[pygame.K_d]) and ((yellow.x + VEL + yellow.width) < BORDER.x):
        yellow.x += VEL
    if (keys_pressed[pygame.K_w]) and ((yellow.y - VEL) > 0):
        yellow.y -= VEL
    if (keys_pressed[pygame.K_s]) and ((yellow.y + VEL + yellow.height) < HEIGHT):
        yellow.y += VEL

def red_movement(keys_pressed, red):
    if (keys_pressed[pygame.K_LEFT]) and ((red.x - VEL) > BORDER.x + BORDER.width):
        red.x -= VEL
    if (keys_pressed[pygame.K_RIGHT]) and ((red.x + VEL + red.width) < WIDTH):
        red.x += VEL
    if (keys_pressed[pygame.K_UP]) and ((red.y - VEL) > 0):
        red.y -= VEL
    if (keys_pressed[pygame.K_DOWN]) and ((red.y + VEL + red.height) < HEIGHT):
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT_RED))
            yellow_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT_YELLOW))
            red_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - (draw_text.get_width()//2), HEIGHT//2 - (draw_text.get_height()//2)))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    yellow = pygame.Rect(300, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(600, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets = []
    red_bullets = []
    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LCTRL) and (len(yellow_bullets) < MAX_BULLETS):
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if (event.key == pygame.K_RCTRL) and (len(red_bullets) < MAX_BULLETS):
                    bullet = pygame.Rect(red.x + 10, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT_RED:
                red_health -= 1

            if event.type == RED_HIT_YELLOW:
                yellow_health -= 1

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red Wins!!!"
        if red_health <= 0:
            winner_text = "Yellow Wins!!!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()

        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)
        
    pygame.quit()


if __name__ == "__main__":
    main()