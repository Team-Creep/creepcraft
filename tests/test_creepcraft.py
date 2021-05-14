import pytest
import pyglet
from pyglet import image, app, font
from pyglet.gl import *
from pyglet.window import key, mouse 
from creep.creepcraft.game import *

# command:
# pytest --cov

player = Player()

def test_player_pos():
    actual = player.pos
    expected = [30,2,30]
    assert actual == expected
    
def test_player_rot():
    actual = player.rot
    expected = [-15,0]
    assert actual == expected

def test_setup():
    actual = glClearColor(0.5, 0.69, 1.0, 1)
    expected = None
    assert actual == expected

def test_main_window_width():
    window = pyglet.window.Window()
    actual = window.width
    expected = 640
    assert actual == expected

def test_main_window_height():
    window = pyglet.window.Window()
    actual = window.height
    expected = 480
    assert actual == expected

def test_window_logo_image():
    logo = pyglet.image.load('creepcraft/assets/logo.png')
    actual = str(logo)
    expected = '<ImageData 866x144>'
    assert actual == expected

def test_window_cloud_image():
    cloud = pyglet.image.load('creepcraft/textures/clouds.png')
    actual = str(cloud)
    expected = '<ImageData 615x480>'
    assert actual == expected

def test_textures_dirt_grass():
    dirt_grass = pyglet.image.load('creepcraft/textures/dirt_grass.png')
    actual = str(dirt_grass)
    expected = '<ImageData 16x16>'
    assert actual == expected

def test_textures_dirt():
    dirt = pyglet.image.load('creepcraft/textures/dirt.png')
    actual = str(dirt)
    expected = '<ImageData 16x16>'
    assert actual == expected

def test_textures_grass_bottom():
    grass_bottom = pyglet.image.load('creepcraft/textures/grass_bottom.jpeg')
    actual = str(grass_bottom)
    expected = '<ImageData 16x16>'
    assert actual == expected

def test_textures_grass_side():
    grass_side = pyglet.image.load('creepcraft/textures/grass_side.png')
    actual = str(grass_side)
    expected = '<ImageData 16x16>'
    assert actual == expected

def test_textures_grass_top():
    grass_top = pyglet.image.load('creepcraft/textures/grass_top.png')
    actual = str(grass_top)
    expected = '<ImageData 16x16>'
    assert actual == expected

def test_textures_stone():
    stone = pyglet.image.load('creepcraft/textures/stone.png')
    actual = str(stone)
    expected = '<ImageData 16x16>'
    assert actual == expected