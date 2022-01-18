
import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface,(floorx,450))
    screen.blit(floor_surface,(floorx + 288,450))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bot_pipe = pipe_surface.get_rect(midtop =(320,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom =(320,random_pipe_pos-175))
    return top_pipe,bot_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -30]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe) :
            death_sound.play()
            return False


    if bird_rect.top <= -100 or bird_rect.bottom >= 450:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_y * 2,1)
    return new_bird

def bird_anim():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), False,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface, score_rect)

    if game_state =='game_over':
        score_surface = game_font.render(f'Score: {int(score)}', False,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', False,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,410))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score

    return high_score


def pipe_score_check():
    global score

    if pipe_list:
        for pipe in pipe_list:
            if  45 < pipe.centerx < 55:
                score += 0.5
                score_sound.play()




#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()

screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
#game_font = pygame.font.Font('C:/Users/dhruv/OneDrive/Desktop/flappy-bird-assets-master/04B_19.TTF',20)



#Game Variables
gravity = 0.25
bird_y = 0
game_active = True
score = 0
high_score = 0


bg_surface = pygame.image.load('C:/Users/dhruv/OneDrive/Desktop/flappy-bird-assets-master/sprites/background-day.png').convert()

floor_surface = pygame.image.load('C:/Users/dhruv/OneDrive/Desktop/flappy-bird-assets-master/sprites/base.png').convert()
floorx = 0

bird_downflap = pygame.image.load('C:/Users/dhruv/OneDrive/Desktop/flappy-bird-assets-master/sprites/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('C:/Users/dhruv/OneDrive/Desktop/flappy-bird-assets-master/sprites/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('C:/Users/dhruv/OneDrive/Desktop/flappy-bird-assets-master/sprites/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50,225))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


pipe_surface = pygame.image.load('C:/Users/dhruv/OneDrive/Desktop/flappy-bird-assets-master/sprites/pipe-green.png')
pipe_list =[]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1300)
pipe_height = [200, 300, 400]


flap_sound = pygame.mixer.Sound('C:/Users/dhruv/OneDrive/Desktop/flappy-bird-assets-master/audio/wing.wav')
death_sound = pygame.mixer.Sound('C:/Users/dhruv/OneDrive/Desktop/flappy-bird-assets-master/audio/hit.wav')
score_sound = pygame.mixer.Sound('C:/Users/dhruv/OneDrive/Desktop/flappy-bird-assets-master/audio/point.wav')
score_sound_cd = 100

while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE :
                    bird_y = 0
                    bird_y -= 6
                    if game_active == True:
                        flap_sound.play()
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (50,256)
                    bird_movement = 0
                    score = 0
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_anim()

    screen.blit(bg_surface,(0,0))

    if game_active:
        #BIRD
        bird_y += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_y
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        #PIPES
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        pipe_score_check()
        score_display('main_game')

    else:
        high_score = update_score(score, high_score)
        score_display('game_over')



    #FLOOR
    floorx -= 1
    draw_floor()
    if floorx <= -288:
        floorx = 0


    pygame.display.update()
    clock.tick(75)
