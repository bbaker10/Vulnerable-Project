# AUTHOR: Brooke Baker
# ASSIGNMENT: Final Project
# OVERVIEW: This script scrapes the https://www.schneier.com/cgi-bin/mt/mt-search.cgi?search=vulnerabilities website for articles discussing various vulnerabilities

### IMPORT STATEMENTS ###
import requests
from bs4 import BeautifulSoup as bs
import urllib.parse

### FUNCTIONS ###
# function to scrape security links for vulnerability articles
def get_articles(url):
    links = []
    for i in range(1, 33):
        # set url page number
        if i <= 10:
            url = url[:-1] + str(i)
        else:
            url = url[:-2] + str(i)

        # get html code and parse to BeautifulSoup object
        webpage = requests.get(url)
        soup = bs(webpage.text, 'html.parser')

        # get page links
        links += get_article_links(soup)

    # call function to store article text
    store_article_text(links)

# function to store page links
def get_article_links(soup):
    # article links are all located in h3 tags with entry class (entry class is unique identifier on page), get those objects
    article_titles = soup.find(class_='entry')
    article_links_a_tags = article_titles.find_all('a')
    article_links = []
    for link in article_links_a_tags:
        try:
            article_links.append(link.get('href'))
        except:
            print('problem with link; moving on to next one')
    
    # keep only unique links
    article_links = set(article_links)
    article_links = list(article_links)

    return article_links

# function to store article text
def store_article_text(links):
    counter = 1

    for link in links:
        print('Writing Security Article file #' + str(counter) + '...')
        # open webpage
        webpage = requests.get(link)
        soup = bs(webpage.text, 'html.parser')

        # store article title and content
        try:
            title = soup.find(class_='entry')
            title = title.get_text()
        except:
            title = 'Title Not Listed.'

        # get article content
        article_content = soup.find(class_='article')

        # remove unneeded footer items that are wrapped in p tags
        try:
            footer_items = article_content.find(class_='entry-tags')
            footer_items.decompose()
            footer_items = article_content.find(class_='posted')
            footer_items.decompose()
        except:
            print('no footer_items to remove')

        # store all article p tags
        paragraphs = article_content.find_all('p')

        # store article to txt file
        with open('C:/Users/Brooke/Documents/My Documents/BYU/Winter 2019/LING 360/Final Project/Security/Security_' + str(counter) + '.txt', 'w', encoding='utf-8') as fout:

            # write link and article title to file
            fout.write(link + '\n')
            fout.write(title + '.\n\n')

            # write paragraphs to file
            for i in paragraphs:
                fout.write(i.get_text() + '\n')

        counter += 1


### FUNCTION CALLS ###
get_articles('https://www.schneier.com/cgi-bin/mt/mt-search.cgi?search=vulnerabilities&__mode=tag&IncludeBlogs=2&blog_id=2&limit=10&page=1')
