# Автор: Вячеслав Кравченко

def appearance(intervals):
    # созадем структуру интервалов [[timestamp, timestamp], [timestamp, timestamp], ...]
    intervals['pupil'] = make_intervals(intervals['pupil'])
    intervals['tutor'] = make_intervals(intervals['tutor'])

    # подгоняем все интервалы в наборе под рамки урока (урезаем первый и последний таймстамп в интервале)
    intervals['pupil'] = adjust_intervals_to_lesson(intervals['pupil'], intervals['lesson'][0], intervals['lesson'][1])
    intervals['tutor'] = adjust_intervals_to_lesson(intervals['tutor'], intervals['lesson'][0], intervals['lesson'][1])

    # выравниваем timeline
    intervals['pupil'] = fix_timeline(intervals['pupil'])
    intervals['tutor'] = fix_timeline(intervals['tutor'])

    # находим пересечения времени у pupil и tutor
    interceptions = find_interceptions(intervals['pupil'], intervals['tutor'])

    # получаем сумму разниц интервалов
    result = sum(get_interval_delta(interval) for interval in interceptions)

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
    intervals_ = []
    for interval in intervals:
        time = interval[0]
        if time < start:  # проверяем начало интервала ко времени старта урока
            if interval[1] < start:  # проверяем конец этого интервала
                continue  # и сразу идем за следующим, если весь интервал не попадает в урок
            interval[0] = start  # увеличиваем интервал до start
        intervals_.append(interval)
    # Подгонка интервалов к концу занятия
    intervals__ = []
    for interval in intervals_:
        time = interval[1]
        if time > end:  # проверяем конец интервала
            if interval[0] > end:  # проверяем конец этого интервала
                continue  #
            interval[1] = end  # уменьшаем интервал до start
        intervals__.append(interval)
    return intervals__


def find_interceptions(intervals_1: list, intervals_2: list) -> list:
    """
    Находим пересечения двух списков с интервалами, и возвращаем список с пересечениями
    :param intervals_1: Список с интервалами 1
    :param intervals_2: Список с интервалами 2
    :return: Список с интервалами (пересечения)
    """
    interceptions = []
    # проход по всем интервалам в списках интервалов
    for interval_i in intervals_1:
        for interval_j in intervals_2:
            # При пересечении интервалов, выделяем пересечение и добавляем в результат
            if check_interception(interval_i, interval_j):
                interceptions.append(intercept_intervals(interval_i, interval_j))
    return interceptions


def check_interception(interval_1: list, interval_2: list) -> bool:
    """
    Проверяем пересекаются ли два интервала
    :param interval_1: Интервал_№1
    :param interval_2: Интервал_№2
    :return: bool
    """
    value = (
             (interval_2[0] <= interval_1[0] <= interval_2[1]) or
             (interval_2[0] <= interval_1[1] <= interval_2[1]) or
             (interval_1[0] <= interval_2[0] and interval_1[1] >= interval_2[1]) or
             (interval_1[0] >= interval_2[0] and interval_1[1] <= interval_2[1])
             )
    return value


def unite_intervals(interval_1: list, interval_2: list) -> list:
    """
    Конкатенация интервалов. Передавать только пересекающиеся интервалы (!)
    :param interval_1: Интервал 1
    :param interval_2: Интервал 2
    :return: Интервал ("Склееный" интервал)
    """
    return [min([interval_1[0], interval_2[0]]), max([interval_1[1], interval_2[1]])]


def intercept_intervals(interval_1: list, interval_2: list) -> list:
    """
    Выделение пересечения интервалов. Передавать только пересекающиеся интервалы (!)
    :param interval_1: Интервал 1
    :param interval_2: Интервал 2
    :return: Интервал (Пересечение интервалов)
    """
    return [max([interval_1[0], interval_2[0]]), min([interval_1[1], interval_2[1]])]


def get_interval_delta(interval: list) -> int:
    """
    Подсчитываем разницу между концом и началом интервала
    :param interval: Интервал
    :return: Дельта между концом и началом интервала
    """
    return interval[1] - interval[0]


def fix_timeline(intervals: list, index = 0):
    """
    Получаем пересекающийся список интервалов,
    возвращаем непересекающийся таймлайн из всех интервалов
    :param intervals: Список из интервалов
    :param index: Нужно для рекурсии, что бы проверить все элементы из списка.
    :return: Таймлайн (Список интервалов упорядоченный и непересекающийся)
    """

    current_interval = intervals.pop(index)  # Этот интервал будем сверять с остальными
    unites = []  # список объединенных интервалов
    rest = []  # все, что не попало в список unities

    # сравниваем интервалы и наполняем списки unities и rest
    for interval in intervals:
        if check_interception(current_interval, interval):
            unity = unite_intervals(current_interval, interval)
            if unity not in unites:
                unites.append(unity)
        elif interval:
            rest.append(interval)

    timeline = unites + rest
    if unites:  # Если есть объединения, то надо проверить весь список еще раз с тем же элементом.
        timeline = fix_timeline(timeline)
    else:  # Если их нет, то просто склеиваем список обратно
        timeline = [current_interval] + rest

    # Идем в рекурсию со следующим элементом, пока не переберем все.
    index += 1
    if index < len(timeline):
        timeline = fix_timeline(timeline, index)
    return timeline




tests = [
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
