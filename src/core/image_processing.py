import os
import cv2 as cv
import numpy as np

def process_image(images_paths, dir):
    dir = f"{dir}/report"
    report_photos_paths = []
    if not os.path.exists(dir):
        os.makedirs(dir)
    for i in range(len(images_paths)):
        print("here")
        img = cv.imread(images_paths[i])
        result_photo = orange_points_algorithm(preprocess_image(img))
        save_photo(f"{dir}/photo_report{i}.png", result_photo)
        report_photos_paths.append(f"{dir}/photo_report{i}.png")
    return report_photos_paths



def preprocess_image(image):
    print('tu')
    resized_image = cv.resize(image, (400, 700), interpolation=cv.INTER_AREA)
    return resized_image

def orange_points_algorithm(image):
    # Algorytm wybierający pomarańczowe punkty
    b, g, r = cv.split(image)
    dif_img = cv.subtract(r, b)

    # Binaryzacja obrazu, aby wyostrzyć jasne punkty na ciemnym tle
    _, threshold = cv.threshold(dif_img, 100, 255, cv.THRESH_BINARY)
    median_filtered = cv.medianBlur(threshold, 7)

    # Dylatacja i erozja
    kernel = np.ones((12, 10), np.uint8)
    kernel2 = np.ones((4, 4), np.uint8)
    dilate = cv.dilate(median_filtered, kernel, iterations=1)
    erode = cv.erode(dilate, kernel2, iterations=1)

    # Znajdowanie konturów na obrazie
    contours, _ = cv.findContours(erode, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Określenie minimalnej powierzchni konturu, aby uznać go za "mały"
    min_contour_area = 600

    # Usuwanie dużych obszarów
    filtered_contours = [cnt for cnt in contours if cv.contourArea(cnt) < min_contour_area]

    # Tworzenie maski dla filtracji konturów
    filtered_mask = np.zeros_like(erode)
    print("przd")
    cv.drawContours(filtered_mask, filtered_contours, -1, 255, thickness=cv.FILLED)
    print("po")

    # Filtracja obrazu
    filtered_image = cv.bitwise_and(erode, filtered_mask)

    # Wyświetlanie przefiltrowanego obrazu
    cv.imshow('Filtered image', filtered_image)

    # Ograniczenie obszaru za pomocą roi
    shape = image.shape
    center_x, center_y = shape[1] // 2, shape[0] // 2

    roi_size1 = 470
    roi_size2 = 200

    roi = filtered_image[center_y - roi_size1 // 3:center_y + 2 * (roi_size1 // 3),
          center_x - roi_size2 // 2:center_x + roi_size2 // 2]

    cv.imshow("ROI", roi)

    # Funkcja podobna do border_kill
    roi = clear_border_objects(roi)

    cv.imshow('r', roi)

    # Wyszukanie konturów na binarnym obrazie
    contours, _ = cv.findContours(roi, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    result_img_with_contours = image.copy()

    # Filtracja i rysowanie tylko tych konturów, które są wystarczająco duże
    min_contour_area = 30
    max_contour_area = 400
    centers = []

    for contour in contours:
        area = cv.contourArea(contour)

        if min_contour_area < area < max_contour_area:
            contour_offset = contour + [center_x - (roi_size2 // 2), center_y - roi_size1 // 3]
            cv.drawContours(result_img_with_contours, [contour_offset], -1, (0, 0, 255), 2)

            # Oblicz współrzędne środka konturu na podstawie momentu zerowego(m00) oraz pierwszego rzędu dla osi X i Y
            M = cv.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"]) + center_x - (roi_size2 // 2)
                cY = int(M["m01"] / M["m00"]) + center_y - roi_size1 // 3
                centers.append((cX, cY))

    # Iteracja przez punkty i rysowanie żółtych kropek na result_img_with_contours
    for point in centers:
        x, y = point[0], point[1]
        cv.circle(result_img_with_contours, (x, y), 5, (0, 255, 255), -1)

    # Sortowanie punktów
    sorted_points = sorted(centers, key=lambda center: center[1])

    positions_to_ignore = [2, 5]

    for i in range(0, len(sorted_points) - 1, 2):
        if i in positions_to_ignore:
            i = i + 1
        elif i + 1 in positions_to_ignore:
            continue
        if sorted_points[i][0] > sorted_points[i + 1][0]:
            sorted_points[i], sorted_points[i + 1] = sorted_points[i + 1], sorted_points[i]

    print(sorted_points)

    # Rysowanie linii
    draw_lines(result_img_with_contours, sorted_points)

    # Wyświetlanie końcowego obrazu z konturami i liniami
    cv.imshow('Result Image with Contours', result_img_with_contours)

    return result_img_with_contours


def clear_border_objects(binary_image, border_size=10):
    # Tworzenie maski krawędzi
    border_mask = np.zeros_like(binary_image)
    border_mask[:border_size, :] = 255
    border_mask[-border_size:, :] = 255
    border_mask[:, :border_size] = 255
    border_mask[:, -border_size:] = 255

    # Usunięcie obiektów przecinających krawędzie
    cleaned_image = cv.bitwise_and(binary_image, cv.bitwise_not(border_mask))

    return cleaned_image

def draw_lines(result_img_with_contours, sorted_points):
    # Rysowanie linii
    l1_direction = [3, 2, 1, 4]
    l2_direction = [0, 5, 6, 8, 10]
    l3_direction = [5, 7, 9, 11]

    for i in range(4):
        cv.line(result_img_with_contours, sorted_points[l2_direction[i]], sorted_points[l2_direction[i + 1]],
                (0, 255, 0), 3)
        if i == 3:
            break
        cv.line(result_img_with_contours, sorted_points[l1_direction[i]], sorted_points[l1_direction[i + 1]],
                (0, 255, 0), 3)
        cv.line(result_img_with_contours, sorted_points[l3_direction[i]], sorted_points[l3_direction[i + 1]],
                (0, 255, 0), 3)

def save_photo(path, image):
    cv.imwrite(path, image)