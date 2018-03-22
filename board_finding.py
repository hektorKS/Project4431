import cv2
import numpy as np
import random

kernel = np.ones((5, 5), np.uint8)
minimalContourArea = 100

def delete_biggest_contour(contours):
    con = get_biggest_contour_index(contours)
    if con is not None and len(contours) > 1:
        contours.pop(con)


def get_biggest_contour_index(contours):
    con = None
    my_max = 0
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > my_max:
            my_max = cv2.contourArea(contours[i])
            con = i
    return con


def my_adaptive_canny(proc):
    _, contours, hierarchy = cv2.findContours(proc, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    threshold1 = 70
    threshold2 = 90
    while len(contours) < 1 and threshold1 > 40 and threshold2 > 60:
        _, contours, hierarchy = cv2.findContours(proc, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        threshold1 -= 10
        threshold2 -= 10
    return cv2.Canny(proc, threshold1, threshold2, 3)


def pre_process(image):
    result = cv2.GaussianBlur(image, (7, 7), 1)
    result = cv2.cvtColor(result, cv2.COLOR_BGRA2BGR)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    result = cv2.Canny(result, 50, 90, 3)
    result = cv2.adaptiveThreshold(result, 90, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    return result


def get_approx_poly(contour):
    epsilon = cv2.arcLength(contour, True) * 0.02
    return cv2.approxPolyDP(contour, epsilon, True)


def find_and_manipulate_contours(img):
    _, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    assert (len(contours) > 0)
    delete_biggest_contour(contours)
    contours = [x for x in contours if
                cv2.contourArea(x) > minimalContourArea]
    return contours


def random_color():
    levels = range(128, 256, 32)
    return tuple(random.choice(levels) for _ in range(3))


def draw_contours_on_blank(img, contours):
    h, w, _ = np.shape(img)
    blank = np.zeros((h, w, 3), np.uint8)
    biggest_contour_index = get_biggest_contour_index(contours)
    if biggest_contour_index is not None:
        cv2.drawContours(blank, [contours[biggest_contour_index]], -1, (120, 140, 170), 1)
    return blank


def try_to_cut_board_coords(processed, contours):
    c = get_biggest_contour_index(contours)
    while c is not None and len(contours) > 1:
        if check_if_contour_looks_like_board(processed, contours[c]):
            break
        delete_biggest_contour(contours)
        c = get_biggest_contour_index(contours)
    if c is None:
        pass
    else:
        c = contours[c]
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(processed, (x, y), (x + w, y + h), random_color(), 2)

    return x, y, w, h


def check_if_contour_looks_like_board(processed, contour):
    not_valid_rect_to_hull = 2
    not_valid_threshold_w_h_ratio = 2
    contour = get_approx_poly(contour)
    x, y, w, h = cv2.boundingRect(contour)
    hull = cv2.convexHull(contour)
    rect_hull_ratio = 0
    if cv2.contourArea(hull) != 0:
        rect_hull_ratio = (w * h) / cv2.contourArea(hull)
    if rect_hull_ratio > not_valid_rect_to_hull:
        return False
    _, contours, hierarchy = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if w / h > not_valid_threshold_w_h_ratio or h / w > not_valid_threshold_w_h_ratio:
        return False
    return True


def find_board(img_name):
    img_original = cv2.imread("./PlanszeWejsciowe/" + img_name)
    processed = pre_process(img_original)
    contours = find_and_manipulate_contours(processed)
    x, y, w, h = try_to_cut_board_coords(processed, contours)
    cropped = img_original[y: y + h, x: x + w]
    draw_contours_on_blank(img_original, contours)
    return cropped


def boards_finding(names):
    for i in range(len(names)):
        current_processing_name = names[i]
        found = find_board(current_processing_name)
        cv2.imwrite("./ZnalezionePlansze/" + names[i], found)
