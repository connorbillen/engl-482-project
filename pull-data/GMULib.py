#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup, SoupStrainer

class SpeakerGetter:
    def __init__(self):
        self.speaker_list = []
        self.counter = []
        self.url = "http://accent.gmu.edu/searchsaa.php" 

        self.params = {
            "function": "find",
            "language": "english",
            "submit": "Find",
            "city": "none",
            "state_or_province": "none",
            "country": "usa",
            "age_op": "iseq",
            "age": "",
            "onset_age_op": "iseq",
            "onset_age": "",
            "other_languageid": "none",
            "english_residence": "none",
            "length_of_residence_op": "iseq",
            "length_of_residence": "",
            "vowgen1": "none",
            "vowgen2": "none",
            "vowgen3": "none",
            "consgen1": "none",
            "consgen2": "none",
            "consgen3": "none",
            "syllgen1": "none",
            "syllgen2":	"none",
            "syllgen3":	"none"
        }

    def acquire_speaker_ids(self): 
        response = requests.post(self.url, data=self.params)
        return self.parse_speaker_ids(response.text)
 
    def parse_speaker_ids(self, response):
        links = BeautifulSoup(response, "html.parser", parse_only=SoupStrainer("a"))
        inputs = BeautifulSoup(response, "html.parser", parse_only=SoupStrainer("input"))
        ps = BeautifulSoup(response, "html.parser", parse_only=SoupStrainer("p"))

        for p in ps:
            p = str(p)
            if "english" in p:
                # output speaker id
                print(p.split("speakerid=")[1].split("\"")[0])

                # output speaker info
                print(p.split("</a> ")[1].split("</p>")[0])

        for link in links:
            if link.has_attr("href") and "=" in link["href"]:
                id = link["href"].split("=")[2]
                self.speaker_list.append(id)

        for input in inputs:
            if input.has_attr("value"):
                if "Next" in input["value"]:
                    print("More data available")

        return self.speaker_list


if __name__ == "__main__":
    speaker_getter = SpeakerGetter()
    print(speaker_getter.acquire_speaker_ids())
