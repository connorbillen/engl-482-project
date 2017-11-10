#!/usr/bin/python3

import string
import urllib.request
from bs4 import BeautifulSoup
import os

# clean the string read from the english transcript (NOT IPA, English words)
# on the webpage
def clean_string(s):
    # replaces non-breaking spaces with spaces and collapses all whitespace runs
    return " ".join(str(s).replace("\u00A0", " ").split())

# gets a urllib(2) file handle to a remote file
def get_net_file_handle(fileurl):
    try:
        webfile = urllib.request.urlopen(fileurl)
    except URLError as e:
        raise e

    req_code = webfile.getcode()
    if req_code < 200 or req_code >= 300:
        raise IOError("HTTP error {0} connecting to {1}".format(req_code, fileurl))

    return webfile

# reads a remote file and returns the contents
def get_net_file_contents(fileurl):
    with get_net_file_handle(fileurl) as net_file_handle:
        content = net_file_handle.read()
    return content

# basically wget: fetch data from fileurl over http and dump it in a
# file named localpath
def save_net_file(fileurl, localpath):
    with get_net_file_handle(fileurl) as net_file_handle:
        with open(localpath, "wb") as target_file:
            # bytes is a "bytes object"
            byte = net_file_handle.read(1)
            while byte != b"":
                target_file.write(byte)
                byte = net_file_handle.read(1)

def overwrite_text(text, localpath):
    with open(localpath, "w") as target_file:
        target_file.write(text)

def extract_extension(fname):
    return ""

# for right now, just scrapes the given speaker_id page for the
# urls and english text and prints them
def fetch_accent_archive(speaker_id, target_directory):
    target_directory += "/"
    os.makedirs(target_directory, exist_ok=True)
    page_url = "http://accent.gmu.edu/browse_language.php?function=detail&speakerid={0}".format(speaker_id)

    # get the html
    html_content = get_net_file_contents(page_url)

    # build a document tree
    soup = BeautifulSoup(html_content, "html.parser")
    # div#translation>audio#player>source[src]
    audio_url = soup.find("div", id="translation").find("audio", id="player").find("source")["src"]
    # div#transcript.img[src]
    image_url = soup.find("div", id="transcript").find("img")["src"]
    # div#translation>p.transtext
    speech_text = clean_string(soup.find("div", id="translation").find("p", class_="transtext").string)

    html_content = None
    overwrite_text(speech_text, target_directory + "english.txt")
    speech_text = None
    save_net_file(audio_url, target_directory + "audio.mp3")
    save_net_file(image_url, target_directory + "ipa.gif")

if __name__ == "__main__":
    archive_id_list = [86]
    for archive_id in archive_id_list:
        try:
            print("Fetching data for archive entry ({0})...".format(archive_id), end="", flush=True)
            fetch_accent_archive(archive_id, "test-data/{0}".format(archive_id))
            print("done.")
        except Exception as e:
            print(" Error fetching data for subject id {0}: {1}".format(86, e))
