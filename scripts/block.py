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
        self.rect.topleft = (self.pos[0] * 86 + camera.offset.x, self.pos[1] * 86 + camera.offset.y)

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

    def update(self, level_maps, player):
        super().update(level_maps, player)
        if self.was_on_item:
            level_maps[2].remove(self)
            level_maps[1].remove(self)

    def copy(self):
        new_block = Key(self.img, self.walkable, self.layer, self.key)
        return new_block
