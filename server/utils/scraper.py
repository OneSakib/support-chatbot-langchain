import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def scrape_website(base_url, max_pages=30):
    visited = set()
    to_visit = [base_url]
    texts = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            visited.add(url)

            page_text = soup.get_text(separator=' ', strip=True)
            texts.append({"url": url, "content": page_text})

            for link_tag in soup.find_all('a', href=True):
                link = urljoin(url, link_tag['href'])
                if urlparse(link).netloc == urlparse(base_url).netloc:
                    to_visit.append(link)

        except Exception as e:
            print(f"Error visiting {url}: {e}")

    return texts
