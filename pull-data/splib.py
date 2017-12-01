#!/usr/bin/python3

import string
import time
import sys
import re
import urllib.request
from geopy import Nominatim
from GMULib import SpeakerGetter
from mutagen.mp3 import MP3
from bs4 import BeautifulSoup
import os

# clean the string read from the english transcript (NOT IPA, English words)
# on the webpage
def clean_string(s):
    # replaces non-breaking spaces with spaces and collapses all whitespace runs
    return " ".join(str(s).replace("\u00A0", " ").split())

# gets a urllib(2) file handle to a remote file
def get_net_file_handle(fileurl):
    webfile = urllib.request.urlopen(fileurl)
    req_code = webfile.getcode()

    if req_code < 200 or req_code >= 300:
        raise IOError("HTTP error {0} connecting to {1}".format(req_code, fileurl))
    else:
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

# overwrite a file's contents with some text
# in the format required for FAVE-align
def overwrite_fave_text(id, length, text, localpath):
    with open(localpath, "w") as target_file:
        target_file.write("{id}\t{name}\t{start}\t{end}\t{text}".format(
                          id=id,
                          name="Speaker " + id,
                          start=0,
                          end=length,
                          text=text))

# extracts age and gender from the bs4 bio <ul> element as a dict
# (note that male is True, female is False)
def extract_bio_data(bio_el):
    location = str(bio_el.find("li")).split("</em>")[1].split("<a")[0].strip()
    age_and_gender_list = str(bio_el.findAll("li")[3]).split("</em> ")[1].split(",")
    age = int(age_and_gender_list[0].strip())
    # maybe startswith('m') would be good enough...
    gender = age_and_gender_list[1].strip().lower().startswith("male")
    return {
        'age' : age,
        'gender' : gender,
        'location' : location
    }

# scrapes the transcription image, speech text, and audio for a speaker and
# stores them in the target directory
def fetch_accent_archive(speaker_id, target_directory):
    gn = Nominatim()
    target_directory += "/"     # fix the directory name so we can append to it
    os.makedirs(target_directory, exist_ok=True)    # create the directory if it does not exist
    page_url = "http://accent.gmu.edu/browse_language.php?function=detail&speakerid={0}".format(speaker_id)

    # get the html
    html_content = get_net_file_contents(page_url)

    # build a document tree
    soup = BeautifulSoup(html_content, "html.parser")
    # div#translation>audio#player>source[src]
    audio_url = soup.find("div", id="translation").find("audio", id="player").find("source")["src"]
    # div#transcript.img[src]
    # don't bother scraping for the image since we aren;t using it with FAVE-align
    #image_url = soup.find("div", id="transcript").find("img")["src"]
    # div#translation>p.transtext
    speech_text = clean_string(soup.find("div", id="translation").find("p", class_="transtext").string)

    bio_element = soup.find('div', id='wrapper').find('div', id='sidebar').find('ul', class_='bio')
    bio_data = extract_bio_data(bio_element)
    print("{}, {}, {}".format(bio_data['location'], bio_data['age'], bio_data['gender']))

    # saves the data to files
    # save the IPA image (not needed for FAVE-align)
    # save_net_file(image_url, target_directory + "ipa.gif")
    save_net_file(audio_url, target_directory + "audio.mp3")
    # command: `mp3info -p "%m:%s\n" filename`
    audio_length = MP3(target_directory + "audio.mp3").info.length
    overwrite_fave_text(speaker_id, audio_length, speech_text, target_directory + "english.txt")

    # write the location
    geo_location = gn.geocode(bio_data['location'])
    location_txt = open(target_directory + 'location.txt', 'w')
    location_txt.write(bio_data['location'] + "\n")
    location_txt.write(str(geo_location.latitude) + ',' + str(geo_location.longitude))
    print(str(geo_location.latitude) + ',' + str(geo_location.longitude))
    location_txt.close()

if __name__ == "__main__":
    if (len(sys.argv) >= 2):
        archive_id_list = sys.argv[1:]
        print("Using provided IDs...")
    else:
        speaker_getter = SpeakerGetter()
        archive_id_list = speaker_getter.acquire_speaker_ids()
        print("Using scraped IDs...")

    filtered_ids = [id for id in archive_id_list if len(id) > 0 and id[0] != "-"]

    do_sleep = False
    for archive_id in filtered_ids:
        try:
            # sleep between requests to avoid getting blocked
            if do_sleep:
                time.sleep(1)
            else:
                do_sleep = True
            print("Fetching data for archive entry ({0})...\n".format(archive_id), end="", flush=True)
            fetch_accent_archive(archive_id, "test-data/{0}".format(archive_id))
            print("done.")
        except Exception as e:
            print("Error fetching data for subject id {0}: {1}".format(archive_id, e))
