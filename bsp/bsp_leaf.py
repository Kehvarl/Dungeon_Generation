from random import random, randint

from game_map.rect import Rect


class Leaf:
    """
    A node in a Binary Spanning Tree
    """
    MIN_LEAF_SIZE = 11

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = []
        self.room = None
        self.corridors = []

    def split(self):
        """
        Attempt to divide this node into 2 smaller nodes
        If successful, call split on each child node
        :return: False if the node cannot be split
        """
        if self.width > 1.25 * self.height:
            split_horizontal = False
        elif self.height > 1.25 * self.width:
            split_horizontal = True
        else:
            split_horizontal = random() < 0.5

        if split_horizontal:
            split_max = self.height - Leaf.MIN_LEAF_SIZE
        else:
            split_max = self.width - Leaf.MIN_LEAF_SIZE

        if split_max < Leaf.MIN_LEAF_SIZE:
            return False

        split = randint(Leaf.MIN_LEAF_SIZE, split_max)

        if split_horizontal:
            self.children.append(Leaf(self.x, self.y, self.width, split))
            self.children.append(Leaf(self.x, self.y + split, self.width, self.height - split))
        else:
            self.children.append(Leaf(self.x, self.y, split, self.height))
            self.children.append(Leaf(self.x + split, self.y, self.width - split, self.height))

        for leaf in self.children:
            leaf.split()

        return True

    def generate_room(self, fill=False):
        """
        Create a room within the node
        :param bool fill: Room fills node completely
        """
        if self.children:
            for leaf in self.children:
                leaf.generate_room(fill)
        else:
            if fill:
                if self.x > 0:
                    self.x -= 1
                    self.width += 1
                if self.y > 0:
                    self.y -= 1
                    self.height += 1
                self.room = Rect(self.x, self.y, self.width, self.height)
            else:
                dx = randint(0, 3)
                dy = randint(0, 3)
                width = randint(self.width - 3, self.width) - dx
                height = randint(self.height - 3, self.height) - dy
                self.room = Rect(self.x + dx, self.y + dy, width, height)

    def get_rooms(self, rooms_list):
        """
        :param list rooms_list:
        """
        if self.children:
            for leaf in self.children:
                leaf.get_rooms(rooms_list)
        else:
            rooms_list.append(self.room)
