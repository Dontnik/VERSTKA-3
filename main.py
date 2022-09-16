import requests

for id in range(1, 11):

    payload = {"id": id }
    filename = f'book_{id}.txt'
    url = f"https://tululu.org/txt.php"
    response = requests.get(url, params = payload)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
    class ErrRedirection(Exception):
    pass
def check_for_redirect(response):
    if response.history:
        raise ErrRedirection("Redirection"))