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

    def center(self):
        """
        :return int, int: the approximate coordinates for the center this space
        """
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return center_x, center_y
