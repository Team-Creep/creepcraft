import pyglet
from pyglet.window import mouse, key, clock
import math 

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
        self.inventory = [brick, grass, sand]
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
        sector = sectorize(self.position)
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
        
    @window.event
    def on_mouse_press(self, x, y, button, modifiers):
        """Called when mouse is pressed. 1 is left button, 4 is right button. Provides user mod control (choose blocks from inventory by type)."""
        if self.exclusive:
            vector = self.line_of_sight()
            block, previous = self.model.

        if button == mouse.LEFT:
            pass
        if button == mouse.RIGHT:
            pass 


    @window.event
    def on_draw():
        window.clear()
        label.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        print('A key was pressed')


    # click escape while mouse hovers over window
    @window.event
    def on_key_press_exit(symbol, modifiers):
        if symbol == key.ESCAPE: # [ESC]
            alive = 0

    

