import requests
import sys
import re
from typing import Optional

from bs4 import BeautifulSoup as bs

START_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
ANIMALS_ALPHABETICAL = {}
STOP_LETTER = 'A' if len(sys.argv) == 1 else sys.argv[1].upper()


def get_page_content(url: str) -> bytes:
    """
    Идем по URL, забираем контент
    :param url: URL страницы
    :return: Контент страницы в bytes
    """
    try:
        r = requests.get(url)
        content = r.content
        return content
    except requests.RequestException as e:
        err = f'Возникла ошибка при запросе к URL {url}, \n {e}'
        print(err, file=sys.stderr)


def get_next_url(content: bytes) -> Optional[str]:
    """
    Получаем ссылку на следующую страницу из контента
    :param content: Контент страницы
    :return: URL в str, если ссылки нет - вернет None
    """
    soup = bs(content, 'html.parser')
    tag_a = soup.find('a', string="Следующая страница")
    relative_url = tag_a['href']
    next_url = f'https://ru.wikipedia.org{relative_url}'
    return next_url


def parse_page_content(content: bytes):
    """
    Генератор, возвращающий названия животных из контента
    1) Ищем div с class "mw-category"
    2) Берем все li из тега и проходимся по их содержимому, добавляя в словарь
    :param content: Контент страницы
    :return: Название животного в str
    """
    soup = bs(content, 'html.parser')
    container = soup.find(class_='mw-category')
    all_li = container.find_all(name="li")
    for li in all_li:
        yield li.string


def allocate_animal(animal: str, stop_letter: str = "A", allocate_to: dict = ANIMALS_ALPHABETICAL):
    """
    Кладет в название животного в словарь. Индекс будет взят из первой буквы названия животного
    :param animal: Название животного
    :param stop_letter: Если увидим животное на эту букву, помещать в словарь не будем.
    :param allocate_to: Словарь, в который будем складывать животных. Индекс - первая буква в названии животного
    :return: Первая буква из названия
    """
    animal = animal.lstrip()
    first_letter = animal[0].upper()
    if first_letter != stop_letter:  # не включаем stop_letter в наш индекс
        try:
            allocate_to[first_letter].append(animal)
        except KeyError:
            allocate_to[first_letter] = [animal]
    return first_letter


if __name__ == '__main__':
    url = START_URL
    first_letter = ""
    stop_letter = STOP_LETTER
    while first_letter != stop_letter:
        cont = get_page_content(url)
        url = get_next_url(cont)
        for name in parse_page_content(cont):
            first_letter = allocate_animal(name, stop_letter=stop_letter)
            if first_letter == stop_letter:
                break
        print(f'Parsing url= {url}')

    for index, value in ANIMALS_ALPHABETICAL.items():
        if re.match(r'[А-Я]', index):  # hotfix пиявки 'Helobdella nununununojensis'
            print(index, len(value))
