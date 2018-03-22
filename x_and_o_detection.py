from finding_digital_game_array import *
import globals


def get_approx_poly(contour):
    epsilon = 0.05 * cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, epsilon, True)


def recognize_contour_type(contour):
    poly = get_approx_poly(contour)
    is_convex = cv2.isContourConvex(poly)
    contour_type = "unknown"
    if is_convex:
        contour_type = "o"
    elif not is_convex:
        contour_type = "x"

    return contour_type


def get_color(contour_type):
    if contour_type == "o":
        return 255, 0, 0
    elif contour_type == "x":
        return 0, 255, 0
    else:
        return 0, 0, 255


def draw_contours_on_image(image_to_process, contours):
    for c in contours:
        contour_type = recognize_contour_type(c)
        cv2.drawContours(image_to_process, [c], -1, color=get_color(contour_type), thickness=2)

    return image_to_process


def find_maxes(data, how_many):
    tmp_list = data.copy()
    tmp_list.sort()
    return tmp_list[-how_many:]


def find_biggest_contours_indices(contours, how_many):
    sizes = []
    indices = []

    for i in range(len(contours)):
        sizes.append(cv2.contourArea(contours[i]))

    maxes = find_maxes(sizes, how_many)

    for i in range(how_many):
        indices.append(sizes.index(maxes[i]))
    return indices


def filter_contours(contour_vector, hierarchy_vector, how_many_biggest_to_ignore):
    if 0 < how_many_biggest_to_ignore <= len(contour_vector):
        contours = []

        indices = find_biggest_contours_indices(contour_vector, how_many_biggest_to_ignore)

        for i in range(len(contour_vector)):
            if cv2.contourArea(contour_vector[i]) > 300:
                if i in indices:
                    continue
                elif hierarchy_vector[0][i][3] in indices:
                    contours.append(contour_vector[i])
        return contours
    else:
        return contour_vector


def find_contours(img, how_many_biggest_to_ignore):
    _, contour_vector, hierarchy_vector = cv2.findContours(image=img, mode=cv2.RETR_TREE,
                                                           method=cv2.CHAIN_APPROX_SIMPLE)

    contours = filter_contours(contour_vector, hierarchy_vector, how_many_biggest_to_ignore)

    return contours


def pre_processing(img):
    img = cv2.pyrMeanShiftFiltering(src=img, sp=11, sr=43)

    img = cv2.GaussianBlur(img, (7, 7), 1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

    img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    kernel = np.ones((5, 5), np.uint8)

    img = cv2.erode(img, kernel)

    return img


def build_around_to_500(img):
    new_img = np.ones((500, 500), np.uint8)
    new_img.fill(255)

    counter = 0
    for i in range(len(new_img)):
        if 10 <= i < 490:
            new_img[i][10:490] = img[counter]
            counter += 1
    return new_img


def move_contours_back_to_480(contours):
    for i in range(len(contours)):
        for j in range(len(contours[i])):
            contours[i][j][0][0] -= 10
            contours[i][j][0][1] -= 10

    return contours


def x_and_o_detection(names):
    games_arrays = []
    for i in range(len(names)):
        original_image = cv2.imread("./ZnalezionePlansze/" + names[i])

        resized_original_image = cv2.resize(original_image, (480, 480))

        img = pre_processing(resized_original_image)

        img = build_around_to_500(img)

        contours = find_contours(img, 3)
        contours = move_contours_back_to_480(contours)

        game_array = find_digital_game_array(contours, recognize_contour_type)

        is_correct, number_of_mistakes = globals.check_correctness(game_array, names[i])
        if is_correct:
            print("Poprawnie wykryto: ", names[i])
            globals.number_of_correctly_identified_fields += 9
            globals.correctly_identified += 1
            globals.correctly_identified_names.append(names[i])
            globals.mistake_array[number_of_mistakes] += 1
        else:
            print("Niepoprawnie wykryto: ", names[i])
            print("Ilość pomyłek na tej planszy: ", number_of_mistakes)
            globals.number_of_incorrectly_identified_fields = \
                globals.number_of_incorrectly_identified_fields + number_of_mistakes
            globals.number_of_correctly_identified_fields += 9 - number_of_mistakes
            globals.incorrectly_identified += 1
            globals.incorrectly_identified_names.append(names[i])
            globals.mistake_array[number_of_mistakes] += 1

        if not globals.argument_from_command_line:
            print(names[i])
            for k in game_array:
                print(k)
        games_arrays.append(game_array)
        original_image_with_contours = draw_contours_on_image(resized_original_image, contours)
        cv2.imwrite("./WynikiPrzetwarzania/" + names[i], original_image_with_contours)
    return games_arrays
