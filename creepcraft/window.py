# from creepcraft.game import cube_position
import pyglet
from pyglet import clock, app, image
from pyglet.window import mouse, key
import math 
# import sys

# TICKS_PER_SEC = 60
# WALKING_SPEED = 5
# FLYING_SPEED = 15
# GRAVITY = 20.0
# MAX_JUMP_HEIGHT = 1.0
# JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
# TERMINAL_VELOCITY = 50
# PLAYER_HEIGHT = 2

# if sys.version_info[0] >= 3:
#     xrange = range


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # controls whether window is capturing mouse
        self.exclusive = False
        self.fly = False
        # controls moving in the direction your facing
        self.strafe = [0,0]
        # specifies current position in the world using a tuple (y-axis)
        self.position = (0,0,0)
        # horizontal range (when player looks up/down)
        self.rotation = (0,0)
        # play space / sector
        self.sector = None
        self.crosshairs = None
        # set velocity and upward direction for flying (y-axis)
        self.dy = 0
        # block texture
        self.inventory = [BRICK, GRASS, SAND]
        # allows you to pick inventory space - which gets placed on the screen
        self.block = self.inventory[0]
        # key mapping (number keys)
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5, key._6, key._7, key._8, key._9, key._0]
        # handles world building - need to write out model
        self.model = Model()
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)

    def exclusive_mouse(self, exclusive):
        """If exclusive is True, it will capture mouse movements. If False, it won't."""
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def line_of_sight(self):
        """Returns the vector of where the player is looking."""
        x, y = self.rotation
        m = math.cos(math.radians(y))
        # vector points of the user
        dx = math.cos(math.radians(x - 90) * m)
        dy = math.sin(math.radians(y))
        dz = math.sin(math.radians(x - 90) * m)
        return (dx, dy, dz)

    def motion_vectors(self):
        """Returns the player motion."""
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.randians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    # moves backwards
                    dy *= -1 
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)
    
    def update(self, dt):
        """Change in time since the last call (per second)."""
        # model methods = process_queue(), change_sectors(), process_entire_queue()
        self.model.process_queue()
        sector = play_space(self.position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector == None:
                self.model.process_entire_queue()
            self.sector = sector 
        m = 8 # blocks that user can interact with (hit range)
        dt = min(dt, 0.2)
        for _ in xrange(m):
            self._update(dt / m)

    def _update(self, dt):
        """Private method with motion logic that deals with gravity and collision detection."""
        speed = FLYING_SPEED if self.fly else WALKING_SPEED
        # distance covered in each tick
        d = dt * speed
        # create new position in space before gravity
        dx, dy, dz = dx * d, dy * d, dx * d
        if not self.fly:
            self.dy -= dt * GRAVITY
            self.dy = max(self.dy, - TERMINAL_VELOCITY)
            # falling velocity
            dy += self.dy * dt
        # collisions
        x, y, z = self.position
        x, y, z = self.collide((x+dx, y+dy, z+dz), PLAYER_HEIGHT) 
        self.position = (x, y, z)

    def collisions(self, position, height):
        """Player at given position and height (flying). Position (tuple) checks for x, y, z. Height is the integer of the player."""
        # need to add: model method - world

        # buffer between user + landscape
        pad = 0.25
        p = list(position)
        # need to create normalize method to find position (if there is a block in that position)
        np = normalize(position)
        for face in FACES:
            for i in xrange(3):
                if not face[i]:
                    continue
                d = (p[i]-np[i]) * face[i]
                if d < pad:
                    continue
                for dy in xrange(height):
                    op = list(np)
                    op[1] += dy
                    op[i] += face[i]
                    if tuple(op) not in self.model.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        self.dy = 0
                    break
        return tuple(p)
        
    def on_mouse_press(self, x, y, button, modifiers):
        """Called when mouse is pressed. 1 is left button, 4 is right button. Provides user mod control (choose blocks from inventory by type)."""
        if self.exclusive:
            vector = self.line_of_sight()
            block, previous = self.model.find_block(self.position, vector)
            if (button == mouse.RIGHT) or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                if previous:
                    self.model.add_block(previous, self.block)
            elif button == pyglet.window.mouse.LEFT and block:
                texture = self.model.world[block]
                if texture != DIRT:
                    self.model.remove_block(block)
        else:
            self.exclusive_mouse(True)

    def on_mouse_movement(self, x, y, dx, dy):
        """[when user moves the mouse this is called]

        Args:
            x, y ([int]): [These are the coordinates of the mouse, always centered in line of sight]
            
            dx, dy ([type]): [coordinates of Where the mouse is moving]
        """
        if self.exclusive:
            m = 0.15
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)

    def key_press(self, symbol, modifiers):
        """[key mapping via pyglet docs. called when user uses keyboard]

        Args:
            symbol ([int]): [key that was pressed]
            modifiers ([int]): [key that was pressed and modified]
        """
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.SPACE:
            if self.dy == 0:
                self.dy = JUMP_SPEED
        elif symbol == key.ESCAPE:
            self.exclusive_mouse(False)
        elif symbol == key.TAB:
            self.flying = not self.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]


    # click escape while mouse hovers over window
    def key_release(self, symbol, modifiers):
        """[key mapping via pyglet docs. called when user releases key]

        Args:
            symbol ([int]): [key that was released]
            modifiers ([int]): [key that was released and modified]
        """
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1

    def screen_resize(self, width, height):
        """[resizes screen with new width and height]"""
        # if we use a lable we will use self.label.y = height -10
        if self.crosshairs:
            self.crosshairs.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.crosshairs = pyglet.graphics.vertex_list(4, ('v2i', (x - n, y, x, y-n, x, y + n)))

    def draw_2d(self):
        """[configure OpenGl to draw in 2d with pyglet]
        """
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw_3d(self):
        """[configure OpenGl to draw in 3d with pyglet]
        """
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        glTranslatef(-x, -y, -z)

    def focused_block(self):
        """[draws edges on block under crosshairs]
        """
        vector = self.line_of_sight()
        block = self.model.find_block(self.position, vector)[0]
        if block:
            x, y, z = block
            vertex_info = cube_position(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw(self):
        """[pyglet calls this to draw on canvas]
        """
        self.clear()
        self.draw_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.focused_block()
        self.draw_2d()
        self.draw_crosshairs()
        

