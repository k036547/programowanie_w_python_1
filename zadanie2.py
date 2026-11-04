import requests

class DownloadError(Exception):
    pass

class AccessDeniedError(DownloadError):
    pass

class NotFoundError(DownloadError):
    pass

def download_file(url: str, filename: str="latest.txt"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        with open(file=filename, mode="wt", encoding="utf-8", newline="") as f:
            f.write(response.text)
    except requests.exceptions.HTTPError as err:
        response_code = response.status_code
        match response_code:
            case 403: 
                raise AccessDeniedError(f"Dostęp zabroniony ({response_code}): {url}") from err
            case 404: 
                raise NotFoundError(f"Zasób nie znaleziony ({response_code}): {url}") from err
            case _:
                raise
    else:
        print(f"Zapis do pliku {filename} się powiódł.")
       
if __name__ == "__main__":
    """ Przypadki testowe z maskowaniem tracestacków i bez"""
    try:
        download_file(url="https://oleksandr-fedoruk.com/sggw/podyplomowe/file")
    except DownloadError as err:
        print(f"Błąd: {err}")
    #download_file(url="http://oleksandr-fedoruk.com/sggw/podyplomowe/403")
    #download_file(url="http://oleksandr-fedoruk.com/sggw/podyplomowe/404")