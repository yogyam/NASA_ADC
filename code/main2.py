from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from terrain1 import *



app = Ursina()

# Make a simple game so we have something to test with
default_pos = (0,250,0)
#keep it slightly more than dataset
lunar_scale=(6600,0,6600)
lunar_initial_pos = (0, 150, 0) 

Entity(model=Terrain1(heightmap="heightmap.png"),
                      texture="texture2",
                      collider='mesh',
                      enabled=False,
                      scale=(6400,2,6400),
                      position= lunar_initial_pos)


e = Entity(model='sphere')



def update():
    walking = held_keys['a'] or \
        held_keys['d'] or \
        held_keys['w'] or \
        held_keys['s']


def input(key):
    if key == 'p':
      printCoordinates()
    if key == 'q' or key == 'esc':
      quit()
    if key == 'm':
        player.enabled = False
        mouse.visible = True


player = FirstPersonController(position = default_pos)
player.cursor.visible = False
player.gravity = False
app.run()