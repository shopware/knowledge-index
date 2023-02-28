from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import List
import requests


def get_links(url: str) -> List[str]:
    doc = requests.get(url)

    if not doc.ok:
        return []

    soup = BeautifulSoup(doc.text, "html.parser")

    root = urlparse(url)
    link_set = set()

    for anchor in soup.find_all("a"):
        link = anchor.get("href")
        if link is None:
            continue

        link = urlparse(link)

        if link.netloc != "":
            continue

        abs_link = root._replace(path=link.path)
        link_set.add(abs_link.geturl())

    return list(link_set)


def get_link_tree(root: str, max_depth=3) -> List[str]:
    seen_links = set()

    stack = [{"url": root, "remaining": max_depth}]

    while len(stack) > 0:
        current = stack.pop()
        url, remaining = current["url"], current["remaining"]
        if remaining == 0 or url in seen_links:
            continue
        print(f"scraping {url}")
        links = get_links(url)
        print("done")

        stack += [{"url": link, "remaining": remaining - 1} for link in links]
        seen_links.add(url)

    return list(seen_links)


def filter_working_urls(urls: List[str]) -> List[str]:
    return [url for url in urls if requests.get(url).ok]
