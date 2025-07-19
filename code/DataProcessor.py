import numpy as np
import hickle as hkl
import networkx as nw
import math


#Earth coordinates from handbook
EARTH_X = 361000 * 1000
EARTH_Y = 0
EARTH_Z = -421000 * 1000

#https://www.oc.nps.edu/oc2902w/coord/llhxyz.htm
#Earth latitude longitude for the given coordinates
EARTH_LAT = -49.38968
EARTH_LON = 0

def load_data_pns():
    heights = np.loadtxt('../datafiles/FY23_ADC_Height_PeakNearShackleton.csv', delimiter=',')
    #print(heights_.shape)
    
    slopes = np.loadtxt('../datafiles/FY23_ADC_Slope_PeakNearShackleton.csv', delimiter=',')
    #print(slopes.shape)
    
    lat = np.loadtxt('../datafiles/FY23_ADC_Latitude_PeakNearShackleton.csv', delimiter=',')
    lon = np.loadtxt('../datafiles/FY23_ADC_Longitude_PeakNearShackleton.csv', delimiter=',')
    return lon, lat, heights, slopes


def load_data_fra():
    heights = np.loadtxt('../datafiles/FY23_ADC_Height_FaustiniRimA.csv', delimiter=',')
    #print(heights_.shape)
    
    slopes = np.loadtxt('../datafiles/FY23_ADC_Slope_FaustiniRimA.csv', delimiter=',')
    #print(slopes.shape)
    
    lat = np.loadtxt('../datafiles/FY23_ADC_Latitude_FaustiniRimA.csv', delimiter=',')
    lon = np.loadtxt('../datafiles/FY23_ADC_Longitude_FaustiniRimA.csv', delimiter=',')
    return lon, lat, heights, slopes

    
def createCartesianCoordinates(lon, lat, heights):
    lunar_radius = 1737400 #meters
    #radius = lunar_radius + terrain height
    #x = radius * (cos(lat) * cos(long))
    #y = radius * (cos(lat) * sin(long))
    #z = radius * sin(lat)
    
    long_radians = np.radians(lon)
    lat_radians = np.radians(lat)
    
    radius = lunar_radius + heights
    
    x = radius * np.cos(lat_radians) * np.cos(long_radians)
    y = radius * np.cos(lat_radians) * np.sin(long_radians)
    z = radius * np.sin(lat_radians)
    
    print(x.shape)
    return x, y, z

def atan2_calc(y,x):
    #print("x = ",x, ","," y = ", y)
    if (x > 0):
        atan2 = np.arctan(y/x)
    
    elif (x < 0 and y >= 0):
        atan2 = np.arctan(y/x) + np.pi
    
    elif (x < 0 and y < 0) :
        atan2 = np.arctan(y/x) - np.pi
    
    elif (x == 0 and y > 0):
        atan2 = np.pi/2
        
    elif (x == 0 and y < 0) :
        atan2 = -1 * np.pi/2
    return 180 - np.degrees(atan2)
    
    
#Azimuth angle from astronaut (location A) to earth (location B)
def calculateAzimuth(lon, lat):
    size = lon.shape
    azimuth = np.zeros(size)
    for i in range(size[0]):
        for j in range(size[1]):
            
            long_radians = np.radians(lon[i][j])
            lat_radians = np.radians(lat[i][j])
            
            y = np.sin(np.radians(EARTH_LON) - long_radians) * np.cos(np.radians(EARTH_LAT))
            
            x = (np.cos(lat_radians) * np.sin(np.radians(EARTH_LAT))) - \
                (np.sin(lat_radians) * np.cos(np.radians(EARTH_LAT)) * np.cos(np.radians(EARTH_LON) - long_radians))
        
            azimuth[i][j] = atan2_calc(y,x)
    return azimuth
    
#Elevation angle from astronaut(A) to earth(B)
def calculateElevation(x, y, z, lon, lat):
    long_radians = np.radians(lon)
    
    lat_radians = np.radians(lat)
    
    x_ab, y_ab, z_ab = EARTH_X - x,  EARTH_Y - y,  EARTH_Z - z
    range_ab = np.sqrt(x_ab*x_ab + y_ab*y_ab + z_ab*z_ab )
    rz = x_ab * np.cos(lat_radians) * np.cos(long_radians) + \
        y_ab * np.cos(lat_radians) * np.sin(long_radians) + \
            z_ab * np.sin(lat_radians)
    
    elevation = np.degrees(np.arcsin(rz/range_ab))
    
    return elevation
    
    

def roundData(x,y,z,lon,lat,heights,slopes,elevation,azimuth):
    x = np.round(x,2)
    y = np.round(y,2)
    z = np.round(z,2)
    lon = np.round(lon,5)
    lat = np.round(lat,5)
    heights = np.round(heights,2)
    slopes = np.round(slopes,2)
    elevation = np.round(elevation,2)
    azimuth = np.round(azimuth,2)
    
    
    return x,y,z,lon,lat,heights,slopes, elevation,azimuth



def store_data(x,y,z,lon,lat,heights,slopes,elevation,azimuth,filename):
    stacked_data = []
    stacked_data.append(x)
    stacked_data.append(y)
    stacked_data.append(z)
    stacked_data.append(lon)
    stacked_data.append(lat)
    stacked_data.append(heights)
    stacked_data.append(slopes)
    stacked_data.append(elevation)
    stacked_data.append(azimuth)
    hkl.dump(stacked_data, filename)

#
# This method returns the distance between 2 points using 3d system
#
def get_distance(point1, point2):
        x1 = x_fra[point1[0]][point1[1]]
        y1 = y_fra[point1[0]][point1[1]]
        z1 = z_fra[point1[0]][point1[1]]
        
        x2 = x_fra[point2[0]][point2[1]]
        y2 = y_fra[point2[0]][point2[1]]
        z2 = z_fra[point2[0]][point2[1]]
        
        d = math.sqrt( ((x2-x1) * (x2-x1)) + 
                ((y2-y1) * (y2 - y1)) + 
                ((z2 - z1) * (z2 - z1)))
        
        return d

def store_graph(slope, file_name):
    slopes = slopes_fra[:, :2000]
    rows, cols = slopes.shape
    G = nw.Graph() 
        
    for i in range(rows):
        for j in range(cols):
            # Add node
            if(slopes[i][j] < slope):
                G.add_node((i, j))
    
    
    for i in range(rows):
        for j in range(cols):
            
            if (i, j) in G.nodes:
                # Check 8 neighboring nodes and add edges with 'slope' attribute
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue  # Skip the current node
                        nx_, ny = i + dx, j + dy
                        if 0 <= nx_ < rows and 0 <= ny < cols:
                            if (nx_, ny) in G.nodes:  # Check if neighbor node exists in the graph
                                distance = get_distance(point1 = (i,j), point2 = (nx_,ny)) 
                                slope_val = abs(slopes[nx_][ny] - slopes[i][j])
                                G.add_edge((i, j), (nx_, ny), slope=slope_val, distance = distance)  # Add the edge

    
                
    hkl.dump(G, file_name)    
#
# start processing -- PNS
#
# lon_pns, lat_pns, heights_pns, slopes_pns = load_data_pns()
# #check values for latitue
# print(lon_pns[0,0])
# print(lon_pns[0,3199])
# print(lon_pns[3199,3199])
# print(lon_pns[3199,0])

# x_pns, y_pns, z_pns = createCartesianCoordinates(lon_pns, lat_pns, heights_pns)
# elevation_pns = calculateElevation(x_pns,y_pns,z_pns,lon_pns, lat_pns)
# azimuth_pns = calculateAzimuth(lon_pns, lat_pns)


#x_pns,y_pns,z_pns,lon_pns,lat_pns,heights_pns,slopes_pns, elevation_pns, azimuth_pns = \
#    roundData(x_pns,y_pns,z_pns,lon_pns,lat_pns,heights_pns,slopes_pns, elevation_pns, azimuth_pns)

#store_data(x_pns,y_pns,z_pns,lon_pns,lat_pns,heights_pns,slopes_pns,elevation_pns, azimuth_pns, 'pns_data.hkl')


#
# start processing -- FRA
#
lon_fra, lat_fra, heights_fra, slopes_fra = load_data_fra()

x_fra, y_fra, z_fra = createCartesianCoordinates(lon_fra, lat_fra, heights_fra)
elevation_fra = calculateElevation(x_fra,y_fra,z_fra,lon_fra, lat_fra)
azimuth_fra = calculateAzimuth(lon_fra, lat_fra)

x_fra,y_fra,z_fra,lon_fra,lat_fra,heights_fra,slopes_fra, elevation_fra, azimuth_fra = \
    roundData(x_fra,y_fra,z_fra,lon_fra,lat_fra,heights_fra,slopes_fra, elevation_fra, azimuth_fra)

store_data(x_fra,y_fra,z_fra,lon_fra,lat_fra,heights_fra,slopes_fra, elevation_fra, azimuth_fra, 'fra_data.hkl')

store_graph(slope=15, file_name = 'fra_slope15.hkl')
store_graph(slope=20, file_name = 'fra_slope20.hkl')



# print("PNS slopes = ", np.min(slopes_pns), "," , np.max(slopes_pns))
# print("PNS heights = ", np.min(heights_pns), "," , np.max(heights_pns))
# print("FRA slopes = ", np.min(slopes_fra), "," , np.max(slopes_fra))
# print("FRA heights = ", np.min(heights_fra), "," , np.max(heights_fra))



    