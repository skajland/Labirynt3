import math

import camera
import pygame

import gamestate


class Enemy:

    def __init__(self, scale, speed):
        self.image = pygame.transform.scale(pygame.image.load("res/enemy.png"), scale)
        self.image_rot = self.image.copy()
        self.angle = 0.0
        self.rect = self.image.get_rect()
        self.speed = speed
        self.layer = 5
        self.pos = (0, 0)
        self.enemy_pos = None

    def point_at_player(self, player):
        dist_x = player.rect.centerx - self.enemy_pos.x - camera.offset.x
        dist_y = player.rect.centery - self.enemy_pos.y - camera.offset.y
        self.angle = math.atan2(dist_y, dist_x)
        self.image_rot = pygame.transform.rotate(self.image, -math.degrees(self.angle))

    def copy(self):
        new_enemy = Enemy(self.image.get_size(), self.speed)
        return new_enemy

    def move_to_player(self):
        self.enemy_pos.x += math.cos(self.angle) * self.speed * gamestate.difficulty_multiplier
        self.enemy_pos.y += math.sin(self.angle) * self.speed * gamestate.difficulty_multiplier

    def collision(self, player):
        mask = pygame.mask.from_surface(self.image_rot)
        overlap_mask = player.mask.overlap_mask(mask, (self.rect.x - player.rect.x, self.rect.y - player.rect.y))
        if overlap_mask.count() > 0:
            gamestate.game_state = "DeathScreen"

    def update(self, _, player):
        self.point_at_player(player)
        self.move_to_player()
        self.collision(player)
        rot_rect = self.image_rot.get_rect()
        self.rect.topleft = (round(self.enemy_pos.x - self.image.get_width() / 2 - rot_rect.left + camera.offset.x), round(self.enemy_pos.y - self.image.get_height() / 2 - rot_rect.top + camera.offset.y))

    def render(self, screen):
        screen.blit(self.image_rot, self.rect)

    def start(self, _):
        if self.enemy_pos is None:
            self.enemy_pos = pygame.Vector2(self.pos[0] * 86, self.pos[1] * 86)
