
from __future__ import division
import math
import random
import pickle
import sys
from helper import Helper
import hickle as hk
import time


landing = (1171, 922)
destinations = [(832,1323), (589,388), (1630,824), (3427,820), (1588,1076)]

REL_PATH_SEARCH = './assets/paths/'
PATH_FILES = [REL_PATH_SEARCH + 'fra_dest{}_shortest.pkl',
              REL_PATH_SEARCH + 'fra_dest{}_lhc.pkl',
              REL_PATH_SEARCH + 'fra_dest{}_slope_20.pkl']

helper = Helper()


import heapq

class PriorityQueue():
    """Implementation of a priority queue 
    to store nodes during search."""
    
    def __init__(self):
        self.queue = []
        self.current = 0    

    def next(self):
        if self.current >=len(self.queue):
            self.current
            raise StopIteration
    
        out = self.queue[self.current]
        self.current += 1

        return out

    def pop(self):
        return heapq.heappop(self.queue)
        
    def remove(self, nodeId):
        for i in range(self.size()):
            if self.queue[i][1] == nodeId:
                self.queue = self.queue[:i] + self.queue[i+1:]
                heapq.heapify(self.queue)
                break

    def __iter__(self):
        return self

    def __str__(self):
        return 'PQ:[%s]'%(', '.join([str(i) for i in self.queue]))

    def append(self, node):
        heapq.heappush(self.queue, node)
        
    def __contains__(self, key):
        self.current = 0
        return key in [n for v,n in self.queue]

    def __eq__(self, other):
        return self == other

    def size(self):
        return len(self.queue)
    
    def clear(self):
        self.queue = []
        
    def top(self):
        return self.queue[0]

    __next__ = next

def euclidean_dist_heuristic(graph, v, goal):
    """Return the Euclidean distance from
    node v to the goal."""
    
    distance = helper.get_distance(v, goal)
    return distance

def slope_heuristic(graph, v, goal):
    """Return the Euclidean distance from
    node v to the goal."""
    
    slope_diff = helper.get_slope(v, goal)
    return slope_diff

def a_star(graph, start, goal, heuristic):
    """Run A* search from the start to
    goal using the specified heuristic
    function, and return the final path."""
    
    if start == goal:
        return []
    
    hcosts = {}
    vcosts = {}
    frontier = PriorityQueue()
    hcost = heuristic(graph, start, goal)
    frontier.append((hcost, start))
    hcosts[start] = hcost
    vcosts[start] = 0
    
    prev = {}
    
    while frontier.size() > 0:
        fcost, node = frontier.pop()
        if node == goal:
            break
        
        for neighbor in graph.neighbors(node):
            if neighbor not in graph.get_explored_nodes():
                if neighbor not in frontier:
                    vcosts[neighbor] = vcosts[node] + graph.edges[node,neighbor]['distance']
                    hcosts[neighbor] = heuristic(graph, neighbor, goal)
                    frontier.append((vcosts[neighbor] + hcosts[neighbor], neighbor))
                    prev[neighbor] = node
                if neighbor in frontier and vcosts[node] + graph.edges[node,neighbor]['distance'] < vcosts[neighbor]:
                    frontier.remove(neighbor)
                    vcosts[neighbor] = vcosts[node] + graph.edge[node][neighbor]['weight']
                    hcosts[neighbor] = heuristic(graph, neighbor, goal)
                    frontier.append((vcosts[neighbor] + hcosts[neighbor], neighbor))
                    prev[neighbor] = node

    path = []
    prev_node = goal
    while prev_node != start:
        path = [prev_node] + path
        prev_node = prev[prev_node]
    path = [start] + path
    return path



def bidirectional_a_star(graph, start, goal, heuristic, file_name):
    """Run bidirectional A* search between
    start and goal."""

    start_time = time.time() 
    
    if start == goal:
        return []
    
    frt1 = PriorityQueue()
    frt2 = PriorityQueue()
    
    prev1 = {}
    prev2 = {}
    
    explored1 = set()
    explored2 = set()
    
    vcosts1 = {start: 0}
    vcosts2 = {goal: 0}
    
    tot = heuristic(graph, start, goal)
    
    def h(v, forward=True):
        fv, rv = heuristic(graph, v, goal), heuristic(graph, start, v)
        if forward:
            return 0.5 * (fv - rv) + 0.5 * tot
        else:
            return 0.5 * (rv - fv) + 0.5 * tot
    
    hcosts1 = {start: h(start)}
    hcosts2 = {goal: h(goal, False)}

    frt1.append((0, start))
    frt2.append((0, goal))
    
    def get_path(prev, start, goal, reverse=False):
        path = []
        if start == goal:
            return path
        if not reverse:
            prev_node = goal
            while prev_node != start:
                path = [prev_node] + path
                prev_node = prev[prev_node]
            path = [start] + path
        else:
            next_node = start
            while next_node != goal:
                path.append(next_node)
                next_node = prev[next_node]
            path.append(goal)
        return path
        
    def combine_path(node):
        if node == start:
            return get_path(prev2, node, goal, True)
        if node == goal:
            return get_path(prev1, start, node)
        path1 = get_path(prev1, start, node)
        path2 = get_path(prev2, node, goal, True)
        return path1[:-1] + path2
        
    min_cost = float('Inf')
    path = []
    
    def add_neighbors(node, frt, explored, other_explored, vcosts, other_vcosts, hcosts, prev, min_cost, path, forward=True):

        for ngbr in graph.neighbors(node):
            if ngbr not in explored:
                if ngbr not in frt:
                    vcosts[ngbr] = vcosts[node] + graph.edges[node,ngbr]['distance']
                    hcosts[ngbr] = h(ngbr, forward)
                    frt.append((vcosts[ngbr] + hcosts[ngbr], ngbr))
                    prev[ngbr] = node
                if ngbr in frt and vcosts[node] + graph.edges[node,ngbr]['distance'] < vcosts[ngbr]:
                    frt.remove(ngbr)
                    vcosts[ngbr] = vcosts[node] + graph.edges[node,ngbr]['distance']
                    hcosts[ngbr] = h(ngbr, forward)
                    frt.append((vcosts[ngbr] + hcosts[ngbr], ngbr))
                    prev[ngbr] = node
                    
                if ngbr in other_explored and vcosts[ngbr] + other_vcosts[ngbr] < min_cost:
                    min_cost = vcosts[ngbr] + other_vcosts[ngbr]
                    path = combine_path(ngbr)
        return min_cost, path
        
    while frt1.size() > 0 and frt2.size() > 0:
        fcost1, node1 = frt1.pop()
        fcost2, node2 = frt2.pop()
        
        if fcost1 + fcost2 >= min_cost + tot:
            break
        
        explored1.add(node1)
        explored2.add(node2)
        
        min_cost, path = add_neighbors(node1, frt1, explored1, explored2, vcosts1, vcosts2, hcosts1, prev1, min_cost, path)
        min_cost, path = add_neighbors(node2, frt2, explored2, explored1, vcosts2, vcosts1, hcosts2, prev2, min_cost, path, False)

    
    end_time = time.time()  # Get end time
    elapsed_time = end_time - start_time  
    print(f"Bidirectional AStar Execution time: {elapsed_time} seconds")
    
    hk.dump(path, file_name)  
    return path


def bidirectional_a_star_slope(graph, start, goal, heuristic, file_name):
    """Run bidirectional A* search between
    start and goal."""

    start_time = time.time() 
    
    if start == goal:
        return []
    
    frt1 = PriorityQueue()
    frt2 = PriorityQueue()
    
    prev1 = {}
    prev2 = {}
    
    explored1 = set()
    explored2 = set()
    
    vcosts1 = {start: 0}
    vcosts2 = {goal: 0}
    
    tot = heuristic(graph, start, goal)
    
    def h(v, forward=True):
        fv, rv = heuristic(graph, v, goal), heuristic(graph, start, v)
        if forward:
            return 0.5 * (fv - rv) + 0.5 * tot
        else:
            return 0.5 * (rv - fv) + 0.5 * tot
    
    hcosts1 = {start: h(start)}
    hcosts2 = {goal: h(goal, False)}

    frt1.append((0, start))
    frt2.append((0, goal))
    
    def get_path(prev, start, goal, reverse=False):
        path = []
        if start == goal:
            return path
        if not reverse:
            prev_node = goal
            while prev_node != start:
                path = [prev_node] + path
                prev_node = prev[prev_node]
            path = [start] + path
        else:
            next_node = start
            while next_node != goal:
                path.append(next_node)
                next_node = prev[next_node]
            path.append(goal)
        return path
        
    def combine_path(node):
        if node == start:
            return get_path(prev2, node, goal, True)
        if node == goal:
            return get_path(prev1, start, node)
        path1 = get_path(prev1, start, node)
        path2 = get_path(prev2, node, goal, True)
        return path1[:-1] + path2
        
    min_cost = float('Inf')
    path = []
    
    def add_neighbors(node, frt, explored, other_explored, vcosts, other_vcosts, hcosts, prev, min_cost, path, forward=True):

        for ngbr in graph.neighbors(node):
            if ngbr not in explored:
                if ngbr not in frt:
                    vcosts[ngbr] = vcosts[node] + graph.edges[node,ngbr]['slope']
                    hcosts[ngbr] = h(ngbr, forward)
                    frt.append((vcosts[ngbr] + hcosts[ngbr], ngbr))
                    prev[ngbr] = node
                if ngbr in frt and vcosts[node] + graph.edges[node,ngbr]['slope'] < vcosts[ngbr]:
                    frt.remove(ngbr)
                    vcosts[ngbr] = vcosts[node] + graph.edges[node,ngbr]['slope']
                    hcosts[ngbr] = h(ngbr, forward)
                    frt.append((vcosts[ngbr] + hcosts[ngbr], ngbr))
                    prev[ngbr] = node
                    
                if ngbr in other_explored and vcosts[ngbr] + other_vcosts[ngbr] < min_cost:
                    min_cost = vcosts[ngbr] + other_vcosts[ngbr]
                    path = combine_path(ngbr)
        return min_cost, path
        
    while frt1.size() > 0 and frt2.size() > 0:
        fcost1, node1 = frt1.pop()
        fcost2, node2 = frt2.pop()
        
        if fcost1 + fcost2 >= min_cost + tot:
            break
        
        explored1.add(node1)
        explored2.add(node2)
        
        min_cost, path = add_neighbors(node1, frt1, explored1, explored2, vcosts1, vcosts2, hcosts1, prev1, min_cost, path)
        min_cost, path = add_neighbors(node2, frt2, explored2, explored1, vcosts2, vcosts1, hcosts2, prev2, min_cost, path, False)

    
    end_time = time.time()  # Get end time
    elapsed_time = end_time - start_time  
    print(f"Bidirectional AStar SLope Execution time: {elapsed_time} seconds")
    
    hk.dump(path, file_name)  
    return path


    
print("Start Loading") 
with open('fra_slope15.hkl', 'rb') as f:
    G_15 = hk.load(f)
    
with open('fra_slope20.hkl', 'rb') as f:
    G_20 = hk.load(f)
    
print("Graphs loaded")  

j = 0
for i in range(4):
    
    path = PATH_FILES[j]
    file_name = path.replace('{}', str(i+1))
    bidirectional_a_star(G_15, landing, destinations[i], euclidean_dist_heuristic, file_name)
        
        #print("path =", path)
    
    path = PATH_FILES[j+1]
    file_name = path.replace('{}', str(i+1))
    bidirectional_a_star_slope(G_15, landing, destinations[i],  slope_heuristic, file_name)
        #print("path =", path)
        
    path = PATH_FILES[j+2]
    file_name = path.replace('{}', str(i+1))
        #bidirectional_a_star(G_20, landing, destinations[i], euclidean_dist_heuristic, file_name)
    bidirectional_a_star(G_20, landing, destinations[i],  euclidean_dist_heuristic, file_name)


