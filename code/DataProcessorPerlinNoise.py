import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from panda3d.core import PNMImage
from noise import snoise2

def loadData():
    heights = np.loadtxt('../datafiles/FY23_ADC_Height_PeakNearShackleton.csv', delimiter=',')
    #print(heights_.shape)
    
    slopes = np.loadtxt('../datafiles/FY23_ADC_Slope_PeakNearShackleton.csv', delimiter=',')
    #print(slopes.shape)
    
    lat = np.loadtxt('../datafiles/FY23_ADC_Latitude_PeakNearShackleton.csv', delimiter=',')
    lon = np.loadtxt('../datafiles/FY23_ADC_Longitude_PeakNearShackleton.csv', delimiter=',')
    return lon, lat, heights, slopes

def generatePerlinNoise():
    scale = 10.0  # Adjust this value to control the "detail" of the noise
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0

    # Generate Perlin noise
    noise_data = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            noise_data[y, x] = snoise2(x / scale,
                                       y / scale,
                                       octaves=octaves,
                                       persistence=persistence,
                                       lacunarity=lacunarity,
                                       repeatx=1024,
                                       repeaty=1024,
                                       base=0)

    # Normalize the noise to [0, 255]
    min_noise = np.min(noise_data)
    max_noise = np.max(noise_data)
    normalized_noise = ((noise_data - min_noise) / (max_noise - min_noise)) * 255
    
    return normalized_noise
    
def createHeightMap(data):

    data = (data - np.min(data)) / (np.max(data) - np.min(data)) * 65535
    
    # Convert to 16-bit integer
    data = data.astype(np.uint16)
    
    #Create and save the heightmap
    image = Image.fromarray(data, mode='I;16')
    image = image.resize((256, 256))
    image.save('assets/pns_heightmap.png')
    


lon, lat, heights, slopes = loadData()
createHeightMap(heights)


    