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
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}

class Dictionary:
    def remove_non_ascii(self, text):
        return re.sub(regex, '', text)

    def get_soup(self, url):
        response = get(url=url, headers=headers).text
        response = self.remove_non_ascii(response)
        soup = bs(response, "html.parser").select(".main-container")[0]
        print(soup)
        definitions = []
        for i in range(len(soup.select('.dtText'))):  # add the definitions
            # dtText is the class they belong to
            definition = soup.select('.dtText')[i].text.strip()
            # print(definition)
            if len(definition) > 1:  # clean up definition
                if definition[len(definition)-1] == ":":
                    definition = definition[:len(definition)-1]
                if definition[0:2] == ": ":
                    definition = definition[2:]

                definitions.append(definition)

        # get part of speech
        part_of_speech_list = []
        for i in range(len(soup.select('.parts-of-speech'))):  # add the definitions
            part_of_speech = soup.select('.parts-of-speech')[i].text.strip()
            part_of_speech_list.append(part_of_speech)

        # other
        etymology = soup.select('.et')[0].text.strip()
        syllables = soup.select('.word-syllables-entry')[0].text.strip()
        return definitions, part_of_speech_list, etymology


    def lookup(self, word):
        # base_url = "http://www.thefreedictionary.com/"
        base_url = "https://www.merriam-webster.com/dictionary/"
        query_url = base_url + word
        return self.get_soup(query_url)


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
    the_dict = Dictionary()
    definition = the_dict.lookup(word)
    print(definition)


# Run
if __name__ == "__main__":
    web_scrape("beautiful")
