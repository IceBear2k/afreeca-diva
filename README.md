# afreeca-diva

A simple Python script compiling a list of mp4 files for direct downloading of all recent broadcasts by The디바 (The DiVa) at http://afreeca.com/vol33lov on 아프리카TV (afreeca TV)

If you don't know what this is about: http://edition.cnn.com/2014/01/29/world/asia/korea-eating-room/

In theory this works with any channel on afreeca TV, it simply needs changing of the URLs in the script.

## Usage:

* ./diva.py will compile a list of direct links to mp4 files
* wget -c -i download.list
* ???
* PROFIT!

## Some quirks and ToDo:

* afreeca's content server IP is currently hardcoded. They probably have more content servers available which could be added.
* Videos are cut into 1h pieces, automatic mp4 merging could be added.
* URL as parameter as to make it more general for afreeca TV and less The DiVa specific.
