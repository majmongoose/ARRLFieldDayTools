# FIELD DAY TOOLS

This repository contains some of my tools used for converting logs for the ARRL Field Day. Specifically these tools work with ADIF files and special files created by [SQUIRL Logger](https://www.qsl.net/kc8opv/squirl-fd/). Since I was unable to locate any tools to do what I needed, I figured I should create and publish these for use.

## adifConverter
ADIF Converter can take command line arguments (input and output file), or it will prompt the user for the file names. It will ask you all of the details for the header, and then truncate it into one big cabrillo file. 

>Known Bug: The software adds some blank qso lines under the header. You can manually delete these or fixed with a PR.

## squirlConverter
Squirl converter is a bit simpler to use. Put all of the exported log TXT files into the same directory as the script, and give it an argument for the name of the output file (it will default to "output.txt"). It will also have you enter the header information, and output another single large cabrillo file.
