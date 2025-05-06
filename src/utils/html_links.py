import requests
from bs4 import BeautifulSoup

def extract_urls_from_html(page_url):
    try:
        response = requests.get(page_url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            # HTML内のすべてのアンカータグからURLを抽出
            return [a['href'] for a in soup.find_all('a', href=True)]
        else:
            print(f"Failed to fetch page: {page_url} (Status code: {response.status_code})")
            return []
    except requests.RequestException as e:
        print(f"Error fetching page: {page_url} ({e})")
        return []
