from random import randint, choice

from game_map.game_map import GameMap

from miner.direction import Direction
from miner.room import Room


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

    def __init__(self, game_map):
        """
        :param GameMap game_map:
        """
        self.game_map = game_map
        self.game_map.clear_map()
        self.width = game_map.width
        self.height = game_map.height
        self.features = []
        self.initial_feature()

    def initial_feature(self, width=None, height=None):
        if width is None:
            width = randint(5, 11)
        if height is None:
            height = randint(5, 11)
        x = self.width // 2 - width // 1
        y = self.height // 2 - height // 2
        room = Room(x, y, width, height)
        self.features.append(room)
        self.game_map.create_room(room)

    def add_feature(self, room, width=None, height=None):
        """
        Add a feature to the map
        :param Room room: room to start from
        :param int width:
        :param int height:
        :return bool: True if the feature was able to be added
        """
        direction = Direction.random_direction()
        if width is None:
            width = randint(3, 11)
        if height is None:
            height = randint(3, 11)

        gap = randint(0, 5)

        x, y = room.get_wall(direction)
        if direction == Direction.UP:
            y -= (height + gap)
        elif direction == Direction.RIGHT:
            x += gap
        elif direction == Direction.DOWN:
            y += gap
        elif direction == Direction.LEFT:
            x -= (width + gap)

        new_room = Room(x, y, width, height)

        if self.game_map.room_in_map(new_room):
            # Check for Intersections
            for other_room in self.features:
                if new_room.intersect(other_room):
                    break
            else:
                self.features.append(new_room)
                self._add_corridor(room, new_room)
                self.game_map.create_room(new_room)
                return True

        return False

    def _add_corridor(self, room1, room2):
        """
        Add connecting corridors between rooms
        """
        x1, y1 = room1.center()
        x2, y2 = room2.center()
        # Randomly determine corridor arrangement.
        if randint(0, 1) == 1:
            # Horizontal tunnel, then Vertical
            self.game_map.create_h_tunnel(x2, x1, y2)
            self.game_map.create_v_tunnel(y2, y1, x1)
        else:
            # Vertical tunnel, then Horizontal
            self.game_map.create_v_tunnel(y2, y1, x2)
            self.game_map.create_h_tunnel(x1, x1, y1)
        pass


if __name__ == "__main__":
    test_map = GameMap(80, 25)
    miner = Miner(test_map)
    miner.add_feature(choice(miner.features))
    miner.add_feature(choice(miner.features))
    miner.add_feature(choice(miner.features))
    miner.add_feature(choice(miner.features))
    miner.add_feature(choice(miner.features))
    miner.add_feature(choice(miner.features))
    miner.add_feature(choice(miner.features))
    miner.add_feature(choice(miner.features))
    miner.add_feature(choice(miner.features))

    print(miner.game_map.printable_map())
