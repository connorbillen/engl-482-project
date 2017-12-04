# ENGL 482 : Term Project
Analyzing the phonetic differences between common phonemes per region.

FAVE-align: http://fave.ling.upenn.edu/
Source of data: http://accent.gmu.edu/

To collect the data and run FAVE-Align, run:
> collect.sh

Please note: This requires `ffmpeg` and `HTK-3.4` to be installed

To convert the TextGrid files to readable text files:
> analyze.sh

Mapping the data requires the latest version of Basemap for Matplotlib to be installed

Final paper improvements
- Geography density plot (dot stacks)
- Socio vars (gender, age)
- Package dependencies/executable
- Choice of words
- Error rate

Requirements:
    Programs:
        python3
        pip3
        Bash-compatible shell (for .sh scripts)
        ffmpeg
        HTK 3.4
    Python libraries:
        FAVE-align (not a pip package)
        matplotlib
        mpl_toolkits (extension to matplotlib)
        geopy
        bs4 (BeautifulSoup 4)
        mutagen
