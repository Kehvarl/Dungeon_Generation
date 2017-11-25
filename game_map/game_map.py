from game_map.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = None

    def clear_map(self, default_block_move=True, default_block_sight=True):
        self.tiles = [
            [Tile(block_move=default_block_move,
                  block_sight=default_block_sight)
             for _ in range(self.height)]
            for _ in range(self.width)]
