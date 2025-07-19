import numpy as np
import math

#Earth coordinates from handbook
EARTH_X = 361000 * 1000
EARTH_Y = 0
EARTH_Z = -421000 * 1000

EARTH_RADIUS = 6371071.03

#EARTH_LAT = math.asin(EARTH_Z/EARTH_RADIUS)
#print(EARTH_LAT)

path_arr = [(23,322), (24,342), (28,346)]
swapped_path = [(y, x) for x, y in path_arr]

print(swapped_path)


REL_PATH = './assets/Images/'
REL_PATH_SEARCH = './assets/paths/'
PATH_FILES = [REL_PATH_SEARCH + 'fra_dest{}_shortest.pkl',
              REL_PATH_SEARCH + 'fra_dest{}_slope_20.pkl',
              REL_PATH_SEARCH + 'fra_dest{}_lhc.pkl']



PATH_MAPS = [REL_PATH + 'fra_dest{}_shortest.png',
              REL_PATH + 'fra_dest{}_slope_20.png',
              REL_PATH + 'fra_dest{}_lhc.png']

for i in range(1, 5):
    for j in range(3):
        path = PATH_FILES[j]
        image = PATH_MAPS[j]
        
        new_path = path.replace('{}', str(i))
        new_image = image.replace('{}', str(i))
        
        if(i == 4 and (j== 0 or j==2)):
            print("skip")
        else:
            print(f"path = {new_path}, new_image = {new_image}")
            
destination = {1: False, 2: True, 3: False, 4: False}

true_key = next(key for key, value in destination.items() if value)

print("The key with True value is:", true_key)
