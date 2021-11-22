from typing import Dict, List, Tuple, Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from utils import movie_div_predicate, movie_span_predicate, poster_list_predicate, get_num_of_pages, rating_to_number
from constants import LETTERBOXD_URL


def get_film_website_information_from_user(username: str, page_number: int) -> BeautifulSoup:
    with requests.Session() as s:
        index_page = s.get(f"https://letterboxd.com/{username}/films/page/{page_number}")
        return BeautifulSoup(index_page.text, 'html.parser')


def get_movie_list_element(soup: BeautifulSoup) -> Tag:
    matched_elements = soup.find_all(poster_list_predicate)
    if len(matched_elements) != 1:
        raise ValueError("Multiple HTML elements with matching predicate for movie list.")
    return matched_elements[0]


def get_movie_divs_from_ul(movie_ul: Tag) -> List[Tag]:
    return movie_ul.find_all(movie_div_predicate)


def get_movie_spans_from_ul(movie_ul: Tag) -> List[Tag]:
    return [p.find("span") for p in movie_ul.find_all("p")]


def get_movie_url_from_div(movie_div: Tag) -> str:
    end_of_url = movie_div.get("data-film-slug", "")
    if not end_of_url:
        raise ValueError("Movie does not have data-film-slug")
    return LETTERBOXD_URL + end_of_url


def get_movie_rating_from_span(span: Tag) -> Optional[float]:
    return rating_to_number(span.text) if span else None


def get_movie_to_rating_map(movie_tags: List[Tuple[Tag, Tag]]) -> Dict[str, Optional[float]]:
    output = {}
    for div, span in movie_tags:
        url = get_movie_url_from_div(div)
        rating = get_movie_rating_from_span(span)
        output[url] = rating
    return output


def get_movie_elements_from_page(username: str, page_number: int) -> List[Tuple[Tag, Tag]]:
    soup = get_film_website_information_from_user(username, page_number)
    movie_ul = get_movie_list_element(soup)
    divs = get_movie_divs_from_ul(movie_ul)
    spans = get_movie_spans_from_ul(movie_ul)
    return list(zip(divs, spans))


def get_movie_divs(username: str) -> List[Tuple[Tag, Tag]]:
    output = []
    num_pages = get_num_of_pages(username)
    for page_num in range(1, num_pages+1):
        output += get_movie_elements_from_page(username, page_num)
    return output


def run(username: str):
    movie_divs = get_movie_divs(username)
    ratings = get_movie_to_rating_map(movie_divs)
    return ratings

