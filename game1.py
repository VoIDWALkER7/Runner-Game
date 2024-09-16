# modules
from tkinter import CENTER
import pygame
from random import randint, choice
from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player1 = pygame.image.load("Graphics/player/player1.png").convert_alpha()
        player2 = pygame.image.load("Graphics/player/player2.png").convert_alpha()
        player3 = pygame.image.load("Graphics/player/player3.png").convert_alpha()
        player4 = pygame.image.load("Graphics/player/player4.png").convert_alpha()
        self.player_list = [player1, player2, player3, player4]
        self.player_index = 0
        self.player_jump1 = pygame.image.load(
            "Graphics/player/player5.png"
        ).convert_alpha()
        self.player_jump1 = pygame.transform.rotozoom(self.player_jump1, 0, 1.4)

        self.image = self.player_list[self.player_index]
        self.rect = self.image.get_rect(midbottom=(75, 475))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 475:
            self.gravity = -27
            jmp_msc.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 475:
            self.rect.bottom = 475

    def anime_pl(self):
        if self.rect.bottom < 475:
            self.image = self.player_jump1
        else:
            self.player_index += 0.175
            if self.player_index >= len(self.player_list):
                self.player_index = 0
            self.image = self.player_list[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.anime_pl()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly_obj":
            fly_obj = pygame.image.load("Graphics/ghosty/ghost4.png").convert_alpha()
            fly_obj = pygame.transform.rotozoom(fly_obj, 0, 1.5)
            objii = fly_obj
            y_pos = 300
        else:
            obj = pygame.image.load("Graphics/ghosty/ghost1.png").convert_alpha()
            obj = pygame.transform.rotozoom(obj, 0, 2)
            objii = obj
            y_pos = 475
        self.animationindex = 0
        self.image = objii
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def update(self):
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current = int(pygame.time.get_ticks() / 100) - start_time
    score_surface = test_font.render(f"Score: {current}", 10, False, "#4d4d4d")
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return current


def obstacle_movement(list):
    if list:
        for obstacle_rect in list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 500:
                screen.blit(fly_obj, obstacle_rect)
            else:
                screen.blit(obj, obstacle_rect)
        list = [obstacle for obstacle in list if obstacle.x > -100]
        return list
    else:
        return []


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# pygame initilasing
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("VOIDWALKER'S HELL")
clock = pygame.time.Clock()
test_font = pygame.font.Font("Fonts/alagard.ttf", 35)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load("Graphics/Sky.jpg").convert()
ground_surface = pygame.image.load("Graphics/Ground.png").convert()

# obstacles
ghost = pygame.image.load("Graphics/ghosty/ghost4.png").convert_alpha()

ghost2 = pygame.image.load("Graphics/ghosty/ghost1.png").convert_alpha()


player_surf = pygame.image.load("Graphics/player/player1.png").convert_alpha()
player_rectangle = player_surf.get_rect(midbottom=(75, 475))
player_gravity = 0
# intro screen
title_page = pygame.image.load("VOIDWALKER_S .jpg").convert_alpha()
player_dead = pygame.image.load("Graphics/player/player5.png").convert_alpha()
player_dead = pygame.transform.rotozoom(player_dead, 0, 1.5)
player_dead_rectangle = player_dead.get_rect(center=(400, 480))
game_message = test_font.render("Press Space to Enter", False, "#AAABAB")
game_message_rectangle = game_message.get_rect(center=(400, 575))
icon = pygame.image.load("Graphics/ghosty/ghost.png")
pygame.display.set_icon(icon)

# Player
player = pygame.sprite.GroupSingle()
player.add(Player())
bg_music = pygame.mixer.Sound("DARKNESS.mp3")
bg_music.play(loops=-1)
jmp_msc = pygame.mixer.Sound("stingers-001.mp3")
# player_jump=pygame.transform.rotozoom(player_jump,0,1.4)
# score
# score_surf=test_font.render("SCORE",False,(0,0,0))
# score_rect=score_surf.get_rect(center=(400,50))

# obstacles
obstacle_group = pygame.sprite.Group()

# Clock
clock = pygame.time.Clock()

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer and game_active:
                obstacle_group.add(Obstacle(choice(["fly_obj", "obj", "obj", "obj"])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 100)

            # if randint(0,2):
            #    obstacle_rect_list.append(obj.get_rect(bottomright=(randint(900,1100),620)))
            # else:
            #    obstacle_rect_list.append(obj.get_rect(bottomright=(randint(900,1100),500)))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 475))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision
        game_active = collision_sprite()

    else:
        screen.blit(title_page, (0, 0))
        player_rectangle.midbottom = (75, 475)
        player_gravity = 0

        score_message = test_font.render(f"Your score:{score}", False, "#AAABAB")
        score_message_rectangle = score_message.get_rect(center=(400, 400))
        screen.blit(game_message, game_message_rectangle)
        if score != 0:
            screen.blit(player_dead, player_dead_rectangle)
            screen.blit(score_message, score_message_rectangle)
    pygame.display.update()
    clock.tick(60)
