from random import randint
from game_map.direction import Direction
from game_map.rect import Rect


class Room(Rect):
    """
    A Room is just a Rect that can tell you where its walls are
    """
    def __init__(self, x, y, width, height):
        super(Room, self).__init__(x, y, width, height)

    def get_wall(self, direction):
        """
        Find the first wall in a given direction
        :param Direction direction: direction to look
        :return int, int, int, int: x1,y1, x2,y2 defining the wall
        """
        if direction == Direction.UP:
            return self.x1, self.y1 - 1, self.x2, self.y1 - 1
        elif direction == Direction.RIGHT:
            return self.x2 + 1, self.y1, self.x2 + 1, self.y2
        elif direction == Direction.DOWN:
            return self.x1, self.y2 + 1, self.x2, self.y2 + 1
        elif direction == Direction.LEFT:
            return self.x1 - 1, self.y1, self.x1 - 1, self.y2

    def get_wall_point(self, direction=None):
        """
        Returns a random point from the wall in the indicated direction
        :param Direction direction:
        :return int, int: x, y point along wall
        """
        if direction is None:
            direction = Direction.random_direction()

        x1, y1, x2, y2 = self.get_wall(direction)
        x = randint(x1, x2)
        y = randint(y1, y2)
        return x, y
