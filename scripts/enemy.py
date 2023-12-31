import math

import camera
import pygame
import leveloader
import block
import usefull


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
            leveloader.game_state = "DeathScreen"

    def update(self, _, player):
        self.collision(player)
        self.point_at_player(leveloader.player)
        self.move_to_player(self.calculate_angle(player))
        self.rect.topleft = (round(self.enemy_pos.x - self.image_rot.get_width() / 2 + camera.offset.x),
                             round(self.enemy_pos.y - self.image_rot.get_height() / 2 + camera.offset.y))

    def render(self, screen):
        rot_rect = self.image_rot.get_rect()
        rot_rect.topleft = self.rect.topleft
        screen.blit(self.image_rot, self.rect)

    def start(self, _):
        if self.enemy_pos is None:
            self.enemy_pos = pygame.Vector2(self.pos[0] * 86, self.pos[1] * 86)
        self.rect.topleft = (round(self.enemy_pos.x - self.image_rot.get_width() / 2 + camera.offset.x),
                             round(self.enemy_pos.y - self.image_rot.get_height() / 2 + camera.offset.y))
        self.point_at_player(leveloader.player)


class Boss(Enemy):
    def __init__(self, img, speed):
        super().__init__(img, speed)
        self.time = 0
        self.all_debris = []

    def update(self, _, player):
        super().update(_, player)
        self.shoot_at_player()
        camera_size = camera.screen_size[0] / 2, camera.screen_size[1] / 2
        for debris in self.all_debris:
            debris.update(_, player)
            if debris.time_till_spawn > 8 and camera.rect_checker(debris.rect, debris.image_rot.get_size() + camera_size):
                self.all_debris.remove(debris)

    def render(self, screen):
        for debris in self.all_debris:
            debris.render(screen)
        super().render(screen)

    def shoot_at_player(self):
        if leveloader.difficulty_multiplier[leveloader.current_difficulty] == 0:
            return
        self.time += 0.05
        current_difficulty = leveloader.difficulty_multiplier[leveloader.current_difficulty]
        if self.time >= 10 - (current_difficulty + 1) * 4:
            rot_rect = self.image_rot.get_rect()
            rot_rect.topleft = self.rect.topleft
            usefull.turret_shoot_sound.play()
            self.all_debris.append(block.Debris((pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/Table.png"), (96, 96)),
                                                 pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/Toilet.png"), (96, 96)),
                                                 pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/Knife.png"), (96, 96))), True, 2, self.angle,
                                                pygame.Vector2(rot_rect.centerx, rot_rect.centery) - camera.offset.copy()).copy())
            self.time = 0

    def copy(self):
        return Boss(self.image, self.speed)
