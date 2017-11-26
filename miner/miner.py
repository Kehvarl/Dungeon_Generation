from enum import Enum
from random import randrange, randint

from game_map.game_map import GameMap
from game_map.rect import Rect


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def random_direction():
        """
        Pick a random direction
        :return Direction:
        """
        return Direction(randrange(0, 3))

    @staticmethod
    def next_direction(direction):
        """
        Clockwise from the given direction
        :param int direction:
        :return Direction:
        """
        return Direction((direction + 1) % 4)

    @staticmethod
    def previos_direction(direction):
        """
        Counter-clockwise from the given direction
        :param int direction:
        :return Direction:
        """
        return Direction((direction - 1) % 4)


class Miner:
    """
    Source: http://www.roguebasin.com/index.php?title=Dungeon-Building_Algorithm
    Algorithm:
        Fill the whole map with solid earth
        Dig out a single room in the centre of the map
        Pick a wall of any room
        Decide upon a new feature to build
        See if there is room to add the new feature through the chosen wall
        If yes, continue. If no, go back to step 3
        Add the feature through the chosen wall
        Go back to step 3, until the dungeon is complete
    """

    def __init__(self, game_map):
        """
        :param GameMap game_map:
        """
        self.game_map = game_map
        self.game_map.clear_map()
        self.width = game_map.width
        self.height = game_map.height
        self.features = []
        self.initial_feature()

    def initial_feature(self, width=None, height=None):
        if width is None:
            width = randint(3, 11)
        if height is None:
            height = randint(3, 11)
        x = self.width//2 + randrange(-width//2, width//2)
        y = self.width // 2 + randrange(-height//2, height//2)
        room = Rect(x, y, width, height)
        self.features.append(room)
        self._create_room(room)

    def add_feature(self, x, y, width=None, height=None):
        """
        Add a feature to the map
        :param int x:
        :param int y:
        :param int width:
        :param int height:
        :return bool: True if the feature was able to be added
        """
        direction = Direction.random_direction()
        if width is None:
            width = randint(3, 11)
        if height is None:
            height = randint(3, 11)

        x, y = self._get_wall(direction, x, y)
        if self._scan_direction(direction, x, y, width, height):
            return True
        return False

    def _get_wall(self, direction, x, y):
        """
        Find the first wall in a given direction
        :param Direction direction: direction to look
        :param int x: Starting X
        :param int y: Starting Y
        :return int, int: position of wall
        """
        tx, ty = x, y
        while 0 < tx < self.width - 1 and 0 < ty < self.height - 1 and not self.game_map.tiles[x][y].block_sight:
            if direction == Direction.UP:
                ty -= 1
            elif direction == Direction.RIGHT:
                tx += 1
            elif direction == Direction.DOWN:
                ty += 1
            else:
                tx -= 1
        if direction == Direction.UP:
            ty -= 1
        elif direction == Direction.RIGHT:
            tx += 1
        elif direction == Direction.DOWN:
            ty += 1
        else:
            tx -= 1
        return tx, ty

    def _scan_direction(self, direction, x, y, width, height):
        """
        Scan past a wall in a given direction and check for space for the
        specified rectangle

        :param int width:
        :param int height:
        :return:
        """
        tx = x
        ty = y
        if direction == Direction.UP:
            ty = (ty - height) - 2
        elif direction == Direction.RIGHT:
            tx += 1
        elif direction == Direction.DOWN:
            ty += 1
        elif direction == Direction.LEFT:
            tx = (tx - width) - 2
        return self._scan_space(tx, ty, width, height)

    def _scan_space(self, x, y, width, height):
        """
        Check an area to see if a feature will fit.
        adjust position if needed to allow for fit.
        :param int x: Starting X
        :param int y: Starting Y
        :param int width:
        :param int height:
        :return bool: Can the feature be placed?
        """
        for row in range(y, y + height + 1):
            for col in range(x, x + width + 1):
                if 0 < col < self.width-1 and 0 < row < self.height-1:
                    if self.game_map.tiles[col][row].block_sight:
                        return False
                else:
                    return False
        return True

    def _create_room(self, room):
        """
        Set the tiles of a room to be passable
        :param Rect room: The room in the map
        """
        # Make interior tiles passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.game_map.tiles[x][y].block()


if __name__ == "__main__":
    test_map = GameMap(80, 25)
    miner = Miner(test_map)

    print(miner.game_map.printable_map())
