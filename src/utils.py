from typing import List, Iterable, Sequence, Union
import requests

from bs4.element import Tag
from bs4 import BeautifulSoup

from constants import STAR, HALF


def one_of_list_starts_with(loe: List[str], *words: str):
    for item in loe:
        for word in words:
            if item.startswith(word):
                return True
    return False


def page_number_predicate(element: Tag) -> bool:
    return element and element.name == "li" and one_of_list_starts_with(element.get("class", []), "paginate-page")


def get_num_of_pages(soup: Union[BeautifulSoup, str]) -> int:
    if isinstance(soup, str):
        with requests.Session() as s:
            index_page = s.get(f"https://letterboxd.com/{soup}/films/page/1")
            soup = BeautifulSoup(index_page.text, 'html.parser')

    page_numbers_list = soup.find_all(page_number_predicate)
    if not page_numbers_list:
        return 1
    return int(page_numbers_list[-1].text)


def poster_list_predicate(element: Tag) -> bool:
    return element and element.name == "ul" and one_of_list_starts_with(element.get('class', []), "poster-list")


def movie_div_predicate(element: Tag) -> bool:
    return element and element.name == "div"


def movie_span_predicate(element: Tag) -> bool:
    return element and element.name == "span"


def rating_to_number(rating_with_stars: str) -> float:
    score = 0
    if not rating_with_stars:
        return score
    for character in rating_with_stars:
        if character == STAR:
            score += 1
        if character == HALF:
            score += 0.5
    return score
