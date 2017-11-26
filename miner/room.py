from game_map.rect import Rect
from miner.direction import Direction


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
        :return int, int: x,y for the corner of the wall
        """
        if direction == Direction.UP:
            return self.x1, self.y1
        elif direction == Direction.RIGHT:
            return self.x2, self.y1
        elif direction == Direction.DOWN:
            return self.x1, self.y2
        elif direction == Direction.LEFT:
            return self.x1, self.y1
