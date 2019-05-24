from random import randint


class CAMap:
    """

    """
    # X, Y Transitions to the 8 neighboring cells
    neighbors = [(-1, -1), (0, -1), (1, -1),
                 (-1, 0), (1, 0),
                 (-1, 1), (0, 1), (1, 1)]

    def __init__(self, width, height):
        """
        Create a new CA Map
        :param int width: Map width in tiles
        :param int height: Map height in tiles
        """
        self.width = width
        self.height = height
        self.tiles = None

    def reset_map(self, live_chance=50):
        """
        Clear the CA Map
        :param int  live_chance: 0-100, likelihood that the cell is alive
        """
        self.tiles = [
            [(randint(1,100) <= live_chance)
             for _ in range(self.height)]
            for _ in range(self.width)]

    def point_in_map(self, x, y):
        """
        Checks if a given point falls within the current map
        :param x: Target X position
        :param y: Target Y position
        :return: True if desired location is within map bounds
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def count_alive_neighbors(self, x, y, invalid=1):
        count = 0
        for dx, dy in CAMap.neighbors:
            tx, ty = x + dx, y + dy
            if not self.point_in_map(tx, ty):
                count += invalid
            elif self.tiles[tx][ty]:
                count += 1
        return count

    def printable_map(self, block_char="#", open_char="."):
        """
        Produce a string representation of the current Game Map
        :param block_char: symbol to represent a sight-blocking tile
        :param open_char: symbol to represent a see-through tile
        :return str: Printable Representation of the Game Map
        """
        output = ""
        for y in range(0, self.height):
            line = ""
            for x in range(0, self.width):
                if not self.tiles[x][y]:
                    line += block_char
                else:
                    line += open_char
            output += line + "\n"
        return output


class CADungeon:
    """
    Generate a Dungeon using Cellular Automata
    Process:
      Define an area
      Scatter Automata randomly
      Grow the Automatons for a number of iterations
      Locate unconnected regions
      Create connections.
    """

    def __init__(self, width, height, initial_live_chance=50,
                 death_limit=1, birth_limit=3):
        self.width = width
        self.height = height
        self.initial_live_chance = initial_live_chance
        self.death_limit = death_limit
        self.birth_limit = birth_limit
        self.current_map = CAMap(width, height)
        self.new_map = self.current_map
        self.current_map.reset_map(initial_live_chance)

    def generate(self, steps=1):
        self.current_map.reset_map(self.initial_live_chance)
        for s in range(0,steps):
            self.step()

    def step(self):
        for y in range(0, self.current_map.height):
            for x in range(0, self.current_map.width):
                neighbors = self.current_map.count_alive_neighbors(x, y)
                if self.current_map.tiles[x][y]:
                    self.new_map.tiles[x][y] = not (neighbors <= self.death_limit)
                else:
                    self.new_map.tiles[x][y] = (neighbors > self.birth_limit)
        self.current_map = self.new_map

    def __repr__(self):
        return self.current_map.printable_map()


if __name__ == "__main__":
    dungeon = CADungeon(80, 25, 33, 1, 4)
    dungeon.generate(50)
    print(dungeon)
