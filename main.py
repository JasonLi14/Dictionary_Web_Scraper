# main.py
"""
Title: Main Web Scraper
Author: Jason
Date Created: 2023-10-11
"""
import csv
# This program gets dictionary data on the internet and converts to a csv.
# Libraries
from bs4 import BeautifulSoup as bS
import re
from requests import get

regex = r'[^\x00-\x7F]+'
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}



def remove_non_ascii(text):
    return re.sub(regex, '', text)


class Word:
    def __init__(self, name):
        self.name = name
        self.link = f"https://www.merriam-webster.com/dictionary/{name}"
        self.letters_amount = len(name)
    definitions = []
    etymology = ""
    pronunciation = ""
    part_of_speech = []
    sentence = ""


class Dictionary:

    def get_soup(self, url, word):
        raw = get(url=url, headers=headers)
        response = raw.text

        soup = bS(response, "html.parser").select(".main-container")[0]
        if len(soup.select('.play-pron-v2')) > 0:
            pronunciation = soup.select('.play-pron-v2')[0].text.strip()
        else:
            return None

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
        for j in range(len(soup.select('.parts-of-speech'))):  # add the definitions
            part_of_speech = soup.select('.parts-of-speech')[j].text.strip()
            part_of_speech_list.append(part_of_speech)

        # other
        etymology = "Not available."
        if len(soup.select('.et')) > 0:
            etymology = soup.select('.et')[0].text.strip()

        # Sentence
        sentence = soup.select('.d-block')[0].text.strip()

        # Create word object
        word_object = Word(word)
        word_object.definitions = definitions
        word_object.etymology = etymology
        word_object.sentence = sentence
        word_object.part_of_speech = part_of_speech_list
        word_object.pronunciation = pronunciation
        return word_object

    def lookup(self, word):
        base_url = "https://www.merriam-webster.com/dictionary/"
        query_url = base_url + word
        return self.get_soup(query_url, word)


# Insert into csv file
def format_word(word_object):
    """
    Inserts word into csv file.
    :param word_object: word class
    :return:
    """
    # Format it
    # Create a possible parts of speech list
    parts_of_speech = ""
    for i in range(len(word_object.part_of_speech)):
        if i != 0:
            parts_of_speech += ", "
        parts_of_speech += word_object.part_of_speech[i]

    row = [word_object.name, word_object.letters_amount, word_object.pronunciation, word_object.etymology, parts_of_speech,
           word_object.sentence] + word_object.definitions
    return row


# Run
if __name__ == "__main__":
    the_dict = Dictionary()

    # get all the words
    words_to_insert = []
    inserted_words = {}
    with open("generatedWords.txt", "r", encoding="UTF8") as words_list:
        for i in words_list:
            words_to_insert.append(i.rstrip())
            inserted_words[i.rstrip()] = False

    # get the definitions
    words_data = []
    index = 1
    for the_word in words_to_insert:
        # if word is already inserted, i.e. no repeats
        if inserted_words[the_word]:
            continue
        else:
            inserted_words[the_word] = True
        print(index, the_word)
        index += 1
        word_info = the_dict.lookup(the_word)
        if word_info is not None:
            words_data.append(format_word(word_info))
        if index == 10:
            break

    # For csv file
    with open('words.csv', 'w', encoding="UTF8") as words_base:
        words_writer = csv.writer(words_base)
        words_writer.writerow(
            ["Word", "Number of Letters", "Pronunciation", "Etymology",
             "Possible Parts of Speech", "Sentence", "Definitions"])
        words_writer.writerows(words_data)
