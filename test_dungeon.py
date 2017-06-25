import pytest
import dungeon


test_map = dungeon.Dungeon(32, 16)


def test_room():
    room = dungeon.Room(3, 3, 3, 3)
    assert test_map.check_room(room) == True


def test_room_edge():
    room = dungeon.Room(8, 16, 3, 3)
    assert test_map.check_room(room) == True
