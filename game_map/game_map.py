from game_map.tile import Tile


class GameMap:
    def __init__(self, width, height):
        """
        Create a new Game Map
        :param int width: Map width in tiles
        :param int height: Map height in tiles
        """
        self.width = width
        self.height = height
        self.tiles = None

    def clear_map(self, default_block_move=True, default_block_sight=True):
        """
        Clear the Game Map
        :param bool default_block_move: do Tile prevent movement by default
        :param bool default_block_sight: do Tiles block sight by default
        """
        self.tiles = [
            [Tile(block_move=default_block_move,
                  block_sight=default_block_sight)
             for _ in range(self.height)]
            for _ in range(self.width)]

    def printable_map(self, block_char="#", open_char="."):
        """
        Produce a string representation of the current Game Map
        :param block_char: symbol to represent a sight-blocking tile
        :param open_char: symbol to represent a see-through tile
        :return str: Printable Representation of the Game Map
        """
        output = ""
        for y in range(0, self.height):
            line = ""
            for x in range(0, self.width):
                if self.tiles[x][y].block_sight:
                    line += block_char
                else:
                    line += open_char
            output += line + "\n"
        return output
