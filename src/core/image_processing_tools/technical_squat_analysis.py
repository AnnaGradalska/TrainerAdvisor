def analyze_squat_inclination(points):
    max_inclination = 0.17
    back_length = list(map(lambda sublist: sublist[5][1] - sublist[0][1], points))
    print(f"{(max(back_length) - min(back_length)) / max(back_length)} > {max_inclination}")
    if (max(back_length) - min(back_length)) / max(back_length) > max_inclination:
        return "Nadmierne pochylenie tułowia w trakcie przysiadu.\n"
    return "Optymalne utrzymanie tułowia w trakcie przysiadu.\n"


def analyze_knees_position(points):
    max_knee_position_difference = -0.2

    shin_length = points[0][10][1] - points[0][8][1]
    left_knee_position_difference = (points[2][8][0] - points[3][8][0]) / shin_length
    right_knee_position_difference = (points[3][9][0] - points[2][9][0]) / shin_length

    print(f"{left_knee_position_difference} < {max_knee_position_difference}")
    print(f"{right_knee_position_difference} < {max_knee_position_difference}")

    if left_knee_position_difference < max_knee_position_difference or right_knee_position_difference < max_knee_position_difference:
        if left_knee_position_difference < max_knee_position_difference and right_knee_position_difference < max_knee_position_difference:
            return "Zapadanie kolan w trakcie wyjścia z dolnej pozycji.\n"
        elif left_knee_position_difference < max_knee_position_difference:
            return "Zapadanie lewego kolana w trakcie wyjścia z dolnej pozycji.\n"
        elif right_knee_position_difference < max_knee_position_difference:
            return "Zapadanie prawego kolana w trakcie wyjścia z dolnej pozycji.\n"

    return "Prawidłowe prowadzenie kolan w trakcie przysiadu.\n"

def analyze_squat_depth(points):
    min_squat_depth = 0.18
    shin_length = points[0][10][1] - points[0][8][1]
    squat_depth = (points[2][8][1] - points[2][6][1]) / shin_length

    if squat_depth > min_squat_depth:
        return "Zbyt płytki przysiad. Staw biodrowy musi znaleźć się poniżej stawu kolanowego.\n"
    return "Optymalna głębokość przysiadu.\n"
