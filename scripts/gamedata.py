import block
import enemy
import usefull
from player import Player
import pygame
items_dict = {0: None,
              1: block.Block(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/grass.png"), (86, 86)), True, 1),
              2: enemy.Enemy(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/enemy.png"), (72, 92)), 3),
              3: Player(),
              4: block.Key(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/key.png"), (86, 86)), True, 2, 'Original'),
              5: block.EntranceBlock(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/entrance.png"), (86, 86)),
                                     False, 3, 'Original'),
              6: block.WinBlock(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/WinBlock.png"), (86, 86)), True,
                                1),
              7: block.WaterBlock(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/WaterBlock.png"), (86, 86)),
                                  False, 2, 'Oak Log',
                                  pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/WaterBlockOakLog.png"),
                                                         (86, 86))),
              8: block.Key(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/OakLog.png"), (86, 86)), True, 2,
                           'Oak Log'),
              9: block.Block(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/sand.png"), (86, 86)), True, 1),
              10: block.Coins(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/coins.png"), (86, 86)), True, 2, 0),
              11: block.Coins(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/coins.png"), (86, 86)), True, 2, 1),
              12: enemy.Boss(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/enemyBoss.png"), (104, 124)), 2),
              13: block.Turret(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/TurretBase.png"), (86, 86)), False, 2,
                               pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/TurretGun.png"), (86, 86))),
              14: block.Lava(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/Lava.png"), (86, 86)), True, 1),
              15: block.Key(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/Redkey.png"), (86, 86)), True, 2, 'Red'),
              16: block.Key(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/Greenkey.png"), (86, 86)), True, 2, 'Green'),
              17: block.Key(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/Bluekey.png"), (86, 86)), True, 2, 'Blue'),
              18: block.EntranceBlock(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/entranceRed.png"), (86, 86)), False, 2, 'Red'),
              19: block.EntranceBlock(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/entranceGreen.png"), (86, 86)), False, 2, 'Green'),
              20: block.EntranceBlock(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/entranceBlue.png"), (86, 86)), False, 2, 'Blue'),
              21: enemy.Enemy(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/enemyRound.png"), (72, 92)), 2.5),
              22: enemy.Enemy(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/enemyTriangle.png"), (86, 110)), 3.5),
              23: block.Block(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/netherack.png"), (86, 86)), True, 1),
              24: block.Coins(
                  pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/coins.png"), (86, 86)),
                  True, 2, 2),
              25: block.Coins(
                  pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/coins.png"), (86, 86)),
                  True, 2, 3),
              26: block.Coins(
                  pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/coins.png"), (86, 86)),
                  True, 2, 4),
              27: block.Coins(
                  pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/coins.png"), (86, 86)),
                  True, 2, 5),
              28: block.Coins(
                  pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/coins.png"), (86, 86)),
                  True, 2, 6),
              29: block.Coins(
                  pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/coins.png"), (86, 86)),
                  True, 2, 7),
              30: block.Block(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/blocks/stone.png"), (86, 86)), True, 1)
              }

original_levels = (usefull.data_directory + 'res/maps/map1/map', usefull.data_directory + 'res/maps/map2/map', usefull.data_directory + 'res/maps/map3/level', usefull.data_directory + 'res/maps/map4/level',
                   usefull.data_directory + 'res/maps/map5/level', usefull.data_directory + 'res/maps/map6/level', usefull.data_directory + 'res/maps/map7/level',
                   usefull.data_directory + 'res/maps/map8/level', usefull.data_directory + 'res/maps/map9/level', usefull.data_directory + 'res/maps/map10/level',)
original_data = (usefull.data_directory + 'res/maps/map1/map_data', usefull.data_directory + 'res/maps/map2/map_data', usefull.data_directory + 'res/maps/map3/leveldata', usefull.data_directory + 'res/maps/map4/leveldata',
                 usefull.data_directory + 'res/maps/map5/leveldata', usefull.data_directory + 'res/maps/map6/leveldata', usefull.data_directory + 'res/maps/map7/leveldata',
                 usefull.data_directory + 'res/maps/map8/leveldata', usefull.data_directory + 'res/maps/map9/leveldata', usefull.data_directory + 'res/maps/map10/leveldata',
                 )

levels = []
levels_data = []
current_level = 0
