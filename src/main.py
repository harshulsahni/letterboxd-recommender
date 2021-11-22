import sys

from src.webscraper import run


if __name__ == '__main__':
    username = sys.argv[1]
    out = run(username)
    print(out)
    # soup = get_film_website_information_from_user("ishaanp")
    # print(find_num_of_pages(soup))
