import pyglet
from pyglet.window import mouse
from pyglet.window import key

window = pyglet.window.Window()

label = pyglet.text.Label('Creep Craft',
                        font_name='Times New Roman',
                        font_size=36,
                        x=window.width//2, y=window.height//2,
                        anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    label.draw()

@window.event
def on_key_press(symbol, modifiers):
    print('A key was pressed')

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print('The left mouse button was pressed.')

# need window class for exit command
@window.event
def on_key_press_exit(symbol, modifiers):
    if symbol == key.ESCAPE: # [ESC]
        alive = 0

pyglet.app.run()