import math
import random

import gamestate

import pygame

import camera
import leveloader


class Block:
    def __init__(self, img, walkable, layer):
        self.img = img
        self.rect = self.img.get_rect()
        self.walkable = walkable
        self.layer = layer
        self.pos = (0, 0)
        self.was_on_item = False

    def update(self, level_maps, player):
        self.rect.topleft = (self.pos[0] * 86, self.pos[1] * 86) + camera.offset

    def copy(self):
        new_block = Block(self.img, self.walkable, self.layer)
        return new_block

    def render(self, screen):
        screen.blit(self.img, self.rect)

    def start(self, _):
        pass


class WinBlock(Block):

    def update(self, level_maps, player):
        super().update(level_maps, player)
        if self.was_on_item:
            leveloader.load_map()

    def copy(self):
        new_block = WinBlock(self.img, self.walkable, self.layer)
        return new_block


class EntranceBlock(Block):
    def __init__(self, img, walkable, layer, keycode):
        super().__init__(img, walkable, layer)
        self.key_keycode = keycode

    def update(self, level_maps, player):
        super().update(level_maps, player)
        level_keys = []
        for level_items in level_maps[2]:
            if type(level_items) == Key:
                level_keys.append(level_items)
        for level_key in level_keys:
            if level_key.key == self.key_keycode:
                self.was_on_item = False
                return
        if self.was_on_item:
            level_maps[2].remove(self)
            level_maps[1].remove(self)
            return

    def copy(self):
        new_block = EntranceBlock(self.img, self.walkable, self.layer, self.key_keycode)
        return new_block


class WaterBlock(Block):

    def __init__(self, img, walkable, layer, keycode, second_img):
        super().__init__(img, walkable, layer)
        self.keycode = keycode
        self.second_img = second_img
        self.all_items = 0

    def update(self, level_maps, player):
        super().update(level_maps, player)
        current_items = 0
        for level_items in level_maps[2]:
            if type(level_items) == Key:
                if level_items.key == self.keycode:
                    current_items += 1
        block_items = 0
        for level_items in level_maps[2]:
            if type(level_items) == WaterBlock:
                if not level_items.keycode == self.keycode:
                    return
                if level_items.second_img == level_items.img:
                    block_items += 1
        items_left = self.all_items - current_items - block_items
        if items_left <= 0:
            self.was_on_item = False
            return
        if self.was_on_item:
            self.img = self.second_img
            self.walkable = True

    def start(self, opt_lvl_map):
        for level_items in opt_lvl_map:
            if type(level_items) == Key:
                if level_items.key == self.keycode:
                    self.all_items += 1

    def copy(self):
        new_block = WaterBlock(self.img, self.walkable, self.layer, self.keycode, self.second_img)
        return new_block


class Key(Block):
    def __init__(self, img, walkable, layer, key):
        super().__init__(img, walkable, layer)
        self.key = key
        self.destroying = False

    def update(self, level_maps, player):
        if self.was_on_item and not self.destroying:
            leveloader.destroy.append(self)
            self.destroying = True
            return
        super().update(level_maps, player)

    def copy(self):
        new_block = Key(self.img, self.walkable, self.layer, self.key)
        return new_block


class Coins(Block):
    def __init__(self, img, walkable, layer, data_index):
        self.data_index = data_index
        if leveloader.Data.data[data_index] == "True":
            return
        super().__init__(img, walkable, layer)

    def update(self, level_maps, player):
        super().update(self, player)
        if self.was_on_item:
            level_maps[2].remove(self)
            level_maps[1].remove(self)
            leveloader.Data.write_data(self.data_index, "True")
            return

    def render(self, screen):
        super().render(screen)

    def copy(self):
        if leveloader.Data.data[self.data_index] == "True":
            return
        return Coins(self.img, self.walkable, self.layer, self.data_index)


class Debris(Block):
    def __init__(self, images, walkable, layer, angle, pos, img_rotation=None):
        img_index = random.randint(0, len(images)) - 1
        super().__init__(images[img_index], walkable, layer)
        self.angle = angle
        self.speed = 6
        self.debris_offset = pygame.Vector2()
        self.enemy_pos = pos
        self.time_till_spawn = 0
        self.img_rotation = img_rotation
        if img_rotation is not None:
            self.image_rot = pygame.transform.rotate(self.img, img_rotation)
            return
        self.image_rot = pygame.transform.rotate(self.img, math.degrees(random.randint(0, 180)))

    def update(self, level_maps, player):
        self.collision(player)
        self.time_till_spawn += 0.05
        self.rect.topleft = (
            round(self.enemy_pos.x - self.image_rot.get_width() / 2 + camera.offset.x + self.debris_offset.x),
            round(self.enemy_pos.y - self.image_rot.get_height() / 2 + camera.offset.y + self.debris_offset.y))
        self.move_debris()

    def render(self, screen):
        screen.blit(self.image_rot, self.rect)

    def collision(self, player):
        mask = pygame.mask.from_surface(self.image_rot)
        overlap_mask = player.mask.overlap_mask(mask, (self.rect.x - player.rect.x, self.rect.y - player.rect.y))
        if overlap_mask.count() > 0:
            gamestate.game_state = "DeathScreen"

    def copy(self):
        return Debris([self.img], self.walkable, self.layer, self.angle, self.enemy_pos, self.img_rotation)

    def move_debris(self):
        self.debris_offset.x += math.cos(self.angle) * self.speed
        self.debris_offset.y += math.sin(self.angle) * self.speed


class Turret(Block):

    def __init__(self, img, walkable, layer, second_img):
        super().__init__(img, walkable, layer)
        self.gun_img = second_img
        self.gun_img_rot = self.gun_img.copy()
        self.time = 0
        self.angle = 0
        self.rot_rect = self.gun_img_rot.get_rect()
        self.all_debris = []

    def update(self, level_maps, player):
        super().update(level_maps, player)
        self.update_turret_pos(player)
        self.shoot_at_player()
        camera_size = camera.screen_size[0] / 2, camera.screen_size[1] / 2
        for debris in self.all_debris:
            debris.update(level_maps, player)
            if debris.time_till_spawn > 10 and camera.rect_checker(debris.rect,
                                                                   debris.image_rot.get_size() + camera_size):
                self.all_debris.remove(debris)

    def update_turret_pos(self, player):
        self.point_at_player(player)
        offset_x = self.img.get_width() / 2 - self.gun_img_rot.get_width() / 2 + camera.offset.x
        offset_y = self.img.get_height() / 2 - self.gun_img_rot.get_height() / 2 + camera.offset.y
        self.rot_rect = pygame.Rect(self.pos[0] * 86 + offset_x, self.pos[1] * 86 + offset_y,
                                    self.gun_img_rot.get_width(), self.gun_img_rot.get_height())

    def shoot_at_player(self):
        if leveloader.difficulty_multiplier[leveloader.current_difficulty] == 0:
            return
        self.time += 0.05
        current_difficulty = leveloader.difficulty_multiplier[leveloader.current_difficulty]
        if self.time >= 10 - (current_difficulty + 1) * 4:
            rot_rect = self.gun_img_rot.get_rect()
            rot_rect.topleft = self.rect.topleft
            self.all_debris.append(
                Debris((pygame.transform.scale(pygame.image.load("res/blocks/bullet.png"), (64, 64)),), True, 2,
                       self.angle,
                       pygame.Vector2(self.rect.centerx, self.rect.centery) - camera.offset.copy(), -math.degrees(self.angle)).copy())
            self.time = 0

    def render(self, screen):
        for debris in self.all_debris:
            debris.render(screen)
        super().render(screen)
        screen.blit(self.gun_img_rot, self.rot_rect)

    def copy(self):
        return Turret(self.img, self.walkable, self.layer, self.gun_img)

    def point_at_player(self, player):
        angle = self.calculate_angle(player)
        self.angle = angle
        self.gun_img_rot = pygame.transform.rotate(self.gun_img, -math.degrees(angle))

    def calculate_angle(self, player):
        dist_x = player.rect.x - self.pos[0] * 86 - camera.offset.x
        dist_y = player.rect.y - self.pos[1] * 86 - camera.offset.y
        return math.atan2(dist_y, dist_x)
