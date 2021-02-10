import requests
from bs4 import BeautifulSoup
import itertools

def get_archive_links(archive_url):
    r = requests.get(archive_url)
    soup = BeautifulSoup(r.content, 'lxml')
    links = [item.a['href']
             for item in soup.find_all(class_='archive-list-item')]
    return links

def get_mp3_links(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    links = [a['href']
             for a in soup.find(id='beta-inner').find_all('a')
             if a['href'].endswith('mp3')]
    return links

def download_link(url):
    name = url.split('/')[-1]
    print("Downloading: " + name)
    r = requests.get(url, stream=True)
    with open(name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                f.write(chunk)

def download_mp3_links(url):
    for link in get_mp3_links(url):
        download_link(link)

def get_entry(element):
    header = element.find(class_='entry-header').a.get_text()
    description = element.find(class_='entry-body').p.get_text()
    return (header, description)

def get_entries(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    entries = [get_entry(entry)
               for entry in soup.find_all(class_='entry-inner')]
    return entries

def format_entries(entries):
    paragraphs = (x + '\n' + y for (x, y) in entries)
    return '\n\n'.join(paragraphs)

def write_entries(entries, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(format_entries(entries))

if __name__ == '__main__':
    archive_url = "https://www.revolutionspodcast.com/archives.html"
    archive_links = get_archive_links(archive_url)
    entries = reversed([entry
                        for link in archive_links
                        for entry in get_entries(link)])
    write_entries(entries, 'test.txt')