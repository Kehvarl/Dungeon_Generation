from random import randint
from enum import Enum


class Direction(Enum):
    """
    Class for handling directions and moving between them.
    """
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
        return Direction(randint(0, 3))

    @staticmethod
    def next_direction(direction):
        """
        Clockwise from the given direction
        :param int direction:
        :return Direction:
        """
        return Direction((direction + 1) % 4)

    @staticmethod
    def previous_direction(direction):
        """
        Counter-clockwise from the given direction
        :param int direction:
        :return Direction:
        """
        return Direction((direction - 1) % 4)
