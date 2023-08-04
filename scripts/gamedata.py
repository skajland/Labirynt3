import block
from enemy import Enemy
from player import Player
import pygame


items_dict = {0: None,
              1: block.Block(pygame.transform.scale(pygame.image.load("res/blocks/grass.png"), (86, 86)), True, 1),
              2: Enemy((72, 92), 2),
              3: Player(),
              4: block.Key(pygame.transform.scale(pygame.image.load("res/blocks/key.png"), (86, 86)), True, 2, 'Green'),
              5: block.EntranceBlock(pygame.transform.scale(pygame.image.load("res/blocks/entrance.png"), (86, 86)), False, 3, 'Green'),
              6: block.EntranceBlock(pygame.transform.scale(pygame.image.load("res/blocks/entrance.png"), (86, 86)), False, 3, 'None'),
              7: block.WinBlock(pygame.transform.scale(pygame.image.load("res/blocks/WinBlock.png"), (86, 86)), True, 1),
              8: block.WaterBlock(pygame.transform.scale(pygame.image.load("res/blocks/WaterBlock.png"), (86, 86)), False, 2, 'Oak Log',
                                  pygame.transform.scale(pygame.image.load("res/blocks/WaterBlockOakLog.png"), (86, 86))),
              9: block.Key(pygame.transform.scale(pygame.image.load("res/blocks/OakLog.png"), (86, 86)), True, 2, 'Oak Log'),
              10: block.Block(pygame.transform.scale(pygame.image.load("res/blocks/sand.png"), (86, 86)), True, 1)}

levels = ('res/maps/map1/map', 'res/maps/map2/map', 'res/maps/map3/map', 'res/maps/map4/map', 'res/maps/map5/map', 'res/maps/MyLevel/level')
levels_data = ('res/maps/map1/map_data', 'res/maps/map2/map_data', 'res/maps/map3/map_data', 'res/maps/map4/map_data', 'res/maps/map5/map_data' , 'res/maps/MyLevel/gamedata')
current_level = 0
