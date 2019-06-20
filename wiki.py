import time
import urllib

from bs4 import BeautifulSoup
import requests


start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"


def find_first_link(url):
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, "html.parser")
    
    # This div contains the article's body
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    # stores the first link found in the article, if the article contains no 
    # links this value will remain None
    article_link = None

    # Find all the direct children of content_div that are paragraphs
    for element in content_div.find_all("p", recursive=False):
        # Find the first anchor tag that's a direct child of a paragraph.
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break

    if not article_link:
        return

    # Build a full url from the relative article_link url
    first_link = urllib.parse.urljoin(
        'https://en.wikipedia.org/', article_link)

    return first_link


def continue_crawl(search_history, target_url, max_steps=50):
    if search_history[-1] == target_url:
        print("https://en.wikipedia.org/wiki/Philosophy")
        print("We've found the target article!")
        return False
    elif len(search_history) > max_steps:
        print("it exceeds 50 result. Abort!")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("We have seen this before. Abort!")
        return False
    else:
        return True


article_chain = [start_url]

while continue_crawl(article_chain, target_url):
    print(article_chain[-1])

    first_link = find_first_link(article_chain[-1])
    if not first_link:
        print("no links in this link")
        break

    article_chain.append(first_link)

    time.sleep(2)  # Slow things down so as to not hammer Wikipedia's servers