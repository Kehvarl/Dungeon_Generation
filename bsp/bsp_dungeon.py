from random import random, randint


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, grid):
        for x in range(self.x, self.x + self.width):
            for y in range(self.y, self.y + self.height):
                if x == self.x or x == self.x + self.width - 1 or y == self.y or y == self.y + self.height - 1:
                    grid[(y, x)] = "#"
                else:
                    grid[(y, x)] = "."


class Leaf:
    MIN_LEAF_SIZE = 9

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = []
        self.room = None
        self.corridors = []

    def split(self):
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

        if split_horizontal:
            split = randint(Leaf.MIN_LEAF_SIZE, split_max)
            self.children.append(Leaf(self.x, self.y, self.width, split))
            self.children.append(Leaf(self.x, self.y + split, self.width, self.height - split))
        else:
            split = randint(Leaf.MIN_LEAF_SIZE, split_max)
            self.children.append(Leaf(self.x, self.y, split, self.height))
            self.children.append(Leaf(self.x + split, self.y, self.width - split, self.height))

        for leaf in self.children:
            leaf.split()

        return True

    def generate_room(self):
        if self.children:
            for leaf in self.children:
                leaf.generate_room()
        else:
            dx = randint(0, 3)
            dy = randint(0, 3)
            width = randint(self.width - 3, self.width) - dx
            height = randint(self.height - 3, self.height) - dy
            self.room = Rect(self.x + dx, self.y + dy, width, height)

    def draw_room(self, grid):
        if self.children:
            for leaf in self.children:
                leaf.draw_room(grid)
        else:
            self.room.draw(grid)


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

    def generate_rooms(self):
        if self.root:
            self.root.generate_room()

    def split(self):
        if self.root:
            self.root.split()

    def fill_grid(self):
        if self.root:
            self.root.draw_room(self.grid)

    def show_grid(self):
        for row in range(0, self.height):
            line = ""
            for col in range(0, self.width):
                line += str(self.grid.get((row, col), "*"))
            print(line)


if __name__ == "__main__":
    dungeon = BSPDungeon(80,25)
    dungeon.split()
    dungeon.generate_rooms()
    dungeon.fill_grid()
    dungeon.show_grid()
