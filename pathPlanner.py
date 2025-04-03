def do_a_star(grid, start, end, display_message):
    """
    Perform an A* path search on a grid from a start cell to an end cell.

    This version uses Euclidean distance as the heuristic to guide expansion. 
    Movement is limited to up, down, left, and right neighbors (4-direction).
    Each movement step has a uniform cost of 1, regardless of direction.
    
    Args:
        grid (list of lists): 2D occupancy grid, where 1 = free, 0 = obstacle.
                              Accessed via grid[col][row].
        start (tuple): (start_col, start_row) for the start cell (0-based).
        end (tuple): (end_col, end_row) for the goal cell (0-based).
        display_message (callable): Callback for printing debug/info messages to the GUI.
    
    Returns:
        list of (int, int): The path as a list of (col, row) coordinates from 'start' to 'end',
                            or an empty list if no valid path is found.
    """
    # Determine the grid's overall dimensions
    COL = len(grid)
    ROW = len(grid[0]) if COL > 0 else 0

    # Unpack start/end coordinates for easier reading
    start_col, start_row = start
    end_col, end_row = end

    # --- Basic Validity Checks ---
    # We exit early if the start/end cell is out-of-bounds or if it's blocked.
    # This avoids wasted computation and prevents index errors or invalid searches.
    if (start_col < 0 or start_col >= COL or 
        start_row < 0 or start_row >= ROW or
        end_col   < 0 or end_col   >= COL or 
        end_row   < 0 or end_row   >= ROW):
        display_message("Error: Start or end is out of grid bounds.")
        return []
    if grid[start_col][start_row] == 0:
        display_message("Error: Start cell is blocked.")
        return []
    if grid[end_col][end_row] == 0:
        display_message("Error: End cell is blocked.")
        return []

    # We store the best-known cost (from 'start') to each visited cell in g_score.
    # Keys = (col, row), Values = cost so far.
    g_score = {}
    g_score[(start_col, start_row)] = 0

    # came_from is used to trace back the path once we reach the goal.
    # came_from[(c, r)] = (parent_c, parent_r)
    came_from = {}

    # open_list holds the set of cells we still need to explore.
    # We'll choose the next cell by scanning for the one with the lowest F = G + H.
    open_list = [(start_col, start_row)]

    # Basic 4-direction movement (N, S, E, W). Diagonals not included here.
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    
    display_message("Starting A* search with Euclidean distance heuristic...")

    while open_list:
        # ----------------------------------------------------------
        # Find the cell in open_list with the smallest F = G + H:
        #     - G is cost so far (g_score).
        #     - H is Euclidean distance to the goal.
        #
        # We do a linear scan here due to the no-extra-library constraint. 
        # This is simpler but slower than a priority queue for large grids.
        # ----------------------------------------------------------
        current = None
        current_f_score = None
        
        for cell in open_list:
            c, r = cell
            # g_score[(c, r)] = cost to reach (c, r) from start.
            g_val = g_score[(c, r)]
            # H is the heuristic used to guide the search: Euclidean distance
            h_val = euclidean_distance(c, r, end_col, end_row)
            f_val = g_val + h_val
            # If this is our first cell or it has a lower F-score, update current
            if current is None or f_val < current_f_score:
                current = cell
                current_f_score = f_val

        # If we've reached the goal, we reconstruct and return the path
        if current == (end_col, end_row):
            display_message("Goal reached! Reconstructing path...")
            return reconstruct_path(came_from, start, (end_col, end_row))

        # Remove 'current' from the open list so we don't expand it again
        open_list.remove(current)
        
        current_col, current_row = current

        # ----------------------------------------------------------
        # Explore the valid neighbors of 'current' (up, down, left, right).
        # For each neighbor, check if we've found a cheaper route from start.
        # ----------------------------------------------------------
        for dc, dr in directions:
            nb_col = current_col + dc
            nb_row = current_row + dr
            
            # Skip neighbors that lie outside the grid or on obstacles
            if (0 <= nb_col < COL and 0 <= nb_row < ROW and grid[nb_col][nb_row] == 1):
                # Each valid step from one cell to another costs 1
                tentative_g = g_score[current] + 1

                # If neighbor not visited or we've found a cheaper path to it, update it
                if (nb_col, nb_row) not in g_score or tentative_g < g_score[(nb_col, nb_row)]:
                    g_score[(nb_col, nb_row)] = tentative_g
                    came_from[(nb_col, nb_row)] = (current_col, current_row)
                    # If it's a newly discovered or improved cell, ensure it's in open_list
                    if (nb_col, nb_row) not in open_list:
                        open_list.append((nb_col, nb_row))

    # If we exhaust the open list without ever reaching the goal, no path exists
    display_message("No path found with A*.")
    return []


def euclidean_distance(col1, row1, col2, row2):
    """
    Compute the straight-line (Euclidean) distance between two grid cells.

    Even though the cost of each step is uniform, using Euclidean distance 
    encourages the search to expand cells that are closer (in a straight line)
    to the goal. This can produce more direct expansions than using Manhattan 
    distance in some cases.
    """
    dx = col1 - col2
    dy = row1 - row2
    return (dx*dx + dy*dy) ** 0.5


def reconstruct_path(came_from, start, goal):
    """
    Rebuild a path from goal back to the start using 'came_from' data.

    This function walks backward from the goal cell, following each cell's 
    recorded parent until it reaches the start cell. Once reconstructed, the 
    path is reversed to produce a forward-facing route (start -> goal).

    Args:
        came_from (dict): Mapping of cell -> parent cell, built during the search.
        start (tuple):    The start coordinate (col, row).
        goal (tuple):     The goal coordinate (col, row).

    Returns:
        A list of (col, row) cells describing the path from 'start' to 'goal'.
    """
    path = []
    current = goal

    # Climb the chain of parents until we return to the start
    while current != start:
        path.append(current)
        current = came_from[current]
    
    # Finally add the start cell, then reverse for proper ordering
    path.append(start)
    path.reverse()
    return path
