# Import any libraries required
import random
from inspect import Parameter
import math


# The main path planning function. Additional functions, classes, 
# variables, libraries, etc. can be added to the file, but this
# function must always be defined with these arguments and must 
# return an array ('list') of coordinates (col,row).
#DO NOT EDIT THIS FUNCTION DECLARATION

class Node:

    def __init__(self, position = None, parent = None):

        self.position = position
        self.parent = parent

        self.g = 0 #DISTANCE FROM START
        self.h = 0 #DISTANCE TO END 
        self.f = 0

    def __str__(self):  
        return "(% s, % s)" % (self.position[0], self.position[1])
    
    def __repr__(self):  
        return "(% s, % s)" % (self.position[0], self.position[1])



def is_outside(p, COL, ROW):
    if p[0] < 0 or p[1] < 0:
        return True
    if p[0] >= (COL - 1) or p[1] >= (ROW - 1):
        return True
    return False


def is_present(position, open_nodes):
    for i in range(len(open_nodes)): 
        if open_nodes[i].position[0] == position[0] and open_nodes[i].position[1] == position[1]:
            return i 
    return False



def do_a_star(grid, start, end, display_message):
   
    print(f"end 0 is {end[0]}, end 1 is {end[1]}")
    print (f"start is {start}")

    # Get the size of the grid
    COL = len(grid)
    ROW = len(grid[0])

    start_node = Node(position=start)
    open_nodes = []
    closed_nodes = []
    reached = False
    path = []
    current_node = start_node
    adjacent_normals = [[1,0], [-1,0], [0,1], [0,-1]] 
   
    while not reached:
        for i in adjacent_normals:  
            p = (current_node.position[0] + i[0], current_node.position[1] + i[1])
            if p[0] < 0 or p[1] < 0:
                continue
            if p[0] > COL -1 or p[1] > ROW-1:
                continue
            if grid[p[0]][p[1]] == 1:
                j = is_present(p, open_nodes)
                k = is_present(p, closed_nodes)
                if j != 0:
                    if open_nodes[j].g > current_node.g + 1:
                        open_nodes[j].g = current_node.g + 1
                        open_nodes[j].parent = current_node
                        open_nodes[j].f = temp_node.g + temp_node.h
                if k != 0: 
                    if closed_nodes[k].g > current_node.g + 1:
                        closed_nodes[k].parent = current_node
                        closed_nodes[k].g = current_node.g + 1
                        closed_nodes[k].f = temp_node.g + temp_node.h
                else:
                    temp_node = Node(position=p)
                    temp_node.parent = current_node
                    temp_node.h = math.sqrt((end[0] - temp_node.position[0])**2 + (end[1] - temp_node.position[1])**2)
                    # print(f"temp current_node h = {temp_node.h} and temp node position = {temp_node.position}")
                    temp_node.g = current_node.g + 1
                    temp_node.f = temp_node.g + temp_node.h
                    open_nodes.append(temp_node)
      
        min_node = min(open_nodes, key=lambda x:x.f)
        
        if min_node.h == 1:
            reached = True
            i = min_node
            while True:
                path.append(i.position)
                if i.parent.position == start:
                    print(path)
                    print("boohakey")
                    break
                i = i.parent

        closed_nodes.append(min_node)

        open_nodes.remove(min_node)

        current_node = closed_nodes[-1]

    # Send the path points back to the gui to be displayed
    #FUNCTION MUST ALWAYS RETURN A LIST OF (col,row) COORDINATES
    return path

#end of file