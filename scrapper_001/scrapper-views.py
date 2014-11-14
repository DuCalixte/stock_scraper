from bs4 import BeautifulSoup
from urllib2 import urlopen
import lxml

BASE_URL = "http://www.chicagoreader.com"

def get_category_links(section_url):
    html = urlopen(section_url).read()
    soup = BeautifulSoup(html, "lxml")
    # boccat = soup.find("dl", "boccat")
    boccat = soup.find("div", "bestOfItem")
    print 'f'
    category_links = [BASE_URL + dd.a["href"] for dd in boccat.findAll("h4")]
    return category_links

def get_category_winner(category_url):
    html = urlopen(category_url).read()
    soup = BeautifulSoup(html, "lxml")
    category = soup.find("h1", "headline").string
    winner = [h2.string for h2 in soup.findAll("h2", "boc1")]
    runners_up = [h2.string for h2 in soup.findAll("h2", "boc2")]
    return {"category": category,
            "category_url": category_url,
            "winner": winner,
            "runners_up": runners_up}

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

if __name__ == '__main__':
	links = get_category_links('http://www.chicagoreader.com/chicago/BestOf?category=1979894&year=2014')
	# print get_category_links('http://www.chicagoreader.com/chicago/BestOf?category=1979894&year=2014')
	print links
	print links.length
