import string
from math import *

# This function calculates the change in y's value, given the slope value (m) and the edge length (distance)

def dy(distance, m):
    return m * dx(distance, m)

# This function calculates the change in x's value, given the slope value (m) and the edge length (distance)

def dx(distance, m):
    return distance / sqrt(m ** 2 + 1)

"""
def build_edges(arr_len):
    edges = []
    count = 0
    for i in range(0, len(arr_len)):
        if arr_len[i] == -1:
            edges.append(count)
            count = 0
        else:
            count = count + 1
    return edges
   

def build_shape(arr_len, arr_ang, arr_dir):
    init_point_x = 0
    init_point_y = 0
    fin_point_x = 0
    fin_point_y = 0
    m = 0
    new_m = 0
    sum_ang = 0
    edges = build_edges(arr_len)
    if arr_dir[0] == 1:
        fin_point_x = edges[0]
    else:
        fin_point_x = -edges[0]
    for i in range(0, len(arr_ang)-1):
        if arr_ang[i] > 90 or arr_ang[i] == 60:
            new_m = (-m - tan(radians(arr_ang[i]))) / (m * tan(radians(arr_ang[i])) - 1)
        else:
            new_m = (m - tan(radians(arr_ang[i]))) / (m * tan(radians(arr_ang[i])) + 1)

        if arr_dir[i+1] == 1:
            if new_m > e**15 or new_m < -e ** 16:
                fin_point_y = fin_point_y + edges[i+1]
            else:
                fin_point_x = fin_point_x + dx(edges[i+1], new_m)
                fin_point_y = fin_point_y + dy(edges[i+1], new_m)

        elif arr_dir[i+1] == 2:
            if new_m > e**15 or new_m < -e ** 16:
                fin_point_y = fin_point_y - edges[i+1]
            else:
                fin_point_x = fin_point_x - dx(edges[i+1], new_m)
                fin_point_y = fin_point_y - dy(edges[i+1], new_m)

        sum_ang = sum_ang + abs(arr_ang[i])
        m = new_m

    sum_ang = sum_ang + abs(arr_ang[len(arr_ang) - 1])
    if abs(fin_point_x) < e**(-15):
        fin_point_x = 0
    if abs(fin_point_y) < e**(-15):
        fin_point_y = 0

    sum_theoretical = 180*(len(arr_ang)-2)

    if fin_point_x == init_point_x and fin_point_y == init_point_y and sum_theoretical == abs(sum_ang):
        return True
    else:
        return False
"""

def build_edges2(shape):
    # This function returns a matchsticks array; Every matchstick is represented by the integer '1' - 1 length unit
    edges = []
    for i in range(0, len(shape)):
        edges.append(1)
    return edges


def build_shape2(shape, arr_dir):
    """
    This function calculates the shape's points. Using the list of points (coordinates), the function determines if the shape is a polygon:
    For each new point: the new point must not be in the list of previous points. (Except for the last point)
    The sum of angles must be: 180 * (number of matchsticks - 2)
    Last point's x = First point's x , Last point's y = First point's y
    Every point is a matchstick head's location, represented by [x,y].
    The function gets:
    The shape - represented by a 2-D array:
    Every row represents a junction between 2 matchsticks
    Each row includes 3 matchsticks: indices 0,2 represent the matchsticks and index 1 represents the angle between them.
    Area units: the shape's area can be divided to 1-match-length squares or 1-match-length triangles.
    The angles of the shape must be: 0,90,180,270 or: 0,60,120,180,240,300.
    Every matchstick has an index - an integer between 1 - (# of matchsticks)

    """
    list_points = [[0, 0]]
    init_point_x = 0
    init_point_y = 0
    fin_point_x = 0
    fin_point_y = 0
    m = 0 # old slope
    new_m = 0 # new_slope
    sum_ang = 0
    edges = build_edges2(shape) # array of 1's, length: same as the shape's number of matchsticks
                                # the first edge is parallel to axis line X
    if arr_dir[0] == 1:
        fin_point_x = edges[0]
    else:
        fin_point_x = -edges[0]
    list_points.append([fin_point_x, fin_point_y])
    
    # slope calculation
    for i in range(0, len(shape)-1):
        if shape[i][1] > 90 or shape[i][1] == 60:
            new_m = (-m - tan(radians(shape[i][1]))) / (m * tan(radians(shape[i][1])) - 1)
        else:
            new_m = (m - tan(radians(shape[i][1]))) / (m * tan(radians(shape[i][1])) + 1)

        if arr_dir[i+1] == 1:                                         # 1 : if the slope is not inf or -inf, the next point's x > the current point's x
                                                                      # otherwise: the next point's y > the current point's y
                
            if new_m > e**15 or new_m < -e ** 16:                     # new slope is: inf or -inf
                fin_point_y = fin_point_y + edges[i+1]                # calculating the new coordinates
            else:                                                     # new slope is not inf or -inf
                fin_point_x = fin_point_x + dx(edges[i+1], new_m)     # calculating the new coordinates
                fin_point_y = fin_point_y + dy(edges[i+1], new_m)

        elif arr_dir[i+1] == 2:                                       # 2 : if the slope is not inf or -inf, the next point's x < the current point's x
                                                                      # otherwise: the next point's y < the current point's y
                
            if new_m > e**15 or new_m < -e ** 16:                     # new slope is: inf or -inf
                fin_point_y = fin_point_y - edges[i+1]                # calculating the new coordinates
            else:                                                     # new slope is not inf or -inf
                fin_point_x = fin_point_x - dx(edges[i+1], new_m)     # calculating the new coordinates
                fin_point_y = fin_point_y - dy(edges[i+1], new_m)

        fin_point_x = round(fin_point_x, 3)
        fin_point_y = round(fin_point_y, 3)
        # For each new point: the new point must not be in the list of previous points. (Except for the last point)
        if [fin_point_x, fin_point_y] in list_points and i != len(shape) - 2:
            return False

        list_points.append([fin_point_x, fin_point_y])
        sum_ang = sum_ang + abs(shape[i][1])                          # calculating the sum of angles
        m = new_m

    sum_ang = sum_ang + abs(shape[len(shape) - 1][1])                 # calculating the sum of angles
    sum_theoretical = 180*(len(shape)-2)
    
    # Returns 'True' if:
    # For each new point: the new point is not in the list of previous points (except for the last point)
    # The theoretical angles sum equals the current angles sum
    # Else: False
    if fin_point_x == init_point_x and fin_point_y == init_point_y and sum_theoretical == abs(sum_ang):
        return True
    else:
        return False


def main():
    # n = degrees(atan(0.75))
    build_shape2([[1,60,2], [2, 60, 3], [3, 300, 4], [4, 60, 5], [5, 60, 6], [6, 180, 1]], [1, 2, 2, 2, 2, 1])


if __name__ == '__main__':
    main()



