"""
Автор: Вячеслав Кравченко
"""


arr = list("111111111111111111111111100000000")


def task(arr=arr):
    """
    Сложность алгоритма O(log n) (бинарный поиск).
    Исходя из условия задачи, я не предусматривал случай, когда в массиве только нули или только единицы.
    :param arr: Массив, в котором сначала идут "1", а потом "0"
    :return: Индекс первого нуля в массиве
    """
    low = 0
    high = len(arr)-1

    while low <= high:
        mid = (low + high) // 2
        guess = (arr[mid], arr[mid+1])
        if guess == ('1', '0'):
            print("I found it!")
            return mid+1
        elif guess == ('1', '1'):
            low = mid
        else:
            high = mid


print(task())
