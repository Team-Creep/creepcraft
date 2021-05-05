# main game logic (move / jump / place blocks / tally score points)

# other, create cubes, get textures, some used by both window class and model


# When we get a file of textures, these coords point to the spot in the picture we are pulling from. 
# TEXTURE_PATH = '.png of textures here'
# GRASS = texture_position((1, 0), (0,1), (0, 0))
# STONE = texture_position((1, 0), (0,1), (0, 0))
# DIRT = texture_position((1, 0), (0,1), (0, 0))

PLAY_SPACE_SIZE = 16
FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

def cube_position(x, y, z, n):
    """[return verticies of cube, n references window size. Each row is a side of the cube, with three verticies pointing to the corners of that side.]

    Args:
        x ([int]): [description]
        y ([int]): [description]
        z ([int]): [description]
        n ([int]): [description]
    """
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
    ]

def texture_position(x, y, n=4):
    """[return verticies of texture square]"""
    pass

def texture_list(top, bottom, side):
    """[return a list of the texture squares]

    Args:
        top ([type]): [description]
        bottom ([type]): [description]
        side ([type]): [description]
    """
    pass

def normalize(position):
    """[takes in the position, rounds each verticie, and returns block in that position]

    Args:
        position ([int]): [tuple length of three]
    """
    pass

def play_space(position):
    """[returns tuple the given position in in]

    Args:
        position ([position]): [tuple length of three]
        returns ([sector]): [tuple length of three]
    """
    pass

def set_up():
    """[Basic OpenGL configuration to run game]
    """
    # set color of the sky
    glClearColor(0.5, 0.69, 1.0, 1)
    # stop render of cubes the user can't see
    glEnable(GL_CULL_FACE)
    # GL_NEAREST
    # "is generally faster than GL_LINEAR, but it can produce textured images
    # with sharper edges because the transition between texture elements is not
    # as smooth."
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # call fog() here if we write this!

def main():
    window = Window(width=800, height=600, caption='Pyglet', resizable=True)
    # Hide the mouse cursor and it can't leave window.
    window.set_exclusive_mouse(True)
    set_up()
    pyglet.app.run()


if __name__ == '__main__':
    main()
