def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup.get_text(strip=True)
        else:
            print(f"Failed to fetch URL: {url} (Status code: {response.status_code})")
            return ""
    except requests.RequestException as e:
        print(f"Error fetching URL: {url} ({e})")
        return ""