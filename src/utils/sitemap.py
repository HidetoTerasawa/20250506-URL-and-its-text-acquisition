import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

def extract_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        print(f"Failed to fetch sitemap: {response.status_code}")
        return []

    try:
        root = ET.fromstring(response.content)
        urls = [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        return urls
    except ET.ParseError:
        print("Failed to parse sitemap XML")
        return []

def extract_recent_urls(sitemap_url, days=30):
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        print(f"Failed to fetch sitemap: {response.status_code}")
        return []

    try:
        root = ET.fromstring(response.content)
        recent_urls = []
        cutoff_date = (datetime.now() - timedelta(days=days)).replace(tzinfo=timezone.utc)
        for url_elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
            loc = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
            lastmod_elem = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")
            if lastmod_elem is not None:
                lastmod = datetime.fromisoformat(lastmod_elem.text)
                if lastmod >= cutoff_date:
                    recent_urls.append(loc)
        return recent_urls
    except ET.ParseError:
        print("Failed to parse sitemap XML")
        return []