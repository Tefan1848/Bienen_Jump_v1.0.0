#Als erstes importieren wir die Bibilotheken 
import pygame
import random

#Initialisieren von Pygame
pygame.init()

#Erzeugen der Klasse Setting
class Setting():
    window_WIDTH = 400
    window_HEIGHT = 500
    window = pygame.display.set_mode([window_WIDTH, window_HEIGHT])
    pygame.display.set_caption("Bienen Jump")
    player = pygame.transform.scale(pygame.image.load("Bienen_Jump.png"), (90, 70))
    fps = 60
    timer = pygame.time.Clock()
    score = 0
    high_score = 0
    game_over = False
    
#Erzeugen der Klasse Farben 
class Farben:
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (128, 128, 128)
    blue = (0, 0, 255)


Text = pygame.font.Font("freesansbold.ttf", 16)


#Hier sind die Spielvariablen zu finden
player_x = 170
player_y = 400
platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10], [85, 150, 70, 10], [265, 150, 70, 10], [175, 40, 70, 10]]
jump = False
y_change = 0
x_change = 0
player_speed = 3
score_last = 0
super_jumps = 2
jump_last = 0

#Tasten
A_KEY = pygame.K_a
D_KEY = pygame.K_d


#create screen
screen = pygame.display.set_mode([Setting.window_WIDTH, Setting.window_HEIGHT])


#Überprüfen auf Kollisionen mit Blöcken
def check_collisions(rect_list, j):
    global player_x
    global player_y
    global y_change
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x + 20, player_y + 60, 35, 5]) and jump == False and y_change > 0: #Kurz gleich vor der null gehabt
            j = True
    return j


#Hauptprogrammschleife
def update_player(y_pos):
    global jump
    global y_change
    jump_height = 10
    gravity = .4
    if jump:
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos



def update_platforms(my_list, y_pos, change):
    global score
    if y_pos < 250 and y_change < 0:
        for i in range(len(my_list)):
            for i in range(len(my_list)):
                 my_list[i][1] -= y_change
    else:
        pass
    for item in range(len(my_list)):
        if my_list[item][1] > 500:
            my_list[item] = [random.randint(0, 320), random.randint(-50, -10) ,70, 10]
            Setting.score += 1
    if Setting.score > Setting.high_score:
        Setting.high_score = Setting.score
    return my_list



running = True
while running == True:
    Setting.timer.tick(Setting.fps)
    screen.fill(Farben.white)
    screen.blit(Setting.player, (player_x, player_y))
    blocks = []
    score_text =Text.render('High Score:' + str(Setting.high_score), True, Farben.black, Farben.white)
    screen.blit(score_text, (260, 0))
    high_score_text = Text.render('Score:' + str(Setting.score), True, Farben.black, Farben.white)
    screen.blit(high_score_text, (300, 20))

    score_text =Text.render('Air Jumps (Spacebar):' + str(super_jumps), True, Farben.black, Farben.white)
    screen.blit(score_text, (10, 10))
    if Setting.game_over:
        game_over_text = Text.render('Game Over: Spacebar to restart', True, Farben.black, Farben.white)
        screen.blit(game_over_text, (80, 80))

    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, Farben.black, platforms[i], 0, 3)
        blocks.append(block)


    player_x += x_change
    if player_x < -90:
        player_x = Setting.window_WIDTH
    elif player_x > Setting.window_WIDTH:
        player_x = -90


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and Setting.game_over:
                Setting.game_over = False
                Setting.score = 0
                player_x = 170
                player_y = 400
                background = Farben.white
                score_last = 0
                super_jumps = 3  #Hier muss eine drei stehen, da sonst sobald man über SPACE restartet zu wenige super_jumps hätte.
                jump_last = 0
                platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10],
                             [85, 150, 70, 10], [265, 150, 70, 10], [175, 40, 70, 10]]
            if event.key == pygame.K_SPACE and not Setting.game_over and super_jumps > 0:
                super_jumps -= 1
                y_change = -15
            if event.key == A_KEY:
                x_change = -player_speed
            if event.key == D_KEY:
                x_change = player_speed
        if event.type == pygame.KEYUP:
            if event.key == A_KEY or event.key == D_KEY:
                x_change = 0

    player_y = update_player(player_y)
    platforms = update_platforms(platforms, player_y, y_change)

    jump = check_collisions(blocks, jump)
    if player_y > Setting.window_HEIGHT:
        Setting.game_over = True

    if Setting.score > Setting.high_score:
        Setting.high_score = Setting.score

#Funktion für Zusaätzliche super_jumps
    if Setting.score - jump_last > 100:
        jump_last = Setting.score
        super_jumps += 1

    pygame.display.update()

pygame.quit()



