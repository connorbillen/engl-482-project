#!/usr/bin/python3

import string
import urllib.request
from bs4 import BeautifulSoup

def clean_string(s):
    # replaces non-breaking spaces with spaces and collapses all whitespace runs
    return " ".join(str(s).replace("\u00A0", " ").split())

# for right now, just scrapes the given speaker_id page for the
# urls and english text and prints them
def fetch_accent_archive(speaker_id, target_directory):
    page_url = "http://accent.gmu.edu/browse_language.php?function=detail&speakerid={0}".format(speaker_id)
    try:
        resp_webpage = urllib.request.urlopen(page_url)
    except URLError as e:
        raise e

    # http response code
    req_code = resp_webpage.getcode()
    # if the code isn't some "OK" variant
    if req_code < 200 or req_code >= 300:
        raise Exception("Unable to get accent archive page: HTTP code {0}".format(req_code))

    # get the html
    html_content = resp_webpage.read()
    resp_webpage.close()

    # build a document tree
    soup = BeautifulSoup(html_content, "html.parser")
    # div#translation>audio#player>source[src]
    audio_url = soup.find("div", id="translation").find("audio", id="player").find("source")["src"]
    # div#transcript.img[src]
    image_url = soup.find("div", id="transcript").find("img")["src"]
    # div#translation>p.transtext
    speech_text = clean_string(soup.find("div", id="translation").find("p", class_="transtext").string)

    print("Audio: ", audio_url)
    print("Image: ", image_url)
    print("Speech text: ", speech_text)

    return

if __name__ == "__main__":
    fetch_accent_archive(86, "data")
