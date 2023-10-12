# main.py
"""
Title: Main Web Scraper
Author: Jason
Date Created: 2023-10-11
"""
# This program gets dictionary data on the internet and converts to a csv.
# Libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import re
from requests import get

regex = r'[^\x00-\x7F]+'

class Dictionary:
    def remove_non_ascii(self, text):
        return re.sub(regex, '', text)

    def get_soup(self, url):
        raw = self.remove_non_ascii(urlopen(url).read().decode('utf-8'))
        soup = bs(raw)
        print(soup.select("#MainTxt")[0].select('.ds-single')[1].text.strip())
        return soup.select("#MainTxt")[0].select('.ds-single')[0].text.strip()

    def lookup(self, word):
        base_url = "http://www.thefreedictionary.com/"
        query_url = base_url + word
        return self.get_soup(query_url)

"""
url = "http://olympus.realpython.org/profiles/aphrodite"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
title_index = html.find("<title>")
start_index = title_index + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]
soup = BeautifulSoup(html, "html.parser")
"""


# Data structures
class Word:
    def __init__(self, name):
        self.name = name
        self.link = f"https://dictionary.cambridge.org/dictionary/english/{name}"
    definitions = []
    etymology = ""


# Create a csv file.


# Insert into csv file
def insert_word(word_object):
    """
    Inserts word into csv file.
    :param word_object: word class
    :return:
    """


# Web scrape.
def web_scrape(word):
    """
    Find info on word and create new word object.
    :param word: string
    :return: wordObject
    """
    """new_word_obj = Word(word)
    print(new_word_obj.link)
    page = urlopen(new_word_obj.link)
    # use the beautiful soup the parse
    html = page.read().decode("utf-8")
    soup = bs(html, "html.parser")
    # print(soup)
    definitions = soup.find_all("beautiful")
    print(definitions)"""
    the_dict = Dictionary()
    definition = the_dict.lookup(word)
    print(definition)


# Run
if __name__ == "__main__":
    web_scrape("beautiful")
