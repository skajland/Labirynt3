import block
import enemy
import usefull
from player import Player
import pygame
print(usefull.data_directory + "res/blocks/grass.png")
items_dict = {0: None,
              1: block.Block(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/grass.png"), (86, 86)), True, 1),
              2: enemy.Enemy(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/enemy.png"), (72, 92)), 3),
              3: Player(),
              4: block.Key(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/key.png"), (86, 86)), True, 2, 'Green'),
              5: block.EntranceBlock(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/entrance.png"), (86, 86)),
                                     False, 3, 'Green'),
              6: block.EntranceBlock(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/entrance.png"), (86, 86)),
                                     False, 3, 'None'),
              7: block.WinBlock(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/WinBlock.png"), (86, 86)), True,
                                1),
              8: block.WaterBlock(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/WaterBlock.png"), (86, 86)),
                                  False, 2, 'Oak Log',
                                  pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/WaterBlockOakLog.png"),
                                                         (86, 86))),
              9: block.Key(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/OakLog.png"), (86, 86)), True, 2,
                           'Oak Log'),
              10: block.Block(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/sand.png"), (86, 86)), True, 1),
              11: block.Coins(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/coins.png"), (86, 86)), True, 2, 0),
              12: block.Coins(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/coins.png"), (86, 86)), True, 2, 1),
              13: enemy.Boss(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/enemy.png"), (72, 92)), 2),
              14: block.Turret(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/TurretBase.png"), (86, 86)), False, 2,
                               pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/TurretGun.png"), (86, 86))),
              15: block.Lava(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/Lava.png"), (86, 86)), True, 1)}

original_levels = (usefull.data_directory + 'res/maps/map1/map', usefull.data_directory + 'res/maps/map2/map', usefull.data_directory + 'res/maps/map3/map')
original_data = (usefull.data_directory + 'res/maps/map1/map_data', usefull.data_directory + 'res/maps/map2/map_data', usefull.data_directory + 'res/maps/map3/map_data')

levels = []
levels_data = []
current_level = 0
