"""
Dungeon Maker
"""

from random import randrange

inclusive_range = lambda start, end: range(start, end + 1)


class Space:
    minSize = 1
    maxSize = 100

    def __init__(self, x, y, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.calculate_sides()

    def terrain(self, x, y):
        if x == self.left or x == self.right:
            return 1
        if y == self.top or y == self.bottom:
            return 1
        return 2

    def calculate_sides(self):
        self.top = self.y
        self.left = self.x
        self.right = self.x + self.width + 1
        self.bottom = self.y + self.height + 1

    def __repr__(self):
        return "({0},{1})-({2},{3})".format(self.left, self.top,
                                            self.right, self.bottom)


class Room(Space):
    minSize = 5
    maxSize = 9

    def __init__(self, x, y, width=0, height=0):
        super(Room, self).__init__(x, y, width, height)

    def generate(self):
        if self.width < Room.minSize or self.width > Room.maxSize:
            self.width = randrange(Room.minSize, Room.maxSize)
        if self.height < Room.minSize or self.height > Room.maxSize:
            self.height = randrange(Room.minSize, Room.maxSize)
        self.calculate_sides()


class Dungeon:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = {}
        self.rooms = []
        self.init_grid()

    def init_grid(self):
        """Set up an empty map grid"""
        for row in range(0, self.height):
            for col in range(0, self.width):
                self.grid[(row, col)] = 0

    def add_grid(self, space):
        """Add a space to the map grid"""
        for row in inclusive_range(space.top, space.bottom):
            for col in inclusive_range(space.left, space.right):
                self.grid[
                    (col, row)] = space.terrain(col, row)

    def generate_room(self, tries=3, width=0, height=0):
        """Create a new room at a random position"""
        x = randrange(0, self.width)
        y = randrange(0, self.height)
        # room = Room(x, y, 3, 3)
        room = Room(x, y, width, height)
        if width > 0 and height > 0:
            room.generate()

        if self.check_room(room):
            self.rooms.append(room)
            self.add_grid(room)
        elif tries >= 0:
            # It didn't fit, try again
            self.generate_room(tries - 1)

    def check_room(self, room):
        """Make sure the room fits on the map"""
        # Check room edges are within the map
        if room.top < 0 or room.bottom >= self.height:
            return False
        if room.left < 0 or room.right >= self.width:
            return False

        # Check if any part of the room overlaps an existing space
        # Two rectangles do not overlap if one is completely below or
        # completely to the left of the other
        for space in self.rooms:
            if space.left > room.right or room.left > space.right:
                continue
            elif space.top > room.bottom or room.top > space.bottom:
                continue
            else:
                return False

        # The room fits
        return True

    def show_grid(self):
        for row in range(0, self.height):
            line = ""
            for col in range(0, self.width):
                line += str(self.grid[(row, col)])
            print(line)

    def __repr__(self):
        return "({0} x {1}))".format(self.width, self.height)


dungeon = Dungeon(64, 32)
dungeon.generate_room(5)
dungeon.generate_room(5)
dungeon.generate_room(5)
dungeon.generate_room(5)
dungeon.generate_room(5)
dungeon.generate_room(5)
print(dungeon.rooms)
dungeon.show_grid()
