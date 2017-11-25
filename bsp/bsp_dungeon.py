from random import randint
from game_map.game_map import GameMap
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

    def __init__(self, game_map):
        """
        :param GameMap game_map:
        """
        self.root = None
        self.rooms_list = []
        self.game_map = game_map
        self.width = self.game_map.width
        self.height = self.game_map.height
        self.init_tree()
        self.game_map.clear_map()

    def init_tree(self):
        """Set up an empty map grid"""
        self.root = Leaf(0, 0, self.width, self.height)

    def generate(self, fill=False):
        self._split()
        self._generate_rooms(fill)
        self._generate_corridors()

    def _split(self):
        """
        Divide the space into leaves on a binary spanning tree
        """
        if self.root:
            self.root.split()

    def _generate_rooms(self, fill=False):
        """
        Fill each child node of the tree with a room
        Collect all created rooms into a list
        :param bool fill: If True, rooms take up the entirety of a node
        """
        if self.root:
            self.root.generate_room(fill)
        self.root.get_rooms(self.rooms_list)
        self._fill_grid()

    def _fill_grid(self):
        """
        Draw the rooms into the map grid
        """
        for room in self.rooms_list:
            for x in range(room.x1, room.x2):
                for y in range(room.y1, room.y2):
                    if x == room.x1 or x == room.x2 - 1 or y == room.y1 or y == room.y2 - 1:
                        self.game_map.tiles[x][y].block(True)
                    else:
                        self.game_map.tiles[x][y].block(False)

    def _generate_corridors(self):
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
                    self._create_h_tunnel(prev_x, new_x, prev_y)
                    self._create_v_tunnel(prev_y, new_y, new_x)
                else:
                    # Vertical tunnel, then Horizontal
                    self._create_v_tunnel(prev_y, new_y, prev_x)
                    self._create_h_tunnel(prev_x, new_x, new_y)
                pass

    def _create_h_tunnel(self, x1, x2, y):
        """
        Create a tunnel
        :param int x1: Start of Tunnel
        :param int x2: End of Tunnel
        :param int y: The y position of the tunnel
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.game_map.tiles[x][y].block(False)

    def _create_v_tunnel(self, y1, y2, x):
        """
        Create a vertical tunnel
        :param int y1: Start of Tunnel
        :param int y2: End of Tunnel
        :param int x: X position of the tunnel
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.game_map.tiles[x][y].block(False)


if __name__ == "__main__":
    test_map = GameMap(80, 25)
    dungeon = BSPDungeon(test_map)
    dungeon.generate(fill=True)
    print(dungeon.game_map.printable_map())
