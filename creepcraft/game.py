from pyglet import image, app
from pyglet.gl import *
from pyglet.window import key, mouse 
import math

class Model:
    def __init__(self):
        # faces of block
        self.grass_top = self.get_tex('textures/grass_top.png')
        self.grass_side = self.get_tex('textures/grass_side.png')
        self.grass_bottom = self.get_tex('textures/dirt.jpeg')
        self.stone = self.get_tex('textures/stone.png')
        self.batch = pyglet.graphics.Batch()
        self.current_world = {}
        self.player = Player()
        self.starter_world()

    def get_tex(self,file):
        tex = pyglet.image.load(file).get_texture()
        # fixes the pixelation of the block face (makes less blurry - min&max filter)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def add_block(self, x, y, z, texture):
        # self.current_world[(x,y,z)] = self.player.pos

        # need to do: add texture parameter to specify which type of block

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
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (X,y,z,  x,y,z,  x,Y,z,  X,Y,z)), tex_coords) 
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (x,y,Z,  X,y,Z,  X,Y,Z,  x,Y,Z)), tex_coords) 

        # left & right
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (x,y,z,  x,y,Z,  x,Y,Z,  x,Y,z)), tex_coords) 
        self.batch.add(4, GL_QUADS, texture[0], ('v3f', (X,y,Z,  X,y,z,  X,Y,z,  X,Y,Z)), tex_coords) 

        # bottom & right
        self.batch.add(4, GL_QUADS, texture[2], ('v3f', (x,y,z,  X,y,z,  X,y,Z,  x,y,Z)), tex_coords)  
        self.batch.add(4, GL_QUADS, texture[1], ('v3f', (x,Y,Z,  X,Y,Z,  X,Y,z,  x,Y,z)), tex_coords)  

    def remove_block(self, x, y, z):
        # del self.current_world[(x,y-1,z-3)]
        pass

    def starter_world(self):
        GRASS = [self.grass_side, self.grass_top, self.grass_bottom]
        STONE = [self.stone, self.stone, self.stone]
        y = 0
        # floor
        for x in range(50):
            for z in range(50):
                self.add_block(x, y, z, GRASS)
                if x in range(1) or z in range(1):
                    for Y in range(0, 15):
                        self.add_block(x, Y, z, STONE)
                        self.add_block(49, Y, z, STONE)
                        self.add_block(x, Y, 49, STONE)

    def draw(self):
        self.batch.draw()

class Player:
    def __init__(self):
        # position - 0,0,0 coordinates don't show the world in the frame without movement 
        # shift coords so that players actually sees the world upon opening the window
        # self.pos = [0,0,0]
        # self.rot = [0,0]
        self.pos = [30,2,30]
        self.rot = [-15,0]

    def update(self,dt,keys):
        """Actually updates the window based on 'dt' (ticks per second)"""
        slower = .5
        s = dt*10
        rotY = -self.rot[1]/180*math.pi
        # dx,dy are the velocity used to change the position of the player within the world 
        # key handler - if key pressed is True, change position
        dx, dz = s*math.sin(rotY), s*math.cos(rotY)
        # pos[0]: x (left/right)
        # pos[2]: z (front/back)
        if keys[key.W]: # walk forward
            # 2 -> front limit
            if self.pos[2] >= 2:
                self.pos[0] += dx*slower
                self.pos[2] -= dz*slower
        if keys[key.S]: # walk backwards
            if self.pos[2] <= 49:
                self.pos[0] -= dx*slower
                self.pos[2] += dz*slower
        if keys[key.A]: # left
            if self.pos[0] >= 2:
                self.pos[0] -= dz*slower
                self.pos[2] -= dx*slower
        if keys[key.D]: # right
            if self.pos[0] <= 48:
                self.pos[0] += dz*slower
                self.pos[2] += dx*slower
        # pos[1]: y (up/down)
        if keys[key.SPACE]: # up
            # 6 -> jump limit
            if self.pos[1] <= 6:
                self.pos[1] += s
        if keys[key.LSHIFT]: # down
            # 2 -> floor limit
            if self.pos[1] >= 2:
                self.pos[1] -= s

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logo = pyglet.image.load('logo.png')
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

    def update(self, dt):
        # updates key events from Player class (changing player position with movement controls)
        self.player.update(dt, self.keys)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.close()

    def on_mouse_motion(self, x, y, dx, dy):
        # stretch goal
        # create method if we get to the point of adding rotation perspective
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        # https://pyglet.readthedocs.io/en/latest/programming_guide/mouse.html 
        # The x and y parameters give the coordinates of the mouse pointer, relative to the bottom-left corner of the window.
        x,y,z = self.player.pos 
        GRASS = [self.model.grass_side, self.model.grass_top, self.model.grass_bottom]
        STONE = [self.model.stone, self.model.stone, self.model.stone]
        if button == mouse.RIGHT:
            print("right button clicked")
            self.model.remove_block(x,y,z)
            # print("block deleted")
        elif button == mouse.LEFT:
            print("block created")
            self.model.add_block(x,y-1,z-3,GRASS)

    def collision(self, position):
        pass

    def on_draw(self):
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
        
def setup():
    # # color codes: https://pemavirtualhub.wordpress.com/2016/06/20/opengl-color-codes/
    glClearColor(0.5, 0.69, 1.0, 1)
    glEnable(GL_DEPTH_TEST)

def main():
    window = Window(width=1000, height=800, caption='CREEPCRAFT',resizable=True)
    setup()
    pyglet.app.run()
    # get current window location
    print(window.get_location())

if __name__ == '__main__':
    main()