from random import randint
from game_map.game_map import GameMap
from game_map.room import Room
from game_map.direction import Direction


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

    def generate_feature(self, direction=None, feature_index=None):
        if direction is None:
            direction = Direction.random_direction()
        if feature_index is None:
            feature_index = randint(0, len(self.features)-1)

        x, y = self.features[feature_index].get_wall_point(direction)
        width = randint(1, 11)
        height = randint(1, 11)
        if direction == Direction.LEFT:
            x -= width
        if direction == Direction.UP:
            y -= height

        x, y, width, height = self.select_feature(x, y, direction)

        if not self.add_feature(x, y, width, height) and feature_index > 0:
            self.generate_feature(feature_index=feature_index-1)

    def select_feature(self, x, y, direction):
        x2, y2 = x, y
        if randint(0, 1) == 0:
            # Corridor
            if direction == Direction.UP:
                x2 = x
                y2 = randint(1, y)
            if direction == Direction.RIGHT:
                x2 = randint(x, self.width - 1)
                y2 = y
            if direction == Direction.DOWN:
                x2 = x
                y2 = randint(y, self.height - 1)
            if direction == Direction.LEFT:
                x2 = randint(1, x)
                y2 = y
        else:
            # Room
            if direction == Direction.UP:
                x2 = randint(x, self.width - 1)
                y2 = randint(1, y)
            if direction == Direction.RIGHT:
                x2 = randint(x, self.width - 1)
                y2 = randint(y, self.height - 1)
            if direction == Direction.DOWN:
                x2 = randint(x, self.width - 1)
                y2 = randint(y, self.height - 1)
            if direction == Direction.LEFT:
                x2 = randint(1, x)
                y2 = randint(y, self.height - 1)

        return min(x, x2), min(y, y2), x2 - x, y2 - y

    def add_feature(self, x, y, width, height):
        room = Room(x, y, width, height)

        if not self.game_map.room_in_map(room):
            return False

        for other_room in self.features:
            if room.intersect(other_room):
                break
        else:
            self.features.append(room)
            self.game_map.create_room(room)
            return True
        return False


if __name__ == "__main__":
    test_map = GameMap(80, 25)
    miner = Miner(test_map)
    x1 = randint(5, 60)
    y1 = randint(5, 15)
    miner.add_feature(x1, y1, 5, 5)
    miner.generate_feature()
    print(miner.game_map.printable_map())
    print(len(miner.features))
