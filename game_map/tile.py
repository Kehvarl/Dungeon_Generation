class Tile:
    def __init__(self, block_move=True, block_sight=True):
        self.block_move = block_move
        self.block_sight = block_sight

    def block(self, block_state=False):
        """
        :param bool block_state:
        """
        self.block_sight = block_state
        self.block_move = block_state
