# ENGL 482 : Term Project
Analyzing the phonetic differences between common phonemes per region.

FAVE-align: http://fave.ling.upenn.edu/

Source of data: http://accent.gmu.edu/

To collect the data and run FAVE-Align, run:
> collect.sh

Please note: This requires `ffmpeg` and `HTK-3.4` to be installed. `ffmpeg` should be available
in any standard Linux package manager. HTK is an open source hidden markov aligner that is available
for download from http://htk.eng.cam.ac.uk/. 

To convert the TextGrid files to readable text files:
> analyze.sh

This runs a simple script that rips out the quantitative information from the Praat TextGrid files and
gives us a text transcription using ARPAbet symbols, as well as a Python Pickle object containing a hierarchy
of information.

Mapping the data requires the latest version of Basemap for Matplotlib to be installed.

Requirements:
Programs:
*   python3
*   pip3
*   Bash-compatible shell (for .sh scripts)
*   ffmpeg
*   HTK 3.4

Python libraries:
*   FAVE-align (not a pip package)
*   matplotlib
*   mpl_toolkits (extension to matplotlib)
*   geopy
*   bs4 (BeautifulSoup 4)
*   mutagen
