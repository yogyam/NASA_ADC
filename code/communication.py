import hickle as hk
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from helper import Helper


REL_PATH_SEARCH = './assets/paths/'

PATH_DETAILS = REL_PATH_SEARCH + 'path_details.hkl'
PATH_FILES = [REL_PATH_SEARCH + 'fra_dest{}_shortest.pkl',
              REL_PATH_SEARCH + 'fra_dest{}_slope_20.pkl',
              REL_PATH_SEARCH + 'fra_dest{}_lhc.pkl']

info_helper = Helper()

def create_plot(path):
    elevation = []
    azimuth = []
    for point in path:
        #print(point)
        elevation.append(info_helper.get_elevation(point))
        azimuth.append(info_helper.get_azimuth(point))
        
    plt.figure(figsize=(8, 6))

    # Plot elevation
    plt.subplot(2, 1, 1)  # Creating the first subplot for elevation
    plt.plot(elevation, marker='o', linestyle='-', color='blue')
    plt.title('Elevation along the Path')
    plt.xlabel('Point Index')
    plt.ylabel('Elevation')
    
    
    # Plot azimuth
    plt.subplot(2, 1, 2)  # Creating the second subplot for azimuth
    plt.plot(azimuth, marker='o', linestyle='-', color='green')
    plt.title('Azimuth along the Path')
    plt.xlabel('Point Index')
    plt.ylabel('Azimuth')
    
    plt.tight_layout()  # Ensuring proper layout
    plt.show()

def find_points(path):
    with open(path, 'rb') as f:
         path_arr = hk.load(f)
    
    print(len(path_arr))
    x, y = zip(*path_arr)
    x = np.array(x)
    y = np.array(y)

    distances = np.cumsum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))
    distances = np.insert(distances, 0, 0)  # Insert initial distance as 0
    
    interp_func = interp1d(distances, np.vstack([x, y]).T, kind='linear', axis=0)
    new_distances = np.linspace(0, distances[-1], 10)  # Generate 10 equidistant distances
    new_points = interp_func(new_distances)
    
    equidistant_points = [(int(round(point[0])), int(round(point[1]))) for point in new_points]
    print(f"path =  {equidistant_points}")

    return path_arr

    
    
for i in range(1, 5):
    for j in range(3):
        path = PATH_FILES[j]
        
        new_path = path.replace('{}', str(i))
        
        path_arr = find_points(path = new_path)
        
        if(i==4 and j == 1):
            create_plot(path_arr)
        
        
        