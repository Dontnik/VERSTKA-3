import requests
import os
from bs4 import BeautifulSoup


url = 'https://tululu.org/txt.php'
response= requests.get(url)

for id in range(1, 11):

    soup =  BeautifulSoup(response.text, 'lxml')
    payload = {"id": id }
    filename_test = soup.find('h1')
    filename = f'{filename_test}.txt'
    file_path = os.path.join('books', filename)
    url = f"https://tululu.org/txt.php"
    response = requests.get(url, params = payload)
    response.raise_for_status()
    with open(filename, 'wb', file_path) as file:
        file.write(response.content)
def check_for_redirect(response):
    if response.history:
        raise ErrRedirection("Redirection")


if __name__ == "__main__":
    path = os.makedirs('books', exist_ok = True)