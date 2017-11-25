class Rect:
    """
    A rectangular space
    """
    def __init__(self, x, y, width, height):
        """

        :param int x:
        :param int y:
        :param int width:
        :param int height:
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def x1(self):
        return self.x

    @property
    def y1(self):
        return self.y

    @property
    def x2(self):
        return self.x + self.width

    @property
    def y2(self):
        return self.y + self.height

    def intersect(self, other):
        """
        Check for overlapping rooms
        :param Rect other: other room to test
        :return bool: True if the two rooms overlap
        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def center(self):
        """
        :return int, int: the approximate coordinates for the center this space
        """
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return center_x, center_y
