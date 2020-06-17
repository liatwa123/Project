import string
from math import *


def dy(distance, m):
    return m * dx(distance, m)


def dx(distance, m):
    return distance / sqrt(m ** 2 + 1)


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


def build_edges2(shape):
    edges = []
    for i in range(0, len(shape)):
        edges.append(1)
    return edges


def build_shape2(shape, arr_dir):
    list_points = [[0, 0]]
    init_point_x = 0
    init_point_y = 0
    fin_point_x = 0
    fin_point_y = 0
    m = 0
    new_m = 0
    sum_ang = 0
    edges = build_edges2(shape)
    if arr_dir[0] == 1:
        fin_point_x = edges[0]
    else:
        fin_point_x = -edges[0]
    list_points.append([fin_point_x, fin_point_y])

    for i in range(0, len(shape)-1):
        if shape[i][1] > 90 or shape[i][1] == 60:
            new_m = (-m - tan(radians(shape[i][1]))) / (m * tan(radians(shape[i][1])) - 1)
        else:
            new_m = (m - tan(radians(shape[i][1]))) / (m * tan(radians(shape[i][1])) + 1)

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

        fin_point_x = round(fin_point_x, 3)
        fin_point_y = round(fin_point_y, 3)
        if [fin_point_x, fin_point_y] in list_points and i != len(shape) - 2:
            return False

        list_points.append([fin_point_x, fin_point_y])
        sum_ang = sum_ang + abs(shape[i][1])
        m = new_m

    sum_ang = sum_ang + abs(shape[len(shape) - 1][1])
    sum_theoretical = 180*(len(shape)-2)

    if fin_point_x == init_point_x and fin_point_y == init_point_y and sum_theoretical == abs(sum_ang):
        return True
    else:
        return False


def main():
    # n = degrees(atan(0.75))
    build_shape2([[1,60,2], [2, 60, 3], [3, 300, 4], [4, 60, 5], [5, 60, 6], [6, 180, 1]], [1, 2, 2, 2, 2, 1])


if __name__ == '__main__':
    main()



