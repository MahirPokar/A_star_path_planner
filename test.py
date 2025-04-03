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

SIZE = 10



def is_outside(p):
    if p[0] < 0 or p[1] < 0:
        return True
    if p[0] >= SIZE or p[1] >= SIZE:
        return True
    return False


def get_neighbours(grid, node: Node, open_nodes, end):
    adjacent = [[1,0], [-1,0], [0,1], [0,-1]]
    for i in adjacent:
        p = (node.position[0] + i[0], node.position[1] + i[1])
        print(f"p values are {p}")
        if not is_outside(p): 
            print(p)
            if grid[p[0]][p[1]] == 1:  
                if not is_present(p, open_nodes):
                    temp_node = Node(position=(node.position[0] + i[0], node.position[1] + i[1]))
                    temp_node.parent = node
                    temp_node.h = abs(end[0] - temp_node.position[0]) + abs(end[0] - temp_node.position[1])
                    temp_node.g = node.g + 1
                    temp_node.f = temp_node.g + temp_node.h
                    open_nodes.append(temp_node)
            

def is_present(position, open_nodes):
    for i in open_nodes: 
        if i.position == position:
            return True
    return False


def create_grid():
        grid = [
            [1 for x in range(10)]
            for y in range(10)
        ]
        return grid

grid = create_grid()
reached = False
open_nodes = []
start_node = Node(position=(1,1))
end = (9,9)
# open_nodes.append(start_node)
closed_nodes = []
path = []
current_node = start_node
print(current_node)

while not reached:

    get_neighbours(grid, current_node, open_nodes, end)

    min_index = min(range(len(open_nodes)), key=lambda i: open_nodes[i].f)


    if open_nodes[min_index].h == 1:
        reached = True
        i = open_nodes[min_index]
        while True:
            path.append(i)
            if i.parent == start_node:
                print(path)
                break
            i = i.parent


    closed_nodes.append(open_nodes[min_index])


    open_nodes.pop(min_index)  

    current_node = closed_nodes[-1]

    







