def appearance(intervals):

    intervals['pupil'] = make_intervals(intervals['pupil'])
    intervals['tutor'] = make_intervals(intervals['tutor'])

    intervals['pupil'] = adjust_intervals_to_lesson(intervals['pupil'], intervals['lesson'][0], intervals['lesson'][1])
    intervals['tutor'] = adjust_intervals_to_lesson(intervals['tutor'], intervals['lesson'][0], intervals['lesson'][1])

    intervals['tutor'] = sorted(intervals['tutor'], key=lambda interval: interval[0])
    intervals['pupil'] = sorted(intervals['pupil'], key=lambda interval: interval[0])

    print("pupil->", intervals['pupil'])
    print("tutor->", intervals['tutor'])
    interceptions = find_interceptions(intervals['pupil'], intervals['tutor'])
    # interceptions = sorted(interceptions, key=lambda interval: interval[0])
    print('sorted interceptions ', interceptions)
    interceptions = fix_interceptions(interceptions)
    print('interceptions ', interceptions)
    result = sum(get_interval_delta(interval) for interval in interceptions)
    print(result)
    return result


def make_intervals(timestamp_list: list) -> list:
    """
    Выделяем интервалы во отдельные массивы
    :param timestamp_list: список с таймстампами
    :return: список с интервалами
    """
    intervals = []
    for i in range(0, len(timestamp_list), 2):
        interval = [timestamp_list[i], timestamp_list[i + 1]]
        intervals.append(interval)
    return intervals


def adjust_intervals_to_lesson(intervals: list, start: int, end: int) -> list:
    """
    Изменяем начальный и конечный timestamp. Подгоняем под start и end.
    :param intervals: Массив интервалов, который следует отредактировать
    :param start: Начало подгонки интервала
    :param end: Конец подгонки интервала
    :return: Отредактированный массив интервалов
    """
    # Подгонка интервалов к началу занятия
    for interval in intervals:
        time = interval[0]
        if time < start:  # проверяем начало интервала
            if interval[1] < start:  # проверяем конец этого интервала
                del interval
                continue  # если оба условия совпали, то удаляем интервал целиком и сразу идем за следующим интервалом
            print(f"увеличиваем {time} до {start}")
            interval[0] = start  # увеличиваем интервал до start

    # Подгонка интервалов к концу занятия
    for interval in intervals:
        time = interval[1]
        if time > end:  # проверяем конец интервала
            if interval[0] > end:  # проверяем конец этого интервала
                print("исключили интервал целиком!!!")
                del interval
                return intervals
            print(f"уменьшаем {time} до {end}")
            interval[1] = end  # уменьшаем интервал до start
    return intervals


def find_interceptions(intervals_1: list, intervals_2: list) -> list:
    interceptions = []
    # проход по всем интервалам в списках интервалов
    for interval_i in intervals_1:
        # interval_i = [intervals_1[i], intervals_1[i + 1]]  # интервал - это начало и конец (нечетный индекс и четный)

        for interval_j in intervals_2:
            # interval_j = [intervals_2[j], intervals_2[j + 1]]
            print("--->", interval_i, interval_j)

            # Условие пересечения интервалов:
            if ((interval_j[0] <= interval_i[0] <= interval_j[1]) or
                    (interval_j[0] <= interval_i[1] <= interval_j[1]) or
                    (interval_i[0] <= interval_j[0] and interval_i[1] >= interval_j[1]) or
                    (interval_i[0] >= interval_j[0] and interval_i[1] <= interval_j[1])):
                interceptions.append([
                    max([interval_i[0], interval_j[0]]), min([interval_i[1], interval_j[1]])
                ])

    return interceptions


def fix_interceptions(intervals: list) -> list:
    """
    Принимаем на вход массив с интервалами, отдаем новый массив, где интервалы не пересекаются между собой
    :param intervals: Массив с интервалами
    :return: Массив с интервалами без пересечений
    """
    new_intervals = []
    another_try = False
    skip = False

    for i in range(len(intervals) - 1):
        if skip:
            skip = False
            continue
        if intervals[i][1] > intervals[i + 1][0]:
            print("SWAPPIN", i)
            new_intervals.append([
                min([intervals[i][0], intervals[i + 1][0]]),
                max([intervals[i][1], intervals[i + 1][1]])
            ])
            another_try = True
            skip = True
        else:
            new_intervals.append(intervals[i])

    print("NEW---->", new_intervals)

    if another_try:
        fix_interceptions(new_intervals)
    else:
        new_intervals.append(intervals[-1])
    return new_intervals


def get_interval_delta(interval: list) -> int:
    delta = interval[1] - interval[0]
    print(delta)
    return delta


tests = [
    # Slava's test data, delete it
    # {'data': {'lesson': [1594668380, 1594668390],
    #           'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
    #           'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
    #  'answer': 3117
    #  },

    {'data': {'lesson': [1594663200, 1594666800],
              'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
              'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150,
                        1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
                        1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                        1594706524, 1594706524, 1594706579, 1594706641],
              'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'data': {'lesson': [1594692000, 1594695600],
              'pupil': [1594692033, 1594696347],
              'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
