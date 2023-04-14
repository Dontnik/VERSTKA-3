import requests
import os
import urllib
from bs4 import BeautifulSoup


class ErrRedirection(Exception):
    pass
def check_for_redirect(response):
    if response.history:
        raise ErrRedirection("Redirection")


def parse_book_page(page_content):
    soup = BeautifulSoup(page_content, 'lxml')
    author_and_name = soup.find('h1').text
    book_name, author = author_and_name.split('::')
    return author, book_name


def download_book(book_id, file_path):
    payload = {"id": book_id}
    url = f"https://tululu.org/txt.php"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response)
    with open(file_path, 'wb') as file:
        file.write(response.content)


def make_path(filename):
    folder = 'books'
    file_path = os.path.join(folder, filename)
    return file_path


if __name__ == '__main__':
    os.makedirs('books', exist_ok=True)
    for book_id in range(1, 11):
        try:
            url = f'https://tululu.org/b{book_id}/'
            response = requests.get(url)
            response.raise_for_status()
            print(response.history)
            check_for_redirect(response)
            page_content = response.text
            soup = BeautifulSoup(page_content, 'lxml')
            print(urllib.parse.urljoin('https://tululu.org/', soup.find('img')))
            author, book_name = parse_book_page(page_content)
            filename = f'{book_name}.txt'
            file_path = make_path(filename)
            download_book(book_id, file_path)
        except ErrRedirection:
            print('Перенаправление')
