import cv2
import numpy as np


def check_if_belongs(contour, left_top_corner, right_bottom_corner):
    for i in range(len(contour)):
        if left_top_corner[0] <= contour[i][0][0] <= right_bottom_corner[0] and left_top_corner[1] <= contour[i][0][1] \
                <= right_bottom_corner[1]:
            return True
    return False


def get_points_over_top_edge(contour, y):
    if y > 0:
        points = []
        for i in range(len(contour)):
            if contour[i][0][1] < y:
                tmp = [contour[i][0][0], contour[i][0][1]]
                points.append(tmp)
        return points
    else:
        return []


def get_points_below_bottom_edge(contour, y):
    if y < 480:
        points = []
        for i in range(len(contour)):
            if contour[i][0][1] > y:
                tmp = [contour[i][0][0], contour[i][0][1]]
                points.append(tmp)
        return points
    else:
        return []


def get_points_behind_left_edge(contour, x):
    if x > 0:
        points = []
        for i in range(len(contour)):
            if contour[i][0][0] < x:
                tmp = [contour[i][0][0], contour[i][0][1]]
                points.append(tmp)
        return points
    else:
        return []


def get_points_behind_right_edge(contour, x):
    if x < 480:
        points = []
        for i in range(len(contour)):
            if contour[i][0][0] > x:
                tmp = [contour[i][0][0], contour[i][0][1]]
                points.append(tmp)
        return points
    else:
        return []


def find_intersection(list1, list2):
    intersectiong_list = []

    for i in range(len(list1)):
        if list1[i] in list2:
            intersectiong_list.append(list1[i])

    return intersectiong_list


def get_contour_inside_area(contour, left_top_corner, right_bottom_corner):
    if check_if_belongs(contour, left_top_corner, right_bottom_corner):
        new_contour_elements = []

        points_over_top_edge = get_points_over_top_edge(contour, left_top_corner[1])
        points_below_bottom_edge = get_points_below_bottom_edge(contour, right_bottom_corner[1])
        points_behind_left_edge = get_points_behind_left_edge(contour, left_top_corner[0])
        points_behind_right_edge = get_points_behind_right_edge(contour, right_bottom_corner[0])

        left_top_corner_intersection = []
        if points_over_top_edge and points_behind_left_edge:
            left_top_corner_intersection = find_intersection(points_over_top_edge, points_behind_left_edge)

        right_top_corner_intersection = []
        if points_over_top_edge and points_behind_right_edge:
            right_top_corner_intersection = find_intersection(points_over_top_edge, points_behind_right_edge)

        left_bottom_corner_intersection = []
        if points_below_bottom_edge and points_behind_left_edge:
            left_bottom_corner_intersection = find_intersection(points_below_bottom_edge, points_behind_left_edge)

        right_bottom_corner_intersection = []
        if points_below_bottom_edge and points_behind_right_edge:
            right_bottom_corner_intersection = find_intersection(points_below_bottom_edge, points_behind_right_edge)

        # LEFT TOP CORNER
        if left_top_corner_intersection:
            new_contour_elements.append(left_top_corner)
            for i in range(len(contour)):
                if contour[i][0][0] > left_top_corner[0] and contour[i][0][1] > left_top_corner[1]:
                    new_contour_elements.append([contour[i][0][0], contour[i][0][1]])

        # RIGHT TOP CORNER
        elif right_top_corner_intersection:
            new_contour_elements.append([right_bottom_corner[0], left_top_corner[1]])
            for i in range(len(contour)):
                if contour[i][0][0] < right_bottom_corner[0] and contour[i][0][1] > left_top_corner[1]:
                    new_contour_elements.append([contour[i][0][0], contour[i][0][1]])

        # LEFT BOTTOM CORNER
        elif left_bottom_corner_intersection:
            new_contour_elements.append([left_top_corner[0], right_bottom_corner[1]])
            for i in range(len(contour)):
                if contour[i][0][0] > left_top_corner[0] and contour[i][0][1] < right_bottom_corner[1]:
                    new_contour_elements.append([contour[i][0][0], contour[i][0][1]])

        # RIGHT BOTTOM CORNER
        elif right_bottom_corner_intersection:
            new_contour_elements.append(right_bottom_corner)
            for i in range(len(contour)):
                if contour[i][0][0] < right_bottom_corner[0] and contour[i][0][1] < right_bottom_corner[1]:
                    new_contour_elements.append([contour[i][0][0], contour[i][0][1]])

        # OVER TOP EDGE
        elif points_over_top_edge:
            for i in range(len(contour)):
                tmp = [contour[i][0][0], contour[i][0][1]]
                if tmp not in points_over_top_edge:
                    new_contour_elements.append(tmp)

        # BELOW BOTTOM EDGE
        elif points_below_bottom_edge:
            for i in range(len(contour)):
                tmp = [contour[i][0][0], contour[i][0][1]]
                if tmp not in points_below_bottom_edge:
                    new_contour_elements.append(tmp)

        # BEHIND LEFT EDGE
        elif points_behind_left_edge:
            for i in range(len(contour)):
                tmp = [contour[i][0][0], contour[i][0][1]]
                if tmp not in points_behind_left_edge:
                    new_contour_elements.append(tmp)

        # BEHIND RIGHT EDGE
        elif points_behind_right_edge:
            for i in range(len(contour)):
                tmp = [contour[i][0][0], contour[i][0][1]]
                if tmp not in points_behind_right_edge:
                    new_contour_elements.append(tmp)

        else:
            return contour

        new_contour = np.array(new_contour_elements).reshape((-1, 1, 2)).astype(np.int32)
        return new_contour
    else:
        return []


def find_digital_game_array(contours, recognize_contour_type):
    array = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]

    for contour in range(len(contours)):
        for i in range(3):
            for j in range(3):
                contour_inside = get_contour_inside_area(contours[contour], [j * 160, i * 160],
                                                         [j * 160 + 160, i * 160 + 160])
                if len(contour_inside) > 0:
                    original_poly_participation = cv2.contourArea(contour_inside) / cv2.contourArea(contours[contour])
                    if original_poly_participation > 0.6:
                        array[i][j] = recognize_contour_type(contours[contour])
    return array
