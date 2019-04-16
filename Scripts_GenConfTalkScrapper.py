# AUTHOR: Brooke Baker
# ASSIGNMENT: Final Project
# OVERVIEW: This script scrapes the www.lds.org website for the general conference talks given by the current prophet and apostles

### IMPORT STATEMENTS ###
import requests
from bs4 import BeautifulSoup as bs
import urllib.parse

### FUNCTIONS ###
# function to create url for speaker
def speaker_url(speaker):
    url = 'https://www.lds.org/general-conference/speakers?speaker=' + speaker + '&lang=eng&encoded=true'
    return url

# function to handle General Conference talks by speaker
def get_talks(url, speaker):
    # get html code and parse to BeautifulSoup object
    webpage = requests.get(url)
    soup = bs(webpage.text, 'html.parser')

    # some of the more senior apostles have two pages of talks.. determine if this apostle does and make sure to get talks for both pages
    multiple_pages = soup.find(class_='pages-nav')

    if multiple_pages != None:
        # get talks for first page
        talk_links = store_talk_links(soup)

        # modify url to account for second page, request page and create soup object
        second_page = url + '&page=2'
        webpage = requests.get(second_page)
        soup = bs(webpage.text, 'html.parser')
        
        # add second page of talk links to talk_links
        talk_links += store_talk_links(soup)
    else:
        # get talks for first (and only) page
        talk_links = store_talk_links(soup)

    # call function that will store talk text in individual txt files
    store_talk_text(talk_links, speaker)

# function to store talk links
def store_talk_links(soup):

    # talk links are all located in the <div class="section-wrapper">, get that object
    section_wrapper = soup.find(class_='section-wrapper')

    # get talk links from section_wrapper object
    talk_links_object = section_wrapper.find_all('a')
    talk_links = []
    for link in talk_links_object:
        try:
            talk_links.append(link.get('href'))
        except:
            print('problem with URL; moving on to next one')
    
    # keep only unique links
    talk_links = set(talk_links)
    talk_links = list(talk_links)

    return talk_links

# function to store talk text
def store_talk_text(links, speaker):
    counter = 1
    speaker_parts = speaker.split('-')
    full_name = " ".join(speaker_parts)
    last_name = speaker_parts[len(speaker_parts) - 1]
    print('Writing General Conference talk files for ' + full_name + '...')
    
    for link in links:
        # open webpage
        webpage = requests.get('https://www.lds.org' + link)
        soup = bs(webpage.text, 'html.parser')

        # store talk title and article content
        try:
            title = soup.find(class_='title')
            title = title.get_text()
        except:
            title = 'Title Not Listed.'

        article_content = soup.find(class_='body-block')
        paragraphs = article_content.find_all('p')

        # store talk to txt file
        with open('C:/Users/Brooke/Documents/My Documents/BYU/Winter 2019/LING 360/Final Project/General Conference/' + last_name + "_" + str(counter) + '.txt', 'w', encoding='utf-8') as fout:
            
            # write link and talk title to file
            fout.write('https://www.lds.org' + link + '\n')
            fout.write(title + '.\n\n')
            
            # write paragraphs to file
            for i in paragraphs:
                fout.write(i.get_text() + '\n')
        
        counter += 1

### FUNCTION CALLS ###
# Russell M. Nelson
speaker = "Russell-M.-Nelson"
get_talks(speaker_url(speaker), speaker)

# Dallin H. Oaks
speaker = "Dallin-H.-Oaks"
get_talks(speaker_url(speaker), speaker)

# Henry B. Eyring
speaker = "Henry-B.-Eyring"
get_talks(speaker_url(speaker), speaker)

# M. Russell Ballard
speaker = "M.-Russell-Ballard"
get_talks(speaker_url(speaker), speaker)

# Jeffrey R. Holland
speaker = "Jeffrey-R.-Holland"
get_talks(speaker_url(speaker), speaker)

# Dieter F. Uchtdorf
speaker = "Dieter-F.-Uchtdorf"
get_talks(speaker_url(speaker), speaker)

# David A. Bednar
speaker = "David-A.-Bednar"
get_talks(speaker_url(speaker), speaker)

# Quentin L. Cook
speaker = "Quentin-L.-Cook"
get_talks(speaker_url(speaker), speaker)

# D. Todd Christofferson
speaker = "D.-Todd-Christofferson"
get_talks(speaker_url(speaker), speaker)

# Neil L. Andersen
speaker = "Neil-L.-Andersen"
get_talks(speaker_url(speaker), speaker)

# Ronald A. Rasband
speaker = "Ronald-A.-Rasband"
get_talks(speaker_url(speaker), speaker)

# Gary E. Stevenson
speaker = "Gary-E.-Stevenson"
get_talks(speaker_url(speaker), speaker)

# Dale G. Renlund
speaker = "Dale-G.-Renlund"
get_talks(speaker_url(speaker), speaker)

# Gerrit W. Gong
speaker = "Gerrit-W.-Gong"
get_talks(speaker_url(speaker), speaker)

# Ulisses Soares
speaker = "Ulisses-Soares"
get_talks(speaker_url(speaker), speaker)