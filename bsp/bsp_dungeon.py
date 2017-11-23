from random import random, randint


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def center(self):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return center_x, center_y

    def draw(self, grid):
        for x in range(self.x, self.x + self.width):
            for y in range(self.y, self.y + self.height):
                if x == self.x or x == self.x + self.width - 1 or y == self.y or y == self.y + self.height - 1:
                    grid[(y, x)] = "#"
                else:
                    grid[(y, x)] = "."


class Leaf:
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
        If succesful, call split on each child node
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
        Fill the node with a room
        :param bool fill: Room fills node completely
        """
        if self.children:
            for leaf in self.children:
                leaf.generate_room(fill)
        else:
            if fill:
                self.room = Rect(self.x, self.y, self.width, self.height)
            else:
                dx = randint(0, 3)
                dy = randint(0, 3)
                width = randint(self.width - 3, self.width) - dx
                height = randint(self.height - 3, self.height) - dy
                self.room = Rect(self.x + dx, self.y + dy, width, height)

    def get_room(self, rooms_list):
        """

        :param list rooms_list:
        """
        if self.children:
            for leaf in self.children:
                leaf.get_room(rooms_list)
        else:
            rooms_list.append(self.room)


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

    def generate_rooms(self, fill=False):
        if self.root:
            self.root.generate_room(fill)
        self.root.get_room(self.rooms_list)

    def generate_corridors(self):
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

    def split(self):
        if self.root:
            self.root.split()

    def fill_grid(self):
        for room in self.rooms_list:
            room.draw(self.grid)

    def show_grid(self):
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
