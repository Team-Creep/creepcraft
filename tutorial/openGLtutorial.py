# https://www.youtube.com/watch?v=Hqg4qePJV2U
# import pyglet
from pyglet.gl import * # auto imports pyglet
from pyglet.window import key
import math

# for 3D
class Model:
    def get_tex(self, file):
        tex = pyglet.image.load(file).get_texture()
        # fix blurry block face (max and min)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        # # color 3 floats
        # color = ('c3f', (1,1,1)*4)

        # need tex (texture) coordinates instead of color
        # 2 floats (2D)
        # default coord (0,0) -> bottom left
        tex_coords = ('t2f', (0,0, 1,0, 1,1, 0,1,))

        # define four 3D vertices of a cube
        # this position is right where the camera is facing -> does not show blocks when perspective is set (gluPerspective)
        # x,y,z = 0,0,0
        # one space forward (to see block):
        x,y,z = 0,0,-1
        # get adjacent cubes
        X,Y,Z = x+1,y+1,z+1

        self.top = self.get_tex('grass_top.png')
        self.side = self.get_tex('grass_side.png')
        self.bottom = self.get_tex('dirt.png')

        # 4: quad is a face with 4 points & also it's the number of vertices that will be inputted (starting arg: 4)
        # GL_QUADS: the type of rendering (triangles, lines, polygons also available - need use with appropriate data)
        # self.side: binds texture to the face
        # v3f: vertex 3 floats (3 dimensions) -> 2 dimension would be v2f
        # last arg fills in the positions
        # self.batch.add(4,GL_QUADS,self.side,('v3f',(x,y,z, X,y,z, X,Y,z, x,Y,z)), color)
        # change to tex_coord
        # will be moved to add_block function later
        self.batch.add(4,GL_QUADS,self.side,('v3f',(x,y,z, X,y,z, X,Y,z, x,Y,z)), tex_coords)

    def draw(self):
        self.batch.draw()

class Player:
    def __init__(self):
        # position
        self.pos = [0,0,0]
        # rotation
        self.rot = [0,0]

    def mouse_motion(self, dx, dy):
        dx/= 8
        dy/= 8
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0]>90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    def update(self, dt, keys):
        # if keys[key.A]: print('a')
        # registers key press with print statements (dated attributes on key press method)
        s = dt*10
        rotY = self.rot[1]/180*math.pi
        dx,dz = s*math.sin(rotY), s*math.cos(rotY)
        # key handler - if key pressed is True, change position
        if keys[key.W]: 
            self.pos[0]+=dx 
            self.pos[2]-=dz
            print('w')
        if keys[key.S]: 
            self.pos[0]-=dx 
            self.pos[2]+=dz
            print('s')
        if keys[key.A]: 
            self.pos[0]-=dz 
            self.pos[2]-=dx
            print('a')
        if keys[key.D]: 
            self.pos[0]+=dz 
            self.pos[2]+=dx
            print('d')
        if keys[key.SPACE]:
            self.pos[1]+=s
            print('space')
        if keys[key.LSHIFT]:
            self.pos[1]-=s
            print('lshift')

# for the actual window
class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300, 200)
        self.model = Model()
        self.player = Player()
        # key state handler holds a bool value - https://pythonhosted.org/pyglet/api/pyglet.window.key.KeyStateHandler-class.html
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        # need scheduler for update to work
        # key press based on time of holding down key
        pyglet.clock.schedule(self.update)

    # define the perspective (set between 2d and 3d) - in order to see the wall
    def Projection(self): 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self): 
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def set3d(self):
        self.Projection()
        # perspective
        # 70: field of view (fov)
        # width/height = aspect ratio
        # .05 min render distance & 1000 max render distance
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()
        self.player = Player()

    def set2d(self): 
        self.Projection()
        # 2D perspective
        gluOrtho2D(0, self.width, 0, self.height)
        self.Model()
    
    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self:self.lock, setLock)

    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    # def on_key_press(self, symbol, modifiers):
    def on_key_press(self, KEY, MOD):
        # prints out unicode for corresponding key pressed
        # print(KEY)
        # prints A when A is pressed
        # if KEY == key.A: print('A')
        if KEY == key.ESCAPE: self.close()
        # lock mouse to play / unlock to escape window
        elif KEY == key.E: self.mouse_lock = not self.mouse_lock

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_draw(self):
        # color set by glClearColor
        self.clear()
        self.set3d()
        # rotation (skews the depth of the block)
        # glRotatef(-30,1,0,0)
        x,y,z = self.player.pos
        # move scene around to show individual cube/block
        # glTranslatef(0,0,-2)
        glTranslatef(-x,-y,-z)
        self.model.draw()


if __name__ == "__main__":
    window = Window(width=400, height=300, caption="G's world", resizable=True)
    # color codes: https://pemavirtualhub.wordpress.com/2016/06/20/opengl-color-codes/
    glClearColor(0.5,.7,1,1)
    pyglet.app.run()