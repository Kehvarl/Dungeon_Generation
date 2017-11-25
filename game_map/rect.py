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
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height

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
        Get the center of the room
        :return int, int: x position, y position
        """
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y
