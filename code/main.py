#References
#Procedural terrain creation using height_map - https://github.com/pokepetter/ursina/blob/master/ursina/models/procedural/terrain.py
##https://github.com/pokepetter/ursina/blob/master/ursina/models/procedural/circle.py
#Options - 

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from helper import Helper



app = Ursina()

# Boolean flags to track direction changes for each key
direction_changed = {'w': False, 'a': False, 's': False, 'd': False}
regen_x_min, regen_x_max = -3300, 3300
regen_z_min, regen_z_max = -3700, 3200

count = 1
default_pos = (0,250,0)
#keep it slightly more than dataset
lunar_scale=(6400,130,6400)
#lunar_scale=(20,5,20)
lunar_initial_pos = (10, 40, 10) 
#lunar_initial_pos = (0, 40, 0) 

# SLOPEMAPS = ['pns_slopemap_small.png', 
#                   'pns_slopemap_colorkey.png' , 
#                   'pns_slopemap_texture.png']

# HEIGHTMAPS = ['pns_heightmap_small.png', 
#                   'pns_heightmap_colorkey.png' , 
#                   'pns_heightmap_texture.png']

# ELEVATIONMAPS = ['pns_elevationmap_small.png', 
#                   'pns_elevationmap_colorkey.png' , 
#                   'pns_elevationmap_texture.png']

# AZIMUTHMAPS = ['pns_azimuthmap_small.png', 
#                   'pns_azimuthmap_colorkey.png' , 
#                   'pns_azimuthmap_texture.png']


SLOPEMAPS = ['fra_slopemap_small.png', 
                  'fra_slopemap_colorkey.png' , 
                  'fra_slopemap_texture.png']

HEIGHTMAPS = ['fra_heightmap_small.png', 
                  'fra_heightmap_colorkey.png' , 
                  'fra_heightmap_texture.png']

ELEVATIONMAPS = ['fra_elevationmap_small.png', 
                  'fra_elevationmap_colorkey.png' , 
                  'fra_elevationmap_texture.png']

AZIMUTHMAPS = ['fra_azimuthmap_small.png', 
                  'fra_azimuthmap_colorkey.png' , 
                  'fra_azimuthmap_texture.png']

OPTIONS = ['HEIGHT', 'SLOPE', 'ELEVATION', 'AZIMUTH', 'PATHFINDING']
lunar_model, color_key = None, None

slope = {15: True, 20: False}
destination = {1: True, 2: False, 3: False, 4: False}
path = {'shortest': True, 'lhc': False}
comm = True

info_helper = Helper()


player = FirstPersonController(gravity=0, 
                                position = default_pos,
                                speed = 320, 
                                enabled = True)
camera.z = -8

boxes_x = -0.6
boxes_y = 0.35
x_add = 0.1
x_shift = 0.05
# player = FirstPersonController(
#     model='cube',
#     color=color.azure,
#   collider='box',
#   position = (0,200,0),
#   speed = 100,
#   enabled = True
# )
player.cursor.visible = False
# player.gravity = False

def create_player():
    player = FirstPersonController()
    player.collider = 'box'
    player.enabled = True
    player.gravity = 0.0
    player.position = (0,200,0)
    return player

def generate_plane():
    plane = Entity(model='plane', parent='camera.ui')
    return plane


# def generate_terrain():
#     new_terrain = Entity(model=Terrain(heightmap="heightmap"),
#                           texture="texture2",
#                           collider='mesh',
#                           enabled=True,
#                           scale=lunar_scale,
#                           position= lunar_initial_pos,
#                           parent=plane)
#     return new_terrain


def generate_terrain(heightmap, texture):
    new_terrain = Entity(model=Terrain(heightmap=heightmap),
                          texture=texture,
                          collider='mesh',
                          enabled=True,
                          scale=lunar_scale,
                          position= lunar_initial_pos,
                          parent=plane,
                          name = 'lunar_model')
    new_terrain.rotation_y = 20
    return new_terrain

# def generate_slope_terrain():
#     new_terrain = Entity(model=Terrain(heightmap=SLOPEMAPS[0]),
#                           texture=SLOPEMAPS[2],
#                           collider='mesh',
#                           enabled=False,
#                           scale=lunar_scale,
#                           position= lunar_initial_pos,
#                           parent=plane)
#     return new_terrain

def update_terrain():
    new_terrain = Entity(model=Terrain(heightmap="pns_heightmap_256.png"),
                          texture="texture3.png",
                          collider='mesh',
                          enabled =False,
                          scale=lunar_scale,
                          position = (60, 0.8, 23),
                          parent=plane)
    return new_terrain

def generateEditorCamera(self):
    pass
    #self.camera.look_at(self.lunar)


def create_mini_map():
    mini_map = Entity(
    model='quad',
    parent=camera.ui,
    origin=(0,0),
    color=color.white,
    texture=HEIGHTMAPS[2],
    enabled=True,
    scale=(0.21, 0.21, 0.21),  # Adjust width and height here
    position=(boxes_x + x_add + 0.3, boxes_y, 2.0)
    )  # Ensure the box appears in front of other objects
    
    return mini_map

def create_rover():
    #Create the Visualization
    rover = Entity(model= 'rover4',
                   #texture='14014_Moon_Rover_Camcorder_diff',
                   texture='rover-bg4',
                    parent=player,
                    position = (0, -1.25, 0.01),
                    collider= 'box',
                    scale=(0.006,0.006,0.006))
    rover.rotation_setter((0, -90, 0))
    return rover

def create_mini_dot():
    mini_dot = Entity(
        model= 'sphere',
        color=color.pink,
        parent=mini_map,
        origin=(0,0),
        collider= 'box',
        scale=(0.04,0.04,0.04),
        position= (0.459, 0.459, -1.0),
        #position= (-0.459, 0.459, -1.0),
        enabled=True
    )  # Ensure the box appears in front of other objects
    
    return mini_dot

def update_mini_dot_position(x,y):
    mini_dot_pos, reset = info_helper.get_mini_dot_location(x,y)
    mini_dot.position = mini_dot_pos
    #print(mini_dot.position)
    return reset

def rotate_rover(direction_changed):
    if held_keys['w'] and not direction_changed['w']:
        rover.rotation_y = 90
        direction_changed = {'w': True, 'a': False, 's': False, 'd': False}
        
    
    if held_keys['d'] and not direction_changed['d']:
        rover.rotation_y = 0
        direction_changed = {'w': False, 'a': False, 's': False, 'd': True}
        
    if held_keys['s'] and not direction_changed['s']:
        rover.rotation_y = -90
        direction_changed = {'w': False, 'a': False, 's': True, 'd': False}
        
    if held_keys['a'] and not direction_changed['a']:
        rover.rotation_y = -180
        direction_changed = {'w': False, 'a': True, 's': False, 'd': False}
        
def update_rover_location(x,y):
    mini_dot_pos, reset = info_helper.get_mini_dot_location(x,y)
    mini_dot.position = mini_dot_pos
    #print(mini_dot.position)
    return reset

def create_info_box():
    info_box = Entity(
    model='quad',
    parent=camera.ui,
    origin=(0,0),
    color=color.blue,
    enabled=True,
    scale=(0.21, 0.21, 0.21),  # Adjust width and height here
    position=(boxes_x, boxes_y, 2.0)
    )  # Ensure the box appears in front of other objects
    
    return info_box

def create_info_text():
    y_loc = -0.1
    x_loc = -0.1
    info_text = Text(text="Information",
          parent=info_box,
          position=(-0.47, 0.45, -1),
          color=color.white,
          scale=3.0)
    
    # rover_text = Text(text = "Rover Coordinates",
    #                   origin=(0,0),
    #                     parent=info_box,
    #                     position=(-0.1, 0.25, -1),
    #                     scale=2.0,
    #                     color=color.white,
    #                     enabled=False)
    
    lat_text = Text(text = 'Latitude: 0 °North',
        origin=(0,0),
          parent=info_box,
          position=(-0.1, 0.25, -1),
          scale=2.5,
          color=color.white)
    
    lon_text = Text(text = 'Longitude: 0 °East',
        origin=(0,0),
          parent=info_box,
          position=(x_loc, lat_text.y + y_loc, -1),
          scale=2.5,
          color=color.white)
    height_text = Text(text = 'Height: ',
        origin=(0,0),
          parent=info_box,
          position=(x_loc, lon_text.y + y_loc, -1),
          scale=2.5,
          color=color.white)
    slope_text = Text(text = 'Slope:',
        origin=(0,0),
          parent=info_box,
          position=(x_loc, height_text.y + y_loc, -1),
          scale=2.5,
          color=color.white)
    elevation_text = Text(text = 'Elevation:',
        origin=(0,0),
          parent=info_box,
          position=(x_loc + 0.08, slope_text.y + y_loc, -1),
          scale=2.5,
          color=color.white)
    azimuth_text = Text(text = 'Azimuth:',
        origin=(0,0),
          parent=info_box,
          position=(x_loc + 0.08, elevation_text.y + y_loc, -1),
          scale=2.5,
          color=color.white)
    rover_text = Text(text = '',
        origin=(0,0),
          parent=info_box,
          position=(x_loc + 0.08, azimuth_text.y + y_loc, -1),
          scale=2.5,
          color=color.white)
    
         
    return lat_text, lon_text, height_text, slope_text, elevation_text, azimuth_text, rover_text 

def create_toggle_box():
    toggle_box = Entity(
              parent=camera.ui,
              model='quad',
              origin=(0,0),
              position=(boxes_x + x_add + 0.095, boxes_y, -2.4),
              color=color.red,
              scale=(0.21, 0.21, 0.2))
            
    return toggle_box

def create_toggles():
    toggle_text = Text(text="~ Toggles ~",
          parent=toggle_box,
          position=(-0.45, 0.45, -1),
          color=color.white,
          scale=2.7)
    
    # Height
    toggle_height = Button( 
                            radius=0.3,
                            scale=(0.22,0.1), 
                            position=(-0.37, 0.3, -1),
                            text='Height',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box)
    
    toggle_height.text_size_setter(0.5)
    toggle_height.on_click = gameplay_height
    
    #Slope
    toggle_slope = Button( 
                            radius=0.3,
                            scale=(0.2,0.1), 
                            position=(-0.14, 0.3, -1),
                            text='Slope',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box)
    
    toggle_slope.text_size_setter(0.45)
    toggle_slope.on_click = gameplay_slope
    
    #Elevation
    toggle_elevation = Button( 
                            radius=0.3,
                            scale=(0.27,0.1), 
                            position=(0.11, 0.3, -1),
                            text='Elevation',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box)
    
    toggle_elevation.text_size_setter(0.45)
    toggle_elevation.on_click = gameplay_elevation
    
    #Azimuth
    toggle_azimuth = Button( 
                            radius=0.3,
                            scale=(0.23,0.1), 
                            position=(0.38, 0.3, -1),
                            text='Azimuth',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box)
    
    toggle_azimuth.text_size_setter(0.45)
    toggle_azimuth.on_click = gameplay_azimuth
    
         
    return toggle_text

def set_slope(_slope):
    global slope
    if(_slope==15):
        slope_option_15.color_setter(color.black)
        slope_option_20.color_setter(color.blue)
        slope = {15: True, 20: False}
        
    if(_slope==20):
        slope_option_15.color_setter(color.blue)
        slope_option_20.color_setter(color.black)
        slope = {15: False, 20: True}
    
        
def set_destination(_dest):
    global destination
    #print("destination =", _dest)
    destination_option_1.color_setter(color.blue)
    destination_option_2.color_setter(color.blue)
    destination_option_3.color_setter(color.blue)
    destination_option_4.color_setter(color.blue)
    
    if(_dest==1):
        destination = {1: True, 2: False, 3: False, 4: False}
        destination_option_1.color_setter(color.black)
       
        
    if(_dest==2):
        destination = {1: False, 2: True, 3: False, 4: False}
        destination_option_2.color_setter(color.black)
        
    if(_dest==3):
        destination = {1: False, 2: False, 3: True, 4: False}
        destination_option_3.color_setter(color.black)
       
        
    if(_dest==4):
        destination = {1: False, 2: False, 3: False, 4: True}
        destination_option_4.color_setter(color.black)
    
    return destination
        
def set_path(_path):
    global path
    pathchoice_shortest.color_setter(color.blue)
    pathchoice_lhc.color_setter(color.blue)
    
    path = {'shortest': True, 'lhc': False}
    if(_path=='shortest'):
        path = {'shortest': True, 'lhc': False}
        pathchoice_shortest.color_setter(color.black)
       
    if(_path=='lhc'):
        path = {'shortest': False, 'lhc': True}
        pathchoice_lhc.color_setter(color.black)
    
        
def set_comm(_comm):
    global comm
    comm_yes.color_setter(color.blue)
    comm_no.color_setter(color.blue)
    
    if(_comm):
        comm = True
        comm_yes.color_setter(color.black)
       
    else:
        comm = False
        comm_no.color_setter(color.black)
    
        
def create_pathfinding_options():
    pathfinding_text = Text(text="~ Path Finding ~",
          parent=toggle_box,
          position=(-0.45, 0.22, -1),
          color=color.white,
          scale=2.7)
    
    y_loc = -0.1
    y_loc_button = -0.125
    x_loc = 0.3
    e = -0.009
    
    ## Add Slope Options
    slope_text = Text(text="Slope:",
          parent=toggle_box,
          position=(-0.45, pathfinding_text.y + y_loc, -1),
          color=color.white,
          scale=2.5)
    
    slope_option_15 = Button( 
                            radius=0.3,
                            scale=(0.1,0.1), 
                            position=(slope_text.x + x_loc, pathfinding_text.y + y_loc_button, -1),
                            text='15',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box,
                            enabled=True)
    
    slope_option_15.text_size_setter(0.45)
    
    slope_option_20 = Button( 
                            radius=0.3,
                            scale=(0.1,0.1), 
                            position=(slope_text.x + (x_loc*1.5), pathfinding_text.y + y_loc_button, -1),
                            text='20',
                            color=color.blue, 
                            text_color=color.white,
                            pressed_color=color.black,
                            parent=toggle_box)
    
    slope_option_20.text_size_setter(0.45)
    
    slope_option_15.on_click = Func(set_slope,15)
    slope_option_20.on_click = Func(set_slope,20)
    
        ## Add Destinations
    destination_text = Text(text="Destination:",
          parent=toggle_box,
          position=(-0.45, slope_text.y + y_loc, -1),
          color=color.white,
          scale=2.5)
    
    destination_option_1 = Button( 
                            radius=0.3,
                            scale=(0.1,0.1), 
                            position=(destination_text.x + 0.45, slope_option_20.y + y_loc + e, -1),
                            text='1',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box)
    
    destination_option_1.text_size_setter(0.45)
     
    destination_option_2 = Button( 
                            radius=0.3,
                            scale=(0.1,0.1), 
                            position=(destination_option_1.x + 0.14, slope_option_20.y + y_loc + e, -1),
                            text='2',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box)
    
    destination_option_2.text_size_setter(0.45)
    
    destination_option_3 = Button( 
                            radius=0.3,
                            scale=(0.1,0.1), 
                            position=(destination_option_2.x + 0.14, slope_option_20.y + y_loc + e, -1),
                            text='3',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box)
    
    destination_option_3.text_size_setter(0.45)
    
    destination_option_4 = Button( 
                            radius=0.3,
                            scale=(0.1,0.1), 
                            position=(destination_option_3.x + 0.14, slope_option_20.y + y_loc + e, -1),
                            text='4',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box)
    
    destination_option_4.text_size_setter(0.45)
    
    destination_option_1.on_click = Func(set_destination,1)
    destination_option_2.on_click = Func(set_destination,2)
    destination_option_3.on_click = Func(set_destination,3)
    destination_option_4.on_click = Func(set_destination,4)
    
    
    ## Add Choice of Path
    pathchoice_text = Text(text="Path Choice:",
          parent=toggle_box,
          position=(-0.45, destination_text.y + y_loc + e, -1),
          color=color.white,
          scale=2.5)
    pathchoice_shortest = Button( 
                            radius=0.3,
                            scale=(0.25,0.1), 
                            position=(pathchoice_text.x + x_loc*1.8, destination_option_4.y + y_loc + e, -1),
                            text='Shortest',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box)
    
    pathchoice_shortest.text_size_setter(0.45)
    
    pathchoice_lhc = Button( 
                            radius=0.3,
                            scale=(0.2,0.1), 
                            position=(pathchoice_shortest.x + x_loc, destination_option_4.y + y_loc + e, -1),
                            text='LHC',
                            color=color.blue, 
                            text_color=color.white,
                            parent=toggle_box)
    
    pathchoice_lhc.text_size_setter(0.45)
    
    
    pathchoice_shortest.on_click = Func(set_path,'shortest')
    pathchoice_lhc.on_click =  Func(set_path,'lhc')


    
    ## Add communication options
    comm_text = Text(text="Communication:",
          parent=toggle_box,
          position=(-0.45, pathchoice_text.y + y_loc + e, -1),
          color=color.white,
          scale=2.5)
    
    comm_yes = Button( radius=0.3,
                      scale=(0.1,0.1), 
                      position=(comm_text.x + x_loc*2, pathchoice_lhc.y + y_loc + e, -1),
                      text='yes',
                      color=color.blue, 
                      text_color=color.white,
                      parent=toggle_box)
    
    comm_yes.text_size_setter(0.45)
     
    comm_no = Button( radius=0.3,
                      scale=(0.1,0.1), 
                      position=(comm_yes.x + 0.14, pathchoice_lhc.y + y_loc + e, -1),
                      text='no',
                      color=color.blue, 
                      text_color=color.white,
                      parent=toggle_box)
    
    comm_no.text_size_setter(0.45)
    
    comm_yes.on_click = Func(set_comm, True)
    comm_no.on_click = Func(set_comm, False)
   
    ## Add Submit Button
    submit_button = Button( 
                            radius=0.3,
                            scale=(0.23,0.1), 
                            position=(-0.35, comm_yes.y + y_loc + 2*e, -2),
                            text='Submit',
                            color=color.orange, 
                            text_color=color.black,
                            parent=toggle_box)
    
    submit_button.text_size_setter(0.45)
    submit_button.on_click = Func(gameplay_pathfinding)
    
    
    ## Show path details
    distance_text = Text(text='',
          parent=toggle_box,
          position=(-0.18, comm_yes.y + y_loc + e, -1),
          color=color.white,
          scale=2.5)
    path_slope_text = Text(text='',
          parent=toggle_box,
          position=(-0.18, distance_text.y + y_loc, -1),
          color=color.white,
          scale=2.5)
   
   
   
    return slope_option_15,slope_option_20,destination_option_1,destination_option_2,destination_option_3,destination_option_4,\
        pathchoice_shortest, pathchoice_lhc, comm_yes, comm_no, distance_text, path_slope_text

def generate_custom_terrain(option, pathtexture=None, distance=0, slope_ = 0):
    global color_key
    print("START OF ENTITIES")
    ct = 0
    for ent in scene.entities:
        ct +=1
        #print(ct, ", " , ent.name)
        if ent.name == 'lunar_model':
            destroy(ent)
        
        # if ent and ent.name == 'color_key':
        #     destroy(ent)  
              
    print("END OF ENTITIES")
    
    if option == 'HEIGHT':
        print("HEIGHT")
        
        #lunar_model = generate_terrain(heightmap = "noisemap.png", texture = HEIGHTMAPS[2])
        lunar_model = generate_terrain(heightmap = HEIGHTMAPS[0], texture = HEIGHTMAPS[2])
        destroy(color_key)
        color_key = show_color_key(texture = HEIGHTMAPS[1])
        rover.enabled  = True

    
    if option == 'SLOPE':
        print("SLOPE")
        lunar_model = generate_terrain(heightmap = SLOPEMAPS[0], texture = SLOPEMAPS[2])
        destroy(color_key)
        color_key = show_color_key(texture = SLOPEMAPS[1])
        rover.enabled  = True
    
    
    if option == 'ELEVATION':
        print("ELEVATION")
        lunar_model = generate_terrain(heightmap = ELEVATIONMAPS[0], texture = ELEVATIONMAPS[2])
        destroy(color_key)
        color_key = show_color_key(texture = ELEVATIONMAPS[1])
        rover.enabled  = True
    
    
    if option == 'AZIMUTH':
        print("AZIMUTH")
        lunar_model = generate_terrain(heightmap = AZIMUTHMAPS[0], texture = AZIMUTHMAPS[2])
        destroy(color_key)
        color_key = show_color_key(texture = AZIMUTHMAPS[1])
        rover.enabled  = True
        
    if option == 'PATHFINDING':
        print("PATHFINDING")
        
        #lunar_model = generate_terrain(heightmap = "noisemap.png", texture = HEIGHTMAPS[2])
        lunar_model = generate_terrain(heightmap = HEIGHTMAPS[0], texture = pathtexture)
        destroy(color_key)
        color_key = show_color_key(texture = HEIGHTMAPS[1])
        rover.enabled  = True
        #rover.position = (-1121, 247, 1617)
        rover.position = (-1121, -2.25, 1617)
        distance_text.text = 'Distance: ' + f'{distance} m'
        path_slope_text.text = 'Slope: ' + f'{slope_}°'
        player.cursor.visible = True
        
    lunar_model.enable()
    color_key.enable()
    player.enable()
    
    return lunar_model, color_key


def gameplay_height():
    destroy(lunar_model)
    destroy(color_key)
    return generate_custom_terrain(OPTIONS[0])


def gameplay_slope():
    destroy(lunar_model)
    destroy(color_key)
    
    return generate_custom_terrain(OPTIONS[1])


def gameplay_elevation():
    destroy(lunar_model)
    destroy(color_key)
    
    return generate_custom_terrain(OPTIONS[2])

def gameplay_azimuth():
    destroy(lunar_model)
    destroy(color_key)
    
    return generate_custom_terrain(OPTIONS[3])

def gameplay_pathfinding():
    destroy(lunar_model)
    destroy(color_key)
    
    #print(f"{slope}, {destination}, {path}")
    slope_ = next(key for key, value in slope.items() if value)
    dest_ = next(key for key, value in destination.items() if value)
    path_ = next(key for key, value in path.items() if value)
    
    print(f"{slope_},{dest_}, {path_},{comm}")
    
    pathtexture = info_helper.get_path_texture(slope_, dest_, path_, comm)
    path_distance, path_slope = info_helper.get_path_details(slope_, dest_, path_, comm)
    return generate_custom_terrain(OPTIONS[4], pathtexture, path_distance, path_slope)
    

def show_color_key(texture):
   
    color_key = Entity(
              parent=info_box,
              model='quad',
              origin=(0,0),
              position=(0.7, -0.75, 0),
              texture = texture,
              scale_x= 2.0,
              scale_y = 0.45,
              name= 'color_key')
    
    #color_key.rotation_x += 90  
    return color_key
    
def update_texture():
    pass


def printCoordinates():
    #print(f"EARTH == x: {earth.x}, y: {earth.y}, z: {earth.z}")
    #print(f"LUNAR == x: {lunar_height_model.x}, y: {lunar_height_model.y}, z: {lunar_height_model.z}")
    print(f"CAMERA == x: {camera.x}, y: {camera.y}, z: {camera.z}")
    print(f"PLAYER == x: {player.x}, y: {player.y}, z: {player.z}")
    print(f"INFO_BOX == x: {info_box.x}, y: {info_box.y}, z: {info_box.z}")
    print(f"PLANE WORLD coordinates == x: {plane.world_x}, y: {plane.world_y}, z: {plane.world_z}")
    print(f"PLANE coordinates == x: {plane.x}, y: {plane.y}, z: {plane.model_bounds}")
    print(f"Rover rotation = {rover.rotation_getter()}")

def input(key):
    if key == 'p':
      printCoordinates()
    if key == 'q' or key == 'esc':
      quit()
    if key == 'm':
        player.enabled = False
        mouse.visible = True
    # if key=='r':
    #     update_rover_location()
       

    

def troubleshoot():
    plane.enabled = False
    player.enabled = False
    earth.enabled = False
    


def update():
    global regen, count, direction_changed
    
    walking = held_keys['a'] or \
            held_keys['d'] or \
            held_keys['w'] or \
            held_keys['s']

    
   
    #rel_pos = rover.get_position(relative_to = lunar_height_model)
    pos = player.get_position()
    pos1 = rover.get_position()
    x,y,z,lon,lat,height,slope,elevation, azimuth = info_helper.get_info(pos.x,  pos.z)
    lat_text.text = 'Latitude: ' + f'{lat:.2f} °N'
    lon_text.text = 'Longitude: ' + f'{lon:.2f} °E'
    height_text.text = 'Height: ' + f'{height:.2f} m'
    slope_text.text = 'Slope: ' + f'{slope:.2f}°'
    elevation_text.text = 'Elevation to Earth: ' + f'{elevation:.2f}°'
    #rover_text.text = f'Position: ({pos1.x:.2f}, {pos1.y:.2f}, {pos1.z:.2f})'
    azimuth_text.text = 'Azimuth to Earth: ' + f'{azimuth:.2f}°'
    
    
    
    #update the mini_dot location on mini_map
    reset = update_mini_dot_position(pos.x,  pos.z)
    
    if (reset):
        player.position = default_pos
        print("resetting")
        #generate_terrain()
    
    
    #player.y = terraincast(world_position, lunar_height_model)
    #lon_text.text = f'Position: ({pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f})'
    #print(info_helper.get_info(pos.x,  pos.z, pos.y))

    #update rover direction
    rotate_rover(direction_changed)

    #troubleshooting
    #troubleshoot()

def reset_game():
    pass

#Create the Visualization
earth = Entity(model= 'sphere',
                parent=camera.ui,
                texture='earth_daymap.jpg',
                collider= 'box',
                scale=(0.04,0.04,0.04),
                position= (0.45, 0.45, 0.05))

#Create info and options box
info_box = create_info_box()
lat_text, lon_text, height_text, slope_text, elevation_text, azimuth_text, rover_text = create_info_text()

#Create info and options box
toggle_box = create_toggle_box()
toggle_text = create_toggles()
slope_option_15,slope_option_20,destination_option_1,destination_option_2,destination_option_3,destination_option_4,\
    pathchoice_shortest, pathchoice_lhc, comm_yes, comm_no, distance_text, path_slope_text = create_pathfinding_options()

#Create an empty plane  
plane = Entity(model = 'plane',
                parent='camera.ui')

rover = create_rover()
lunar_model, color_key = generate_custom_terrain(option=OPTIONS[0])

mini_map = create_mini_map()
mini_dot = create_mini_dot()



#hv = lunar_height_model.model.height_values.tolist()
#print(hv)

     



sky = Sky(texture='sky_default', color=color.black)
# sky.color = color.blue
window.fullscreen = True
#window.size = (1300, 900)
window.fps_counter.enabled = False
window.exit_button.visible = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False
#window.color = color.black


input_handler.bind('up arrow', 'w')
input_handler.bind('left arrow', 'a')
input_handler.bind('down arrow', 's')
input_handler.bind('right arrow', 'd')
input_handler.bind('right mouse down', 'm')
#Cursor() 
#mouse.visible = True



app.run(info=False)



