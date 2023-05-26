import requests
from tqdm import tqdm
import os
import urllib
import time
import logging
import argparse
from bs4 import BeautifulSoup


class ErrRedirection(Exception):
    pass


def check_for_redirect(response):
    if response.history:
        raise ErrRedirection("Redirection")


def parse_book_page(page_content, book_id):
    soup = BeautifulSoup(page_content, 'lxml')
    author_and_name = soup.find('h1').text
    book_name, author = author_and_name.split('::')

    cover_url = urllib.parse.urljoin(url, soup.find('div', class_='bookimage').find('img')['src'])
    return author, book_name, covers_url


def download_book(book_id, file_path):
    payload = {"id": book_id}
    url = f"https://tululu.org/txt.php"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response)
    with open(file_path, 'wb') as file:
        file.write(response.content)

def cover_download(covers_url, book_id):
    response = requests.get(covers_url)
    response.raise_for_status()
    file_path_cover = f'covers/cover_{book_id}.jpg'
    with open(file_path_cover, 'wb') as file:
        file.write(response.content)

if __name__ == '__main__':
    os.makedirs('books', exist_ok=True)
    os.makedirs('covers', exist_ok=True)
    os.makedirs('comments', exist_ok=True)
    os.makedirs('genres', exist_ok=True)
    parser = argparse.ArgumentParser(
        description='Данная программа скачивает книги'
    )
    start_id = parser.add_argument("start_id", help="first number", type=int)
    end_id = parser.add_argument("end_id", help="second number", type=int)
    args = parser.parse_args()
    for book_id in range(args.start_id, args.end_id):
        while True:
            try:
                url = f'https://tululu.org/b{book_id}/'
                response = requests.get(url)
                response.raise_for_status()
                check_for_redirect(response)
                page_content = response.text
                soup = BeautifulSoup(page_content, 'lxml')
                author, book_name, covers_url = parse_book_page(page_content, book_id)
                comments_file_path = f'comments/comment_{book_id}.txt'
                genres_file_path = f'genres/genre_{book_id}.txt'
                cover_download(covers_url, book_id)
                file_path = f'books/{book_name}.txt'
                genres = soup.find_all('span', class_='d_book')
                genres = [genre.text for genre in genres]
                with open(genres_file_path, 'w', encoding='UTF-8') as file:
                    file.write('\n'.join(genres))
                comments = soup.find_all('span', class_='black')
                comments = [comment.text for comment in comments]
                with open(comments_file_path, 'w', encoding='UTF-8') as file:
                    file.write('\n'.join(comments))
                download_book(book_id, file_path)
                break
            except ErrRedirection:
                logging.warning("Перенаправление")
                break
            except requests.exceptions.ConnectionError:
                logging.warning("Потеряно соединение")
                time.sleep(4)
            except requests.exceptions.HTTPError:
                logging.exception("Ошибка при запросе")
                break