from pyglet import image, app
from pyglet.gl import *
from pyglet.window import key, mouse 
import math

class Model:

    def get_tex(self,file):
        tex = pyglet.image.load(file).get_texture()
        # fixes the pixelation of the block face (makes less blurry - min&max filter)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def add_block(self,x,y,z):
        # defines four 3D vertices of a cube
        # this position is right where the camera is facing -> does not show blocks when perspective is set (gluPerspective)
        # x,y,z = 0,0,0
        # get adjacent cubes (X, Y, Z)
        X, Y, Z = x+1, y+1, z+1

        # texture mapping (2 floats - 2D): http://www.glprogramming.com/red/chapter09.html
        # 2D tex coordinates: range from 0.0-1.0 in both directions
        # square tex coordinates: (0, 0), (1, 0), (1, 1), and (0, 1)
        tex_coords = ('t2f', (0,0, 1,0, 1,1, 0,1))

        # one single block:
        # back & front
        self.batch.add(4, GL_QUADS, self.side,   ('v3f', (X,y,z,  x,y,z,  x,Y,z,  X,Y,z)), tex_coords) 
        self.batch.add(4, GL_QUADS, self.side,   ('v3f', (x,y,Z,  X,y,Z,  X,Y,Z,  x,Y,Z)), tex_coords) 

        # left & right
        self.batch.add(4, GL_QUADS, self.side,   ('v3f', (x,y,z,  x,y,Z,  x,Y,Z,  x,Y,z)), tex_coords) 
        self.batch.add(4, GL_QUADS, self.side,   ('v3f', (X,y,Z,  X,y,z,  X,Y,z,  X,Y,Z)), tex_coords) 

        # bottom & right
        self.batch.add(4, GL_QUADS, self.bottom, ('v3f', (x,y,z,  X,y,z,  X,y,Z,  x,y,Z)), tex_coords)  
        self.batch.add(4, GL_QUADS, self.top, ('v3f', (x,Y,Z,  X,Y,Z,  X,Y,z,  x,Y,z)), tex_coords)  

    def world(self):
        for x in range(50):
            for y in range(50):
                self.add_block(x, 0, y)

    def __init__(self):
        # faces of a single block
        self.top = self.get_tex('textures/grass_top.png')
        self.side = self.get_tex('textures/grass_side.png')
        self.bottom = self.get_tex('textures/dirt.png')

        self.batch = pyglet.graphics.Batch()
        self.world()

    def draw(self):
        self.batch.draw()

class Player:
    def __init__(self):
        # position - 0,0,0 coordinates don't show the world in the frame without movement 
        # shift coords so that players actually sees the world upon opening the window
        # self.pos = [0,0,0]
        # self.rot = [0,0]
        self.pos = [1,2,2]
        self.rot = [-15,0]

    def update(self,dt,keys):
        """Actually updates the window based on 'dt' (ticks per second)"""
        slower = 0.2
        s = dt*10
        rotY = -self.rot[1]/180*math.pi
        # dx,dy are used to change the position of the player within the world 
        # key handler - if key pressed is True, change position
        dx, dz = s*math.sin(rotY), math.cos(rotY)
        # pos[0]: x, pos[2]: z
        if keys[key.W]: # walk forward
            self.pos[0] += dx*slower
            self.pos[2] -= dz*slower
        if keys[key.S]: # walk backwards
            self.pos[0] -= dx*slower
            self.pos[2] += dz*slower
        if keys[key.A]: # left
            self.pos[0] -= dz*slower
            self.pos[2] -= dx*slower
        if keys[key.D]: # right
            self.pos[0] += dz*slower
            self.pos[2] += dx*slower
        # pos[1]: y (up/down)
        if keys[key.SPACE]: # up
            self.pos[1] += s
        if keys[key.LSHIFT]: # down
            self.pos[1] -= s

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #logo
        self.logo_image = pyglet.image.load('logo.png')
        self.logo = pyglet.sprite.Sprite(self.logo_image, x=70, y=650)
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

    # define the perspective (set between 2d and 3d) - in order to see the world
    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        self.Projection()
        gluPerspective(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()

    def on_key_press(self, KEY, _MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock

    def update(self, dt):
        # updates key events from Player class (changing player position with movement controls)
        self.player.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.logo.draw()
        glColor3d(1, 1, 1)
        # rotation (skews the depth of the block)
        # glRotatef(-30,1,0,0)
        x,y,z = self.player.pos
        # move scene around to show individual cube/block
        # glTranslatef(0,0,-2)
        glTranslatef(-x,-y,-z)
        self.model.draw()

def setup():
    # # color codes: https://pemavirtualhub.wordpress.com/2016/06/20/opengl-color-codes/
    glClearColor(0.5, 0.69, 1.0, 1)
    glEnable(GL_DEPTH_TEST)

def main():
    window = Window(width=1000, height=800, caption='CREEPCRAFT',resizable=True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main()