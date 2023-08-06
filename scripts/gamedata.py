import block
from enemy import Enemy
from player import Player
import pygame

items_dict = {0: None,
              1: block.Block(pygame.transform.scale(pygame.image.load("res/blocks/grass.png"), (86, 86)), True, 1),
              2: Enemy((72, 92), 3),
              3: Player(),
              4: block.Key(pygame.transform.scale(pygame.image.load("res/blocks/key.png"), (86, 86)), True, 2, 'Green'),
              5: block.EntranceBlock(pygame.transform.scale(pygame.image.load("res/blocks/entrance.png"), (86, 86)),
                                     False, 3, 'Green'),
              6: block.EntranceBlock(pygame.transform.scale(pygame.image.load("res/blocks/entrance.png"), (86, 86)),
                                     False, 3, 'None'),
              7: block.WinBlock(pygame.transform.scale(pygame.image.load("res/blocks/WinBlock.png"), (86, 86)), True,
                                1),
              8: block.WaterBlock(pygame.transform.scale(pygame.image.load("res/blocks/WaterBlock.png"), (86, 86)),
                                  False, 2, 'Oak Log',
                                  pygame.transform.scale(pygame.image.load("res/blocks/WaterBlockOakLog.png"),
                                                         (86, 86))),
              9: block.Key(pygame.transform.scale(pygame.image.load("res/blocks/OakLog.png"), (86, 86)), True, 2,
                           'Oak Log'),
              10: block.Block(pygame.transform.scale(pygame.image.load("res/blocks/sand.png"), (86, 86)), True, 1)}

original_levels = ('res/maps/map1/map', 'res/maps/map2/map', 'res/maps/map3/map', 'res/maps/map4/map')
original_data = ('res/maps/map1/map_data', 'res/maps/map2/map_data', 'res/maps/map3/map_data', 'res/maps/map4/map_data')

levels = []
levels_data = []
current_level = 0


class Data:
    data = []

    @staticmethod
    def read_data():
        Data.data = [data.strip() for data in open("/home/skajland/Downloads/Labirynt 3/data/data").readlines()]
        print(Data.data)

    @staticmethod
    def write_data(index, value):
        Data.data[index] = value
        fixed_data = [data + "\n" for data in Data.data]
        with open("/home/skajland/Downloads/Labirynt 3/data/data", 'w') as file:
            file.writelines(fixed_data)


Data.read_data()
Data.write_data(0, "Hunvee")