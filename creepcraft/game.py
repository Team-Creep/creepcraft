from pyglet import image, app, font
from pyglet.gl import *
from pyglet.window import key, mouse 
import math

class Model:
    """Model class: world features of the game (block creation, block textures, add block method, and starter world)."""
    def __init__(self):
        """Constructs textures of a block and initializes starting landscape (starter world)"""
        # faces of block
        self.grass_top = self.get_tex('textures/grass_top.png') # pragma: no cover
        self.grass_side = self.get_tex('textures/grass_side.png') # pragma: no cover
        self.grass_bottom = self.get_tex('textures/grass_bottom.jpeg')
        self.dirt = self.get_tex('textures/dirt.png')
        self.dirt_grass = self.get_tex('textures/dirt_grass.png')
        self.stone = self.get_tex('textures/stone.png')
        self.batch = pyglet.graphics.Batch()
        self.current_world = {}
        self.player = Player()
        self.starter_world()

    def get_tex(self,file):
        """Takes in a file to create a texturized image with focus specification (makes less blurry - min & max(mag) filter)."""
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def add_block(self, x, y, z, texture):
        """Creates a single block with the specified texture."""
        position = x, y, z
        self.current_world[position] = texture

        # defines four 3D vertices of a cube
        # this position is right where the camera is facing -> does not show blocks when perspective is set (gluPerspective)
        # x,y,z = 0,0,0 & adjacent cubes (X, Y, Z)
        X, Y, Z = x+1, y+1, z+1

        # texture mapping (2 floats - 2D): http://www.glprogramming.com/red/chapter09.html
        # 2D tex coordinates: range from 0.0-1.0 in both directions
        tex_coords = ('t2f', (0,0, 1,0, 1,1, 0,1))

        # one single block:
        # back & front
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (X,y,z,  x,y,z,  x,Y,z,  X,Y,z)), tex_coords) 
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (x,y,Z,  X,y,Z,  X,Y,Z,  x,Y,Z)), tex_coords) 

        # left & right
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (x,y,z,  x,y,Z,  x,Y,Z,  x,Y,z)), tex_coords) 
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (X,y,Z,  X,y,z,  X,Y,z,  X,Y,Z)), tex_coords) 

        # bottom & right
        self.batch.add(4, GL_QUADS, texture[2], ('v3f', (x,y,z,  X,y,z,  X,y,Z,  x,y,Z)), tex_coords)  
        self.batch.add(4, GL_QUADS, texture[1], ('v3f', (x,Y,Z,  X,Y,Z,  X,Y,z,  x,Y,z)), tex_coords)  

    def remove_block(self, position):
        """Stretch goal: remove added block"""
        position = x,y,z 
        del self.current_world[position]

    def starter_world(self):
        """Add blocks for starter world (floor and border walls)"""
        GRASS = [self.grass_side, self.grass_top, self.grass_bottom]
        STONE = [self.stone, self.stone, self.stone]
        y = 0
        # floor
        for x in range(50):
            for z in range(50):
                self.add_block(x, y, z, GRASS)
                # border walls
                if x in range(1) or z in range(1):
                    for Y in range(0, 15):
                        self.add_block(x, Y, z, STONE)
                        self.add_block(49, Y, z, STONE)
                        self.add_block(x, Y, 49, STONE)

    def draw(self):
        """Actually draws (displays) on the window"""
        self.batch.draw()

class Player:
    """Player class: player features of the game (positioning, movement)
    """
    def __init__(self):
        # position - [0,0,0] coordinates don't show the world in the frame without movement 
        # shift coords so that players actually sees the world upon opening the window
        self.pos = [30,2,30]
        self.rot = [-15,0]

    def update(self,dt,keys):
        """Actually updates the player's current position based on 'dt' (ticks per second) and keys pressed. """
        slower = .1
        s = dt*10
        # pos[0]: x (left/right)
        # pos[2]: z (front/back)
        if keys[key.W]: # walk forward
            # 2 -> front limit
            if self.pos[2] >= 3:
                self.pos[2] -= 1*slower
        if keys[key.S]: # walk backwards
            if self.pos[2] <= 46:
                self.pos[2] += 1*slower
        if keys[key.A]: # left
            if self.pos[0] >= 1:
                self.pos[0] -= 1*slower
        if keys[key.D]: # right
            if self.pos[0] <= 48:
                self.pos[0] += 1*slower
        # pos[1]: y (up/down)
        if keys[key.SPACE]: # up
            # 6 -> jump limit
            if self.pos[1] <= 6:
                # self.pos[1] += s
                self.pos[1] += 1*slower
        if keys[key.LSHIFT]: # down
            # 2 -> floor limit
            if self.pos[1] >= 2:
                # self.pos[1] -= s
                self.pos[1] -= 1*slower

class Window(pyglet.window.Window):
    """Window Class: encompasses everything related to the actual game window."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logo = pyglet.image.load('assets/logo.png') 
        self.cloud = pyglet.image.load('textures/clouds.png') 
        # self.score_batch = pyglet.graphics.Batch()
        # self.score_label = pyglet.text.Label("Score: 0", font_name='Minecraft', font_size=9, x=0, y=18, batch=self.score_batch)
        # min size of window so it doesn't error out if user tries to make it too small
        self.set_minimum_size(400,300)
        # key state handler holds a bool value - https://pythonhosted.org/pyglet/api/pyglet.window.key.KeyStateHandler-class.html
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        # need scheduler for update to work
        # key press based on time of holding down key
        pyglet.clock.schedule(self.update)
        self.model = Model()
        self.player = Player()

    def Projection(self):
        """Defines the perspective (set between 2d and 3d) - in order to see the world."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        """Defines the perspective (set between 2d and 3d) - in order to see the world."""
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        """Sets 2 dimension perspective."""
        self.Projection()
        gluPerspective(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        """Sets 3 dimension perspective."""
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()

    def update(self, dt):
        """Updates key events from Player class (changing player position with movement controls)."""
        self.player.update(dt, self.keys)

    def on_key_press(self, symbol, modifiers):
        """Sets up keyboard shortcut to escape the game window."""
        if symbol == key.ESCAPE:
            self.close()

    def on_mouse_motion(self, x, y, dx, dy):
        # stretch goal
        # create method if we get to the point of adding rotation perspective
        pass

    def get_score(self):
        """Score counter (per blocks created). Starter world contains 5244 blocks."""
        starter = 5244
        current_blocks = len(self.model.current_world)
        current_score = current_blocks - starter
        return current_score

    def on_mouse_press(self, x, y, button, modifiers, batch=None):
        """Mouse controls for adding and removing blocks."""
        # https://pyglet.readthedocs.io/en/latest/programming_guide/mouse.html 
        # The x and y parameters give the coordinates of the mouse pointer, relative to the bottom-left corner of the window.
        DIRT_GRASS = [self.model.dirt, self.model.dirt_grass, self.model.grass_bottom]
        STONE = [self.model.stone, self.model.stone, self.model.stone]
        x,y,z = self.player.pos 
        if button == mouse.LEFT:
            # print("block created")
            # print(self.model.current_world[-1])
            self.model.add_block(x,y-1,z-3,DIRT_GRASS)
            print("player position: ", self.player.pos)
            els = list(self.model.current_world.items())
            print("block created at: ", els[-1])
            print("current score: ", self.get_score())
            # score = pyglet.sprite.Sprite(batch=self.score_batch)
        elif button == mouse.RIGHT:
            # position = x,y-1,z-3
            # if self.model.current_world[position]:
            #     self.model.remove_block(position)
            # # els = list(self.model.current_world.items())
            #     print("delete button clicked / player position: ", self.player.pos)
            # else:
            #     print("no blocks to remove")
            print("block deletion feature not ready")

    def collision(self, position):
        """stretch goal to check for player collision against blocks"""
        pass

    def on_draw(self):
        """Actually draws (displays) on the window"""
        self.clear()
        self.set3d()
        glColor3d(1, 1, 1)
        # rotation (skews the depth of the block)
        # glRotatef(-30,1,0,0)
        x,y,z = self.player.pos
        # move scene around to show individual cube/block
        # glTranslatef(0,0,-2)
        glTranslatef(-x,-y,-z)
        self.model.draw()
        # Images with an alpha channel can be blended with the existing framebuffer. To do this you need to supply OpenGL with a blend equation. 
        # https://pyglet.readthedocs.io/en/latest/programming_guide/image.html
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.logo.blit(5,6,2, width=40, height=8)
        self.cloud.blit(-14,16,4, width=15, height=5)
        self.cloud.blit(-12,20,12, width=18, height=12)
        self.cloud.blit(8,16,6, width=25, height=8)
        self.cloud.blit(16,20,8, width=35, height=10)
        self.cloud.blit(52,20,10, width=35, height=6)
        # self.get_score()
        # self.score_label.draw()
        # self.score_batch.draw()
        
def setup():
    """Sets the depth of images and sets the background color (sky)."""
    # # color codes: https://pemavirtualhub.wordpress.com/2016/06/20/opengl-color-codes/
    glClearColor(0.5, 0.69, 1.0, 1)
    glEnable(GL_DEPTH_TEST)

def main():
    """Creates a pyglet window and tells it to run the app."""
    window = Window(width=1000, height=800, caption='CREEPCRAFT',resizable=True)
    setup()
    pyglet.app.run()
    # get current window location
    # print(window.get_location())

if __name__ == '__main__':
    main()