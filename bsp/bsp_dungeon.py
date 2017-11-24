from random import randint
from bsp.bsp_leaf import Leaf


class BSPDungeon:
    """
    Generate a Dungeon using the BSP algorithm
    Process:
      Define an area
      Select Horizontal or Vertical
      Divide the area randomly either Horizontally or Vertically
      Repeat in each new area for a pre-defined number of iterations
      Define an space within each area
      Connect adjacent spaces
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = None
        self.rooms_list = []
        self.grid = {}
        self.init_tree()
        self.init_grid()

    def init_tree(self):
        """Set up an empty map grid"""
        self.root = Leaf(0, 0, self.width, self.height)

    def init_grid(self):
        """Set up an empty map grid"""
        for row in range(0, self.height):
            for col in range(0, self.width):
                self.grid[(row, col)] = " "

    def split(self):
        """
        Divide the space into leaves on a binary spanning tree
        """
        if self.root:
            self.root.split()

    def generate_rooms(self, fill=False):
        """
        Fill each child node of the tree with a room
        :param bool fill: If True, rooms take up the entirety of a node
        """
        if self.root:
            self.root.generate_room(fill)
        self.root.get_rooms(self.rooms_list)

    def generate_corridors(self):
        """
        Add connecting corridors between rooms
        """
        first_room = True
        new_x, new_y = 0, 0
        for room in self.rooms_list:
            if first_room:
                first_room = False
                new_x, new_y = room.center()
            else:
                prev_x, prev_y = new_x, new_y
                new_x, new_y = room.center()
                # Randomly determine corridor arrangement.
                if randint(0, 1) == 1:
                    # Horizontal tunnel, then Vertical
                    self.create_h_tunnel(prev_x, new_x, prev_y)
                    self.create_v_tunnel(prev_y, new_y, new_x)
                else:
                    # Vertical tunnel, then Horizontal
                    self.create_v_tunnel(prev_y, new_y, prev_x)
                    self.create_h_tunnel(prev_x, new_x, new_y)
                pass

    def create_h_tunnel(self, x1, x2, y):
        """
        Create a tunnel
        :param int x1: Start of Tunnel
        :param int x2: End of Tunnel
        :param int y: The y position of the tunnel
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.grid[(y, x)] = "."

    def create_v_tunnel(self, y1, y2, x):
        """
        Create a vertical tunnel
        :param int y1: Start of Tunnel
        :param int y2: End of Tunnel
        :param int x: X position of the tunnel
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.grid[(y, x)] = "."

    def fill_grid(self):
        """
        Draw the rooms into the map grid
        """
        for room in self.rooms_list:
            for x in range(room.x, room.x + room.width):
                for y in range(room.y, room.y + room.height):
                    if x == room.x or x == room.x + room.width - 1 or y == room.y or y == room.y + room.height - 1:
                        self.grid[(y, x)] = "#"
                    else:
                        self.grid[(y, x)] = "."

    def show_grid(self):
        """
        Print the map grid
        """
        for row in range(0, self.height):
            line = ""
            for col in range(0, self.width):
                line += str(self.grid.get((row, col), "*"))
            print(line)


if __name__ == "__main__":
    dungeon = BSPDungeon(80, 25)
    dungeon.split()
    dungeon.generate_rooms(fill=True)
    dungeon.fill_grid()
    dungeon.generate_corridors()
    dungeon.show_grid()
