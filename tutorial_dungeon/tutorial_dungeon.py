from game_map.game_map import GameMap
from game_map.rect import Rect

from random import randint


class TutorialDungeon:
    """
    Generate a dungeon using the algorithm from the RogueBasin tutorial
    Source: http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_3
    Process:
        Add randomly-sized rooms to random locations in the map
        If a new room overlaps an existing one, discard it
        After all rooms added
            connect each room with the previous room using a corridor
    """
    def __init__(self, game_map):
        """
        :param GameMap game_map:
        """
        self.game_map = game_map
        self.width = game_map.width
        self.height = game_map.height
        self.game_map.clear_map()
        self.rooms_list = []

    def generate(self, max_rooms=1, room_min_size=5, room_max_size=10):
        """
        Create initial Map Layout
        :param int max_rooms: Number of rooms to attempt to generate
        :param int room_min_size: Smallest allowable room (width or height)
        :param int room_max_size: Largest allowable room (width or height)
        """
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)

            # Room class stores some useful features
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in self.rooms_list:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
                # "paint" it to the map's tiles
                self._create_room(new_room)

                # finally, append the new room to the list
                self.rooms_list.append(new_room)
                num_rooms += 1
        self._generate_corridors()

    def _create_room(self, room):
        """
        Set the tiles of a room to be passable
        :param Map.room.Room room: The room in the map
        """
        # Make interior tiles passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.game_map.tiles[x][y].block()

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
    dungeon = TutorialDungeon(test_map)
    dungeon.generate(max_rooms=10)
    print(dungeon.game_map.printable_map())