import requests
import bs4

def crawl_links(url):
    visited = set()
    frontier = [url]
    while len(frontier) > 0:
        link = frontier.pop()
        if link not in visited:
            visited.add(link)
            r = requests.get(url)
            soup = bs4.BeautifulSoup(r.content, 'html5lib')
