import math

import camera
import pygame
import leveloader
import gamestate


class Enemy:

    def __init__(self, img, speed):
        self.image = img
        self.image_rot = self.image.copy()
        self.angle = 0.0
        self.rect = self.image.get_rect()
        self.speed = speed
        self.layer = 5
        self.pos = (0, 0)
        self.enemy_pos = None

    def point_at_player(self, player):
        self.angle = self.calculate_angle(player)
        self.image_rot = pygame.transform.rotate(self.image, -math.degrees(self.angle))

    def calculate_angle(self, player):
        dist_x = player.rect.centerx - self.enemy_pos.x - camera.offset.x
        dist_y = player.rect.centery - self.enemy_pos.y - camera.offset.y
        return math.atan2(dist_y, dist_x)

    def copy(self):
        return Enemy(self.image, self.speed)

    def move_to_player(self, angle):
        self.enemy_pos.x += math.cos(angle) * self.speed * leveloader.difficulty_multiplier[leveloader.current_difficulty]
        self.enemy_pos.y += math.sin(angle) * self.speed * leveloader.difficulty_multiplier[leveloader.current_difficulty]

    def collision(self, player):
        mask = pygame.mask.from_surface(self.image_rot)
        overlap_mask = player.mask.overlap_mask(mask, (self.rect.x - player.rect.x, self.rect.y - player.rect.y))
        if overlap_mask.count() > 0:
            gamestate.game_state = "DeathScreen"

    def update(self, _, player):
        self.move_to_player(self.calculate_angle(player))
        self.collision(player)

    def render(self, screen):
        self.point_at_player(leveloader.player)
        rot_rect = self.image_rot.get_rect()
        self.rect.topleft = (round(self.enemy_pos.x - self.image.get_width() / 2 - rot_rect.left + camera.offset.x),
                             round(self.enemy_pos.y - self.image.get_height() / 2 - rot_rect.top + camera.offset.y))
        screen.blit(self.image_rot, self.rect)

    def start(self, _):
        if self.enemy_pos is None:
            self.enemy_pos = pygame.Vector2(self.pos[0] * 86, self.pos[1] * 86)


class Boss(Enemy):
    def __init__(self, img, speed):
        super().__init__(img, speed)
        self.time = 0

    def update(self, _, player):
        super().update(_, player)
        self.shoot_at_player()

    def shoot_at_player(self):
        if leveloader.difficulty_multiplier[leveloader.current_difficulty] == 0:
            return
        self.time += 0.05
        if self.time >= 10 - leveloader.difficulty_multiplier[leveloader.current_difficulty] * 3:
            print("shoot")
            self.time = 0

    def copy(self):
        return Boss(self.image, self.speed)
