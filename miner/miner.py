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
        self.center = (width//2, height//2)
        self.grid = {}
        self.features = []
        self.init_grid()
        x, y = self.center
        x, y = self.add_rect(x-2, y-2, 5, 5)
        self.features.append((x, y))

    def init_grid(self):
        """Set up an empty map grid"""
        for row in range(0, self.height):
            for col in range(0, self.width):
                self.grid[(row, col)] = "#"

    def add_rect(self, x, y, width, height):
        """
        Clear a rectangle in the grid
        :param int x: Starting X
        :param int y: Starting Y
        :param int width:
        :param int height:
        return int, int: Center of feature
        """
        for row in range(y, y+height+1):
            for col in range(x, x+width+1):
                self.grid[(row, col)] = " "
        return x + width//2, y+height//2
