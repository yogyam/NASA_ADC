#generate heightmaps separately
import hickle as hk
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import interp1d
import numpy as np
import cv2


from helper import Helper

IMAGE_SIZE_SMALL = (400,400)
IMAGE_SIZE = (2048,2048)
IMAGE_SIZE_P = (4000,4000)
#IMAGE_SIZE = (4000,4000)
SCALE = 256
EXPO_HEIGHT = 1.05

REL_PATH = './assets/Images/'
REL_PATH_SEARCH = './assets/paths/'

PATH_DETAILS = REL_PATH_SEARCH + 'path_details.hkl'

noisemap = REL_PATH+'noisemap.png'
info_helper  = Helper()


FRA_SLOPEMAPS = [REL_PATH + 'fra_slopemap.png', 
                 REL_PATH + 'fra_slopemap_small.png', 
                 REL_PATH + 'fra_slopemap_colorkey.png' , 
                 REL_PATH + 'fra_slopemap_texture.png',
                 REL_PATH + 'fra_slopemap_colormap.png' ]

FRA_HEIGHTMAPS = [REL_PATH + 'fra_heightmap.png', 
                 REL_PATH + 'fra_heightmap_small.png', 
                 REL_PATH + 'fra_heightmap_colorkey.png' , 
                 REL_PATH + 'fra_heightmap_texture.png',
                 REL_PATH + 'fra_heightmap_colormap.png' ]     


FRA_ELEVATIONMAPS = [REL_PATH + 'fra_elevationmap.png', 
                 REL_PATH + 'fra_elevationmap_small.png', 
                 REL_PATH + 'fra_elevationmap_colorkey.png' , 
                 REL_PATH + 'fra_elevationmap_texture.png',
                 REL_PATH + 'fra_elevationmap_colormap.png' ]  

FRA_AZIMUTHMAPS = [REL_PATH + 'fra_azimuthmap.png', 
                 REL_PATH + 'fra_azimuthmap_small.png', 
                 REL_PATH + 'fra_azimuthmap_colorkey.png' , 
                 REL_PATH + 'fra_azimuthmap_texture.png',
                 REL_PATH + 'fra_azimuthmap_colormap.png' ] 


PATH_FILES = [REL_PATH_SEARCH + 'fra_dest{}_shortest.pkl',
              REL_PATH_SEARCH + 'fra_dest{}_slope_20.pkl',
              REL_PATH_SEARCH + 'fra_dest{}_lhc.pkl']

colors = ['blue', 'black','purple']

PATH_MAPS = [REL_PATH + 'fra_dest{}_shortest.png',
              REL_PATH + 'fra_dest{}_slope_20.png',
              REL_PATH + 'fra_dest{}_lhc.png']

PATH_MAPS_COMM = [REL_PATH + 'fra_dest{}_shortest_comm.png',
              REL_PATH + 'fra_dest{}_slope_20_comm.png',
              REL_PATH + 'fra_dest{}_lhc_comm.png']
      
def get_data(loaded_data):
     x = loaded_data[0]
     y = loaded_data[1]
     z = loaded_data[2]
     lon = loaded_data[3]
     lat = loaded_data[4]
     heights = loaded_data[5]
     slopes = loaded_data[6]
     elevation = loaded_data[7]
     azimuth = loaded_data[8]
 
     return x,y,z,lon,lat,heights,slopes, elevation, azimuth
     
 
# with open('pns_data.hkl', 'rb') as f:
#      pns_loaded_data = hk.load(f)
#      #print(pns_loaded_data)
            
with open('fra_data.hkl', 'rb') as f:
     fra_loaded_data = hk.load(f)
     
x_fra,y_fra,z_fra,lon_fra,lat_fra,heights_fra,slopes_fra, elevation_fra, azimuth_fra = get_data(fra_loaded_data)
#x_pns,y_pns,z_pns,lon_pns,lat_pns,heights_pns,slopes_pns, elevation_pns, azimuth_pns = get_data(pns_loaded_data)


def get_texture(heatmap, filename, alpha = 0.75):
    texture = REL_PATH + 'texture2.png'
    texture_img = Image.open(texture)
    overlay_img = Image.open(heatmap)
    final_img = Image.blend(texture_img, overlay_img, alpha) 
    final_img.save(filename)
    
def create_heat_map(data, colorscale, image_name, img_small, color_key,  title, alpha = 0.75):
    ax = sns.heatmap(data, cmap=colorscale, cbar=False, xticklabels=False, yticklabels=False)
    
    plt.savefig(image_name, format = "png", bbox_inches='tight', pad_inches=0, dpi = 2048)
    plt.close()

    #save the colorbar
    plt.imshow(data, cmap=colorscale)
    plt.style.use("dark_background")
    cbar = plt.colorbar(orientation="horizontal") 
    cbar.set_label(title)
    plt.savefig(color_key, format = "png", bbox_inches='tight',  dpi = 512)
    plt.close()


    #resize the texture image to 2048*2048 and 400*400
    image = cv2.imread(image_name, cv2.IMREAD_UNCHANGED)
    
    resized_image = cv2.resize(image, IMAGE_SIZE)
    cv2.imwrite(image_name, resized_image)
    
    resized_image_sm = cv2.resize(image, IMAGE_SIZE_SMALL)
    cv2.imwrite(img_small, resized_image_sm)
    

    noise = Image.open(noisemap)
    resized_image_sm = Image.open(img_small)
    
    if noise.mode != resized_image_sm.mode:
        #print("resampling")
        resized_image_sm = resized_image_sm.convert(noise.mode)

    #print(noise.mode)
    #print(resized_image_sm.mode)
    
    final_img = Image.blend(resized_image_sm, noise, 0.75) 
    final_img.save(img_small)
    
    
def create_color_bar(color_key, new_color_bar):
    original_image = Image.open(color_key)
    bar_coordinates = (0, 1360, 2762, 2074)  

    color_bar = original_image.crop(bar_coordinates)
    #rotated_color_bar = color_bar.transpose(Image.Transpose.ROTATE_270)

    color_bar.save(new_color_bar)  
    

def create_path(orig_image, path, new_image, linecolor, comm = False):
    image = Image.open(orig_image)
    resized_image = image.resize(IMAGE_SIZE_P, resample=Image.LANCZOS)
    
    with open(path, 'rb') as f:
         path_arr = hk.load(f)
    
    #print(f"{path}, {path_arr}")
    swapped_path = [(y, x) for x, y in path_arr]
    draw = ImageDraw.Draw(resized_image)
    
    if (comm):
        draw.line(swapped_path, fill = linecolor, width = 1, joint= "curve")
        
        draw.ellipse((swapped_path[0][0] - 2, swapped_path[0][1] - 2, swapped_path[0][0] + 2, swapped_path[0][1] + 2), fill='red', width=50)  # Mark first node as red
        draw.ellipse((swapped_path[-1][0] - 2, swapped_path[-1][1] - 2, swapped_path[-1][0] + 2, swapped_path[-1][1] + 2), fill='green', width=50)  # Mark last node as green
    
        #Plot communciation points
        comm_points = find_points(path_arr)
        swapped_comm_points = [(y, x) for x, y in comm_points]
        #print(f"comm points =  {swapped_comm_points}")
        for point in swapped_comm_points:
            x,y = point
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill='orange')
        
        image = resized_image.resize(IMAGE_SIZE, resample=Image.LANCZOS)
        image.save(new_image)
        
    else:
        draw.line(swapped_path, fill = linecolor, width = 1, joint= "curve")
        
        draw.ellipse((swapped_path[0][0] - 2, swapped_path[0][1] - 2, swapped_path[0][0] + 2, swapped_path[0][1] + 2), fill='red', width=50)  # Mark first node as red
        draw.ellipse((swapped_path[-1][0] - 2, swapped_path[-1][1] - 2, swapped_path[-1][0] + 2, swapped_path[-1][1] + 2), fill='green', width=50)  # Mark last node as green
    
        
        image = resized_image.resize(IMAGE_SIZE, resample=Image.LANCZOS)
        image.save(new_image)


def create_combined_path(orig_image, path15, path20, new_image, linecolor15, linecolor20, comm = False):
    image = Image.open(orig_image)
    resized_image = image.resize(IMAGE_SIZE_P, resample=Image.LANCZOS)
    
    with open(path15, 'rb') as f:
         path_arr_15 = hk.load(f)
         
    with open(path20, 'rb') as f:
         path_arr_20 = hk.load(f)
    
    #print(f"{path}, {path_arr}")
    swapped_path_15 = [(y, x) for x, y in path_arr_15]
    swapped_path_20 = [(y, x) for x, y in path_arr_20]
    
    draw = ImageDraw.Draw(resized_image)
    
    if (comm):
        draw.line(swapped_path_15, fill = linecolor15, width = 1, joint= "curve")
        draw.line(swapped_path_20, fill = linecolor20, width = 1, joint= "curve")
        
        draw.ellipse((swapped_path_15[0][0] - 2, swapped_path_15[0][1] - 2, swapped_path_15[0][0] + 2, swapped_path_15[0][1] + 2), fill='red', width=50)  # Mark first node as red
        draw.ellipse((swapped_path_15[-1][0] - 2, swapped_path_15[-1][1] - 2, swapped_path_15[-1][0] + 2, swapped_path_15[-1][1] + 2), fill='green', width=50)  # Mark last node as green
    
        #Plot communciation points
        comm_points = find_points(path_arr_15)
        swapped_comm_points = [(y, x) for x, y in comm_points]
        for point in swapped_comm_points:
            x,y = point
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill='orange')
            
        #Plot communciation points
        comm_points = find_points(path_arr_20)
        swapped_comm_points = [(y, x) for x, y in comm_points]
        for point in swapped_comm_points:
            x,y = point
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill='orange')  
    
        image = resized_image.resize(IMAGE_SIZE, resample=Image.LANCZOS)
        image.save(new_image)
            
        
    else:
        draw.line(swapped_path_15, fill = linecolor15, width = 1, joint= "curve")
        draw.line(swapped_path_20, fill = linecolor20, width = 1, joint= "curve")
        
        draw.ellipse((swapped_path_15[0][0] - 2, swapped_path_15[0][1] - 2, swapped_path_15[0][0] + 2, swapped_path_15[0][1] + 2), fill='red', width=50)  # Mark first node as red
        draw.ellipse((swapped_path_15[-1][0] - 2, swapped_path_15[-1][1] - 2, swapped_path_15[-1][0] + 2, swapped_path_15[-1][1] + 2), fill='green', width=50)  # Mark last node as green
    
        
        image = resized_image.resize(IMAGE_SIZE, resample=Image.LANCZOS)
        image.save(new_image)

def find_points(path_arr):
    x, y = zip(*path_arr)
    x = np.array(x)
    y = np.array(y)

    distances = np.cumsum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))
    distances = np.insert(distances, 0, 0)  # Insert initial distance as 0
    
    interp_func = interp1d(distances, np.vstack([x, y]).T, kind='linear', axis=0)
    new_distances = np.linspace(0, distances[-1], 10)  # Generate 10 equidistant distances
    new_points = interp_func(new_distances)
    
    equidistant_points = [(int(round(point[0])), int(round(point[1]))) for point in new_points[1:-1]]
    print(f"path =  {equidistant_points}")

    return equidistant_points

def store_path_info():
    
    path_info = {"15_1_shortest":"fra_dest1_shortest",
                  "15_2_shortest":"fra_dest2_shortest",
                  "15_3_shortest":"fra_dest3_shortest",
                  "15_4_shortest":"fra_dest4_shortest",
                  
                  "15_1_lhc":"fra_dest1_lhc",
                  "15_2_lhc":"fra_dest2_lhc",
                  "15_3_lhc":"fra_dest3_lhc",
                  "15_4_lhc":"fra_dest4_lhc",
                  
                  "20_1_shortest":"fra_dest1_slope_20",
                  "20_2_shortest":"fra_dest2_slope_20",
                  "20_3_shortest":"fra_dest3_slope_20",
                  "20_4_shortest":"fra_dest4_slope_20"}
    
    for key, value in path_info.items():
        path = REL_PATH_SEARCH + value+'.pkl'
        
        with open(path, 'rb') as f:
             path_arr = hk.load(f)
         
        total_distance = 0
        for i in range(len(path_arr) - 2):
            total_distance += info_helper.get_distance(path_arr[i], path_arr[i+1])
            
        total_slope = 0
        for i in range(len(path_arr) - 1):
            total_slope += info_helper.get_slope(path_arr[i], path_arr[i+1])
        
        path_info[key] = (round(total_distance,4), round(total_slope,2))
        
        print(f"{key}, {total_distance}, {total_slope}")
        
    
    hk.dump(path_info, PATH_DETAILS)
    
    
    

def check_path(path1, path2):
    with open(path1, 'rb') as f:
         path_arr1 = hk.load(f)
         
    with open(path2, 'rb') as f:
         path_arr2 = hk.load(f)
    
    print(f"{path_arr1 == path_arr2}")
    



# create_heat_map(slopes_fra, colorscale='Accent', image_name = FRA_SLOPEMAPS[0], img_small = FRA_SLOPEMAPS[1], color_key = FRA_SLOPEMAPS[4], title = 'Slope (degrees)' )
# get_texture(heatmap = FRA_SLOPEMAPS[0], filename = FRA_SLOPEMAPS[3])
# create_color_bar(FRA_SLOPEMAPS[4], FRA_SLOPEMAPS[2]) 
    
# create_heat_map(heights_fra, colorscale='gray', image_name = FRA_HEIGHTMAPS[0], img_small = FRA_HEIGHTMAPS[1], color_key = FRA_HEIGHTMAPS[4], title = 'Height (meters)', )
# get_texture(heatmap = FRA_HEIGHTMAPS[0], filename = FRA_HEIGHTMAPS[3],  alpha = 0.4)
# create_color_bar(FRA_HEIGHTMAPS[4], FRA_HEIGHTMAPS[2])
  
# create_heat_map(elevation_fra, colorscale='viridis', image_name = FRA_ELEVATIONMAPS[0], img_small = FRA_ELEVATIONMAPS[1], color_key = FRA_ELEVATIONMAPS[4],  title = 'Elevation (degrees)' )
# get_texture(heatmap = FRA_ELEVATIONMAPS[0], filename = FRA_ELEVATIONMAPS[3])
# create_color_bar(FRA_ELEVATIONMAPS[4], FRA_ELEVATIONMAPS[2])
    
# create_heat_map(azimuth_fra, colorscale='cividis', image_name = FRA_AZIMUTHMAPS[0], img_small = FRA_AZIMUTHMAPS[1], color_key = FRA_AZIMUTHMAPS[4], title = 'Azimuth (degrees)' )
# get_texture(heatmap = FRA_AZIMUTHMAPS[0], filename = FRA_AZIMUTHMAPS[3])
# create_color_bar(FRA_AZIMUTHMAPS[4], FRA_AZIMUTHMAPS[2])

for i in range(1, 5):
    for j in range(3):
        path = PATH_FILES[j]
        image = PATH_MAPS[j]
        image_comm = PATH_MAPS_COMM[j]
        
        new_path = path.replace('{}', str(i))
        new_image = image.replace('{}', str(i))
        new_image_comm = image_comm.replace('{}', str(i))
        
        if (j != 1):
            create_path(orig_image = FRA_HEIGHTMAPS[3], path = new_path, new_image = new_image, linecolor = colors[j] )
            create_path(orig_image = FRA_HEIGHTMAPS[3], path = new_path, new_image = new_image_comm, linecolor = colors[j], comm = True )
        
        else: 
            path_15 = PATH_FILES[0].replace('{}', str(i))
            create_combined_path(orig_image = FRA_HEIGHTMAPS[3], path15 = path_15, path20 = new_path, new_image = new_image, linecolor15 = colors[0], linecolor20 = colors[j] )
            create_combined_path(orig_image = FRA_HEIGHTMAPS[3], path15 = path_15, path20 = new_path, new_image = new_image_comm, linecolor15 = colors[0], linecolor20 = colors[j], comm = True )
            
# for i in range(1, 5):
#     path = PATH_FILES[0]
#     new_path = path.replace('{}', str(i))
#     with open(new_path, 'rb') as f:
#         path_arr = hk.load(f)
    
#     print("i = ", i)
#     for i in range(len(path_arr)):
#         point = path_arr[i]
#         #print(point)
#         if elevation_fra[point[0]][point[1]] >= 180 - azimuth_fra[point[0]][point[1]]:
#             print(f"Point = {path_arr[i]}")                                                         
    
store_path_info()