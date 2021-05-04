# pyglet can batch render graphics, texture, define play area, what blocks are shown, map position of user,
# map from play area of current positions in playarea,
# show and hide blocks
from creepcraft.game import cube_position
import pyglet
import time
from collections import dequeue
from pyglet.gl import *
from pyglet import image
from pyglet.graphics import TextureGroup

class Model(object):
    def __init__(self):
        # collection of verticies in lists to allow us batch rendering
        self.batch = pyglet.graphics.Batch()
        # TextureGroup manages an openGL texture
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())
        # define blocks in the world by mapping position to the texture block there
        self.world = {}
        # just like world, but we only map those blocks the user can see
        self.shown = {}
        # mapping from the user all shown blocks, to a pyglet verticies list
        self._shown = {}
        # Maps the sector positions in a list
        self.sectors = {}
        # a queue implementation for back-of-house show and hide block calls
        self.queue = dequeue()
        self._playarea()

    def _playarea(self):
        """[starts world, by placing blocks in play area. Sets wall, and areas of stone/dirt]
        """
        pass
        n = 80 # 1/2 width and height of playarea
        s = 1  # step size
        y = 0 # initial y height (vertical line!)
        # create a layer of stone across play area
        # create outterwall nested in that
        # out of loop, generate hills randomly
            # need x and z positions of the hills
            # set base of the hill
            # create a random variable to set height of the hill
            # create a random variable so 2 * s is the side length of the hill
            # set variable to 1 to quickly taper off side of hills
            # set variable to get a random block
            # do some loops in loops to populate those, use self.addblock method to add those verticies
        # decrement the side length so the hills taper off

    def find_block(self, position, vector, hit_range=8):
        """[search the users line of sight]

        Args:
            position ([tuple, length of 3]): [where user is]
            vector ([tuple, length of 3]): [line of sight]
            hit_range (int, optional): [how many blocks away are we looking for a hit at?]. Defaults to 8.
        """
        pass

    def visible_block(self, position):
        """[returns Bool indicating False if block is surrounded on all 6 sides by blocks, otherwise returns true. Allows us to hide unseen blocks for rendering]

        Args:
            position ([tuple of 3]): [block position to check]
        """
        pass

    def add_block(self, position, texture, immediate=True):
        """[add block with the texture and position into the playspace]

        Args:
            position ([tuple of 3]): [the (x, y, z) position of block to add]
            texture ([type]): [coordinates of texture square, use 'texture_position()' from game.py to generate]
            immediate (bool, optional): [should we draw the block immedietly?]. Defaults to True.
        """
        pass

    def remove_block(self, position, immediate=True):
        """[remove block with the texture and position out of the playspace]

        Args:
            position ([tuple of 3]): [the (x, y, z) position of block to delete]
            immediate (bool, optional): [should we remove the block immedietly?]. Defaults to True.
        """
        pass

    def block_buddies(self, position):
        """[check blocks surrounding position, hiding blocks that are not exposed to the user, and showing blocks that are]

        Args:
            position ([tuple of 3]): [position of user]
        """
        pass
        # going to need to use show_block() and hide_block() in this

    def show_block(self, position, immediate=True):
        """[assuming the block has already been added with add_block(), shows the block at that position specified]

        Args:
            position ([tuple of 3]): [position of block]
            immediate (bool, optional): [is the block shown now?]. Defaults to True.
        """
        pass

    def _show_block(self, position, texture):
        """[like the show_block, but private for us to use back-of-house]

        Args:
            position ([tuple of 3]): [position of block]
            texture ([type]): [use texture_list() to get coordinates of texture square]
        """
        x, y, z = position
        vertex_info = cube_position(x, y, z, 0.5)
        # create a list of info about texture
        texture_info = list(texture)
        self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_info),
            ('t2f/static', texture_info))

    def hide_block(self, position, Immediate=True):
        """[summary]

        Args:
            position ([tuple of 3]): [position of block]
            Immediate (bool, optional): [hides the block at given position]. Defaults to True.
        """
        pass

    def _hide_block(self, position):
        """[back-of-house way of hiding blocks to take care of]

        Args:
            position ([tuple of 3]): [position of block (x, y, z)]
        """
        self._shown.pop(position).delete()

    def show_sector(self, sector):
        """[draw all blocks that are shown to play area]"""
        pass

    def hide_sector(self, sector):
        """[remove all hidden blocks from play area]"""
        pass

    def change_sector(self, previous, new):
        """[change the 'before' sector to 'after' sectors are going to help us speed up rendering!]

        Args:
            previous ([x, y, z]): [description]
            new ([x, y, z]): [description]
        """
        pass

    def _enqueue(self, function, *args):
        """[add function to back-of-house queue]"""
        self.queue.append((function, args))

    def _dequeue(self):
        """[pop and call the function from back-of-house queue]"""
        function, args = self.queue.popleft()
        function(*args)

    def queue_timer(self):
        """[uses calls to _show_block(), _hide_block() to allow game to loop and run smoothly. Call this method everytime we use add_block() and remove_block()]
        """
        start = time.perf_counter()
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self._dequeue()

    def process_queue(self):
        """[process all of our back-of-house queue, without waiting]
        """
        while self.queue:
            self._dequeue()
            