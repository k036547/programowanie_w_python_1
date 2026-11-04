import requests

def download_file(url: str, filename: str="latest.txt"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        with open(file=filename, mode="wt", encoding="utf-8", newline="") as f:
            f.write(response.text)
    except requests.exceptions.HTTPError as http_error:
        print(f"Query failed with error: {http_error}")

if __name__ == "__main__":
    download_file(url="https://oleksandr-fedoruk.com/sggw/podyplomowe/file")