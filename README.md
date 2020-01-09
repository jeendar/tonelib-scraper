# ToneLib Scraper

**ToneLib Scraper** is a command-line tool for downloading guitar effects pedal patches from ToneLib forums.
It requires Python 3.0+, Selenium, and Geckodriver.
Note that this tool does not download the contents of a torrent file but downloads files with .torrent extension.
You should use a Torrent client to open these files. 

## Usage

Run `pip install selenium` before running the script.
You should also download the latest Geckodriver executable and put it in the same directory with `tonelib_scraper.py`.
Execute the script by running `python3 tonelib_scraper.py -u <yourUsername> -p <yourPassword> -e <yourPedalModel>`.
All of the arguments are required for the script to run.
By default, it will create a new folder in scripts directory and store downloaded files in there.

## Options

| Commands                          | Description                                                                                                                 |
|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
|```-h``` or ```--help```           |Prints help text                                                                                                             |
|```-u``` or ```--username```       |ToneLib login name                                                                                                           |
|```-p``` or ```--password```       |ToneLib login password                                                                                                       |
|```-e``` or ```--effects```        |Effects pedal models. Available options are: "tonelib", "ms50g", "ms60b", "ms70cdr", "g3n", "g1on", "b1on", "b3n", "g1", "b1"|
