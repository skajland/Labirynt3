import pygame
import camera
import usefull
keys_pressed = []


class Player:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/Player.png"), (86, 86))
        self.rect = self.image.get_rect()
        self.layer = 3
        self.pos = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def movement(self, level_map):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and pygame.K_w not in keys_pressed:
            keys_pressed.append(pygame.K_w)
            if self.collision(level_map, pygame.math.Vector2(0, self.image.get_height())):
                self.rect.y += -self.image.get_height()
        elif not keys[pygame.K_w] and pygame.K_w in keys_pressed:
            keys_pressed.remove(pygame.K_w)

        if keys[pygame.K_s] and pygame.K_s not in keys_pressed:
            keys_pressed.append(pygame.K_s)
            if self.collision(level_map, pygame.math.Vector2(0, -self.image.get_height())):
                self.rect.y += self.image.get_height()
        elif not keys[pygame.K_s] and pygame.K_s in keys_pressed:
            keys_pressed.remove(pygame.K_s)

        if keys[pygame.K_a] and pygame.K_a not in keys_pressed:
            keys_pressed.append(pygame.K_a)
            if self.collision(level_map, pygame.math.Vector2(self.image.get_width(), 0)):
                self.rect.x += -self.image.get_width()
        elif not keys[pygame.K_a] and pygame.K_a in keys_pressed:
            keys_pressed.remove(pygame.K_a)

        if keys[pygame.K_d] and pygame.K_d not in keys_pressed:
            keys_pressed.append(pygame.K_d)
            if self.collision(level_map, pygame.math.Vector2(-self.image.get_width(), 0)):
                self.rect.x += self.image.get_width()
        elif not keys[pygame.K_d] and pygame.K_d in keys_pressed:
            keys_pressed.remove(pygame.K_d)

    def collision(self, level_map, point):
        collided = False
        level_map_not_walkable = [level_item for level_item in level_map if hasattr(level_item, 'walkable') if level_item.walkable is False]
        for level_item in level_map_not_walkable:
            if self.rect.collidepoint(level_item.rect.topleft + point):
                level_item.was_on_item = True
                collided = True

        if collided:
            return False

        for level_item in level_map:
            if hasattr(level_item, 'walkable') and level_item.walkable:
                if self.rect.collidepoint(level_item.rect.topleft + point):
                    level_item.was_on_item = True
                    collided = True
        if collided:
            return True
        return False

    def copy(self):
        new_enemy = Player()
        return new_enemy

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, level_maps, player):
        self.movement(level_maps[2])
        camera.box_camera(player.rect)

    def start(self, _):
        pass
