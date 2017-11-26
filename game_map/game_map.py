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

    def create_room(self, room):
        """
        Set the tiles of a room to be passable
        :param Map.room.Room room: The room in the map
        """
        # Make interior tiles passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].block()

    def create_h_tunnel(self, x1, x2, y):
        """
        Create a tunnel
        :param int x1: Start of Tunnel
        :param int x2: End of Tunnel
        :param int y: The y position of the tunnel
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].block(False)

    def create_v_tunnel(self, y1, y2, x):
        """
        Create a vertical tunnel
        :param int y1: Start of Tunnel
        :param int y2: End of Tunnel
        :param int x: X position of the tunnel
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].block(False)

    def point_in_map(self, x, y):
        """
        Checks if a given point falls within the current map
        :param x: Target X position
        :param y: Target Y position
        :return: True if desired location is within map bounds
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def room_in_map(self, room):
        """
        Checks if a given room fits completely on the map
        :param room:
        :return: True if desired location is within map bounds
        """
        return self.point_in_map(room.x1, room.y1) and self.point_in_map(room.x2, room.y2)

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
