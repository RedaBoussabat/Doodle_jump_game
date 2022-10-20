import random
import pygame

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)

platforms = [[160, 650, 100, 10], [280, 600, 100, 10], [30, 450, 100, 10], [10, 400, 100, 10], [300, 350, 100, 10],
             [150, 200, 100, 10], [150, 100, 100, 10]]

# SCREEN DIMENSIONS
WIDTH = 600
HEIGHT = 700

player_x = 160
player_y = 350
score = 0
score_last = 0
high_score = 0
jump_last = 0
game_over = False
super_jumps = 2

# update player y position
jump = False
y_change = 0
x_change = 0
player_speed = 3

running = True
background = white

# PlAYER
player = pygame.transform.scale(pygame.image.load('view/img/grumpy_jumpy.png'), (70, 70))
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('view/font/OpenSans-Bold.ttf', 16)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Grumpy jumper")


###################
#### FUNCTIONS ####
###################

def update_player(y_pos):
    global jump
    global y_change
    jump_height = 10
    gravity = .4
    if jump:
        y_change = - jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos


# Check for platform collision on downwards trajectory
def check_collisions(rect_list, j):
    global player_x
    global player_y
    global y_change
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x, player_y + 60, 90, 25]) and jump == False and y_change > 0:
            j = True
    return j


def update_platforms(my_list, y_pos, change):
    global score
    if y_pos < 500 and y_change < 0:
        for i in range(len(my_list)):
            my_list[i][1] -= change
    else:
        pass
    for item in range(len(my_list)):
        if my_list[item][1] > 700:
            my_list[item] = [random.randint(0, 530), random.randint(-100, -10), 100, 10]
            score += 1
    return my_list


while running:
    timer.tick(fps)
    screen.fill(background)
    screen.blit(player, (player_x, player_y))
    blocks = []
    score_text = font.render('Score: ' + str(score), True, black, background)
    screen.blit(score_text, (520, 20))
    high_score_text = font.render('Highscore: ' + str(high_score), True, black, background)
    screen.blit(high_score_text, (485, 0))
    super_jumps_text = font.render('Super Jump [spacebar]: ' + str(super_jumps), True, black, background)
    screen.blit(super_jumps_text, (0, 0))
    if game_over:
        game_over_text = font.render("Game over, press spacebar to restart", True, black, background)
        screen.blit(game_over_text, (180, 350))

    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, black, platforms[i], 0, 5)
        blocks.append(block)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    game_over = False
                    score = 0
                    score_last = 0
                    background = white
                    super_jumps = 2
                    jump_last = 0
                    player_x = 160
                    player_y = 350
                    platforms = [[160, 650, 100, 10], [280, 600, 100, 10], [30, 450, 100, 10], [10, 400, 100, 10],
                                 [300, 350, 100, 10],
                                 [150, 200, 100, 10], [150, 100, 100, 10]]
                else:
                    if super_jumps > 0:
                        super_jumps -= 1
                        y_change = -15

            if event.key == pygame.K_a:
                x_change = - player_speed
            if event.key == pygame.K_d:
                x_change = player_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                x_change = 0

    jump = check_collisions(blocks, jump)
    player_x += x_change

    if player_y < 630:
        player_y = update_player(player_y)
    else:
        game_over = True
        y_change = 0

    platforms = update_platforms(platforms, player_y, y_change)

    if player_x < -20:
        player_x = -20
    elif player_x > 630:
        player_x = 630

    if x_change < 0:
        player = pygame.transform.scale(pygame.image.load('view/img/grumpy_jumpy.png'), (70, 70))
    elif x_change > 0:
        player = pygame.transform.flip(pygame.transform.scale(pygame.image.load('view/img/grumpy_jumpy.png'), (70, 70)),
                                       True, False)

    if score > high_score:
        high_score = score

    if score - score_last > 15:
        score_last = score
        background = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    if score - jump_last > 25:
        jump_last = score
        super_jumps += 1

    pygame.display.flip()
pygame.quit()
