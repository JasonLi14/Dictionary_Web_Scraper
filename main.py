# main.py
"""
Title: Main Web Scraper
Author: Jason
Date Created: 2023-10-11
"""
# This program gets dictionary data on the internet and converts to a csv.
# Libraries
from urllib.request import urlopen

url = "http://olympus.realpython.org/profiles/aphrodite"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
title_index = html.find("<title>")
start_index = title_index + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]
print(title)


# Data structures
class Word:
    def __init__(self, name):
        self.name = name
    definitions = []


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

# Run
if __name__ == "__main__":
    pass
