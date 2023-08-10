import camera
import gamedata
import pygame
from player import Player
background_color = (105, 200, 75)
difficulty_multiplier = 1
current_difficulty = 1  # 0 = easy 1 = mid 2 = hard
destroy = []


def copy_item(original_item):
    if original_item is not None:
        new_item = original_item.copy()
        return new_item
    return None


def level_loader(file_raw, object_dict):
    # the cool part
    with open(file_raw, "r") as file:
        lines = file.readlines()

    level_map = []
    for line in lines:
        line_stripped = line.strip().strip("[]")
        row = line_stripped.split("][")
        level_row = (
            [[int(row_string)] if ',' not in row_string else [int(item) for item in row_string.split(',')] for
             row_string in
             row])
        level_map.append(level_row)

    # transform to item
    for i, level in enumerate(level_map):
        for j, level_item_list in enumerate(level):
            for k, level_item in enumerate(level_item_list):
                level_map[i][j][k] = copy_item(object_dict.get(level_item))
    return level_map


def render_level(screen):
    for level in level_maps[2]:
        if hasattr(level, 'img'):
            if level.img is None:
                continue
        level.render(screen)


def start(lvl_map, opt_lvl_map, sorted_lvl_map, data):
    global player
    for i, level in enumerate(lvl_map):
        for j, level_item_list in enumerate(level):
            for k, level_item in enumerate(level_item_list):
                if level_item is None or type(level_item) != Player:
                    continue
                opt_lvl_map.remove(level_item)
                player = level_item
                camera.offset = pygame.math.Vector2(
                    camera.screen_size[0] / 2 - player.image.get_width() / 2 - (j * 86 + camera.offset.x) + data[0],
                    camera.screen_size[1] / 2 - player.image.get_height() / 2 - (i * 86 + camera.offset.y) + data[1])
                player.rect.topleft += camera.offset
                break

    for i, level in enumerate(lvl_map):
        for j, level_item_list in enumerate(level):
            for level_item in level_item_list:
                if level_item is None:
                    continue
                level_item.rect.topleft = (j * 86 + camera.offset.x, i * 86 + camera.offset.y)
                level_item.pos = (j, i)
                level_item.start(opt_lvl_map)


def update():
    player.update(level_maps, player)
    for level_item in level_maps[1]:
        level_item.update(level_maps, player)
    for destroy_item in destroy:
        level_maps[1].remove(destroy_item)
        level_maps[2].remove(destroy_item)
        destroy.remove(destroy_item)


def load_map():
    global player, background_color, level_maps, difficulty_multiplier
    data = level_data()
    camera.left, camera.top, camera.right, camera.bottom = data[2]
    background_color = data[1]
    difficulty_multiplier = [difficulty_data / 100 for difficulty_data in data[3]]
    level_map1 = level_loader(gamedata.levels[gamedata.current_level], gamedata.items_dict)
    gamedata.current_level += 1
    optimized_level_map = [level_block for level_row in level_map1 for level_list in level_row for level_block in
                           level_list if level_block is not None]
    sorted_level_map = sorted((x for x in optimized_level_map if x is not None), key=lambda x: x.layer)
    camera.offset = pygame.Vector2()
    start(level_map1, optimized_level_map, sorted_level_map, data[0])
    level_maps = level_map1, optimized_level_map, sorted_level_map
    update()


def level_data():
    data = []
    with open(gamedata.levels_data[gamedata.current_level], 'r') as file:
        lines = file.readlines()
        for line in lines:
            line_stripped = line.strip().split(':')
            line_data = [int(data) if ',' not in line_stripped[1] else int(data) for data in line_stripped[1].split(",")]
            data.append(line_data)
    return data


player = None
level_maps = None


class Data:
    data = []

    @staticmethod
    def read_data():
        Data.data =[data.strip() for data in open("/home/skajland/Downloads/Labirynt 3/data/data").readlines()]

    @staticmethod
    def write_data(index, value):
        Data.data[index] = value
        fixed_data = [data + "\n" for data in Data.data]
        with open("/home/skajland/Downloads/Labirynt 3/data/data", 'w') as file:
            file.writelines(fixed_data)


Data.read_data()
