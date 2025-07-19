import hickle as hk
import numpy as np
from matplotlib.path import Path
import cv2
import networkx as nx
import math


class Helper:
    
    def __init__(self):
        with open('fra_data.hkl', 'rb') as f:
            self.loaded_data = hk.load(f)
            
        with open('./assets/paths/path_details.hkl', 'rb') as f:
            self.path_details = hk.load(f)
            
        self.x = self.loaded_data[0]
        self.y = self.loaded_data[1]
        self.z = self.loaded_data[2]
        self.lon = self.loaded_data[3]
        self.lat = self.loaded_data[4]
        self.heights = self.loaded_data[5]
        self.slopes = self.loaded_data[6]
        self.elevation = self.loaded_data[7]
        self.azimuth = self.loaded_data[8]
        
        #path_dictionary
        self.path_dictionary = {"15_1_shortest":"fra_dest1_shortest",
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
                      "20_4_shortest":"fra_dest4_slope_20",
                      
                      "15_1_shortest_comm":"fra_dest1_shortest_comm",
                      "15_2_shortest_comm":"fra_dest2_shortest_comm",
                      "15_3_shortest_comm":"fra_dest3_shortest_comm",
                      "15_4_shortest_comm":"fra_dest4_shortest_comm",
                      
                      "15_1_lhc_comm":"fra_dest1_lhc_comm",
                      "15_2_lhc_comm":"fra_dest2_lhc_comm",
                      "15_3_lhc_comm":"fra_dest3_lhc_comm",
                      "15_4_lhc_comm":"fra_dest4_lhc_comm",
                      
                      "20_1_shortest_comm":"fra_dest1_slope_20_comm",
                      "20_2_shortest_comm":"fra_dest2_slope_20_comm",
                      "20_3_shortest_comm":"fra_dest3_slope_20_comm",
                      "20_4_shortest_comm":"fra_dest4_slope_20_comm"
          }
        
        
        
        self.landing = (1171, 922)
        self.destinations = [(832,1323), (589,388), (1630,824), (3427,820)]
        
        

#
# This method returns the latitide, longitude and other values based on the grid location
# Pass the index value as argument
#
            
    def get_info(self,x,y):
        
        x_index, y_index = self.map_coordinates_to_array(x,y)
        
        #print("x = ", x_index, " y = ", y_index)
        #print(self.x.shape)
        
        x = self.x[x_index, y_index]
        y = self.y[x_index, y_index]
        z = self.z[x_index, y_index]
        
        lon = self.lon[x_index, y_index]
        lat = self.lat[x_index, y_index]
        
        height = self.heights[x_index, y_index]
        
        slope = self.slopes[x_index, y_index]
        elevation = self.elevation[x_index, y_index]
        azimuth = self.azimuth[x_index, y_index]
        
        
        return x,y,z,lon,lat,height,slope, elevation, azimuth

#
# This method returns the distance between 2 points using 3d system
#
    def get_distance(self, point1, point2):
        x1 = self.x[point1[0]][point1[1]]
        y1 = self.y[point1[0]][point1[1]]
        z1 = self.z[point1[0]][point1[1]]
        
        x2 = self.x[point2[0]][point2[1]]
        y2 = self.y[point2[0]][point2[1]]
        z2 = self.z[point2[0]][point2[1]]
        
        d = math.sqrt( ((x2-x1) * (x2-x1)) + 
                ((y2-y1) * (y2 - y1)) + 
                ((z2 - z1) * (z2 - z1)))
        
        return d
    

#
# This method returns the slope between 2 points using 3d system
#
    def get_slope(self, point1, point2):
        distance = self.get_distance(point1, point2)
        return (abs(self.slopes[point1[0]][point1[1]] - self.slopes[point2[0]][point2[1]]) * distance)
        
#
# This method returns the azimuth angle at the given point
#
    def get_azimuth(self, point):
        return self.azimuth[point[0]][point[1]]      
#
# This method returns the elevation angle at the given point
#
    def get_elevation(self, point):
        return self.elevation[point[0]][point[1]]

#
# This method maps the player coordinates using the Ursina terrain location to the grid location
# Pass the player location
#
   
    def map_coordinates_to_array(self, player_x, player_y):
        # Given coordinates
        coordinates = np.array([
            [-2133, 3819],
            [3823, 1631],
            [1712, -4259],
            [-4246, -2077]
        ], dtype=np.float32)
    
        # Target indices for the given coordinates in the matrix
        target_indices = np.array([
            [0, 0],        # top_left
            [0, 3999],     # bottom_left
            [3999, 3999],  # bottom_right
            [3999, 0]      # top_right
        ], dtype=np.float32)
    
        # Convert the coordinates and target indices to the format required by getPerspectiveTransform
        coordinates_for_transform = coordinates.reshape(-1, 1, 2)
        target_indices_for_transform = target_indices.reshape(-1, 1, 2)
    
        # Create a transformation matrix using the perspective transformation
        matrix, _ = cv2.findHomography(coordinates_for_transform, target_indices_for_transform, method=cv2.RANSAC)
    
        # Transform the player's position to the array index
        player_coords = np.array([[player_x, player_y]], dtype=np.float32)
        transformed = cv2.perspectiveTransform(player_coords.reshape(-1, 1, 2), matrix)
        array_index = transformed.flatten().astype(int)
    
        # Ensure indices are within the range of the matrix
        scaled_indices = [max(0, min(idx, 3999)) for idx in array_index]
    
        return scaled_indices[0], scaled_indices[1]


#
# This method maps the player coordinates using the Ursina terrain location to the grid location
# Pass the player location
#
   
    def map_array_to_coordinates(self, row, col):
        # Given coordinates
        coordinates = np.array([
            [-2133, 3819],
            [3823, 1631],
            [1712, -4259],
            [-4246, -2077]
        ], dtype=np.float32)
    
        # Target indices for the given coordinates in the matrix
        indices = np.array([
            [0, 0],        # top_left
            [0, 3999],     # bottom_left
            [3999, 3999],  # bottom_right
            [3999, 0]      # top_right
        ], dtype=np.float32)

        # Convert the coordinates and target indices to the format required by getPerspectiveTransform
        coordinates_for_transform = coordinates.reshape(-1, 1, 2)
        target_indices_for_transform = indices.reshape(-1, 1, 2)
    
        # Create a transformation matrix using the perspective transformation
        matrix, _ = cv2.findHomography(coordinates_for_transform, target_indices_for_transform, method=cv2.RANSAC)
 
        array_coords = np.array([[row, col]], dtype=np.float32)
        inv_matrix = np.linalg.inv(matrix)  # Calculate the inverse of the transformation matrix
        
        transformed = cv2.perspectiveTransform(array_coords.reshape(-1, 1, 2), inv_matrix)
        player_position = transformed.flatten()
        
        return player_position[0], player_position[1]
#
# This method returns the location for the mini dot
# Pass the player location
#
    
    def get_mini_dot_location(self, x, y):
        # Given coordinates
        coordinates = np.array([
            [-2133, 3819],
            [3823, 1631],
            [1712, -4259],
            [-4246, -2077]
        ], dtype=np.float32)
    
        vertices = [
            (-2133, 3819),
            (3823, 1631),
            (1712, -4259),
            (-4246, -2077)]   
        
        target_coords = np.array([
            [-0.4599, 0.4599],        # top_left
            [0.4599, 0.4599],     # bottom_left
            [0.4599, -0.4599],  # bottom_right
            [-0.4599, -0.4599]      # top_right
        ], dtype=np.float32)
    
        # Calculate the transformation matrix
        matrix = cv2.getPerspectiveTransform(coordinates, target_coords)

        player_coords = np.array([[x,y, 1]], dtype=np.float32)
        transformed_coords = np.dot(matrix, player_coords.T).T
        
        transformed_x, transformed_y = transformed_coords[0, :2] / transformed_coords[0, 2]

        path = Path(vertices)
        
        reset = not (path.contains_point((x,y)))
        
        #if(reset):
        #        print("coordinates = ", x, ",", y)
        #print(transformed_coords)
        return (transformed_x, transformed_y), reset

#
# This method returns the index from the grid 
# Pass the latitude and longitude value
#    
    def get_index(self, lat_val, lon_val):
        self.lat = np.round(self.lat,3)
        self.lon = np.round(self.lon,3)
        
        row_lat, col_lat = np.where(lat_val == self.lat)
        print(row_lat , col_lat)
        
        row_lon, col_lon = np.where(lon_val == self.lon)
        print(row_lon , col_lon)

        common_row = np.intersect1d(row_lat, row_lon)
        common_col = np.intersect1d(col_lat, col_lon)
        
        corresponding_indices = []
        for row_index in range(4000):
            for col_index in range(4000):
                if self.lat[row_index, col_index] == lat_val and self.lon[row_index, col_index] == lon_val:
                    corresponding_indices.append((row_index, col_index))
        
        print("find me")
        print(corresponding_indices)
        
    
    def get_path_texture(self, slope, destination, path, comm):
        _comm = "_comm"
            
        #15_1_shortest"
        key = str(slope) + "_" + str(destination) + "_" + path
        if (comm):
            key += _comm
        
        return self.path_dictionary[key]
    
    def get_path_details(self, slope, destination, path, comm):
        _comm = "_comm"
            
        #15_1_shortest"
        key = str(slope) + "_" + str(destination) + "_" + path
        # if (comm):
        #     key += _comm
        
        return self.path_details[key]
        


helper  = Helper()
# print(helper.map_array_to_coordinates(helper.landing[0],helper.landing[1]))

# print(helper.map_coordinates_to_array(-1377.34, 1588.04))
#helper.store_graph()
#d1 = helper.get_distance(point1 = (832,1324), point2 = (832,1323))
#d2 = helper.get_distance(point1 = (833,1324), point2 = (832,1323))
#print("distance = ", d1, ",", d2)


# LANDING SITE -- DO NOT REMOVE
#print(helper.get_index(-87.992, 84.499))
# print(helper.lat[1171][922])
# print(helper.lon[1171][922])
# print(helper.slopes[1171][922])
# #landing site coordinates
# #-88.06245, 85.95728

#destination 1
#-87.99192, 84.49935
#print(helper.lat[832][1323])
#print(helper.lon[832][1323])

#destination 2
#-88.1407, 82.8148
#print(helper.lat[589][388])
#print(helper.lon[589][388])

#destination 3
#-88.08245, 88.17939
#print(helper.get_index(-88.082, 88.179))
#print(helper.lat[1630][824])
#print(helper.lon[1630][824])


#destination 4
#-88.05618, 98.12117
#print(helper.get_index(-88.056, 98.121))
# print(f"elevation =, {helper.elevation[3665][871]}")
# print(helper.azimuth[3665][871])s
# print(helper.lat[3665][871])
# print(helper.lon[3665][871])   

# # #destination 5
# #-88.05618, 98.12117
# print(helper.get_index(-88.041, 88.016))
# print(f"{helper.lat[1588][1076]}, {helper.lon[1588][1076]}, {helper.slopes[1588][1076]}")

# [1588][1076]

#print(helper.get_distance(point1=(832,1323), point2=(1171,922)))

#print(helper.azimuth[1171][922])
#print(helper.elevation[1171][922])
# print(helper.azimuth[1][1])
# print(helper.lat[0][0])
# print(helper.lon[0][0])

# print(f"Azimuth = {np.min(helper.azimuth)}, {np.max(helper.azimuth)}")
# print(f"Elevation = {np.min(helper.elevation)}, {np.max(helper.elevation)}")





