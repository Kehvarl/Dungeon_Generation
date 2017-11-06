from enum import Enum
from random import randrange, randint


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


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

    def __init__(self, width=80, height=25):
        self.width = width
        self.height = height
        self.center = (width // 2, height // 2)
        self.grid = {}
        self.features = []
        self._init_grid()
        x, y = self.center
        x, y = self._add_rect(x - 2, y - 2, 5, 5)
        self.features.append((x, y))

    def _init_grid(self):
        """Set up an empty map grid"""
        for row in range(0, self.height):
            for col in range(0, self.width):
                self.grid[(col, row)] = "#"

    @staticmethod
    def _random_direction():
        """
        Pick a random direction
        :return Direction:
        """
        return Direction(randrange(0, 3))

    def _get_wall(self, direction, x, y):
        """
        Find the first wall in a given direction
        :param Direction direction: direction to look
        :param int x: Starting X
        :param int y: Starting Y
        :return int, int: position of wall
        """
        tx, ty = x, y
        while 0 < tx < self.width - 1 and 0 < ty < self.height - 1 and self.grid[(tx, ty)] != "#":
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
                    if self.grid[(col, row)] != "#":
                        return False
                else:
                    return False
        return True

    def _add_rect(self, x, y, width, height):
        """
        Clear a rectangle in the grid
        :param int x: Starting X
        :param int y: Starting Y
        :param int width:
        :param int height:
        return int, int: Center of feature
        """
        for row in range(y, y + height + 1):
            for col in range(x, x + width + 1):
                self.grid[(col, row)] = " "
        return x + width // 2, y + height // 2

    def add_feature(self):
        """
        Add a feature to the map
        return bool: True if feature was added
        """
        x, y = self.features[-1]
        direction = self._random_direction()
        width = randint(1, 5)
        height = randint(1, 5)
        x, y = self._get_wall(direction, x, y)
        if self._scan_direction(direction, x, y, width, height):
            x, y = self._add_rect(x, y, width, height)
            self.features.append((x, y))
            return True
        return False

    def show_grid(self):
        """
        Display the current map
        """
        for row in range(0, self.height):
            line = ""
            for col in range(0, self.width):
                line += str(self.grid[(col, row)])
            print(line)


if __name__ == "__main__":
    miner = Miner()
    while miner.add_feature():
        pass
    miner.show_grid()
