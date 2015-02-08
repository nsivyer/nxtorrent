nxtorrent
=========

Nathans eXecutable Torrent Client

# Background 

For the life of me, I could not find a torrent client which could watch a folder for torrents and execute them once finished. 

This application is currently in use to cluster deliver 4GB executable payloads to 30+ machines, saving bandwidth and time.

# Install

Its advised that you use a private tracker such as opentracker https://erdgeist.org/arts/software/opentracker/


## OSX

    http://www.rasterbar.com/products/libtorrent/python_binding.html

## Debian/Ubuntu

    apt-get install python-libtorrent


#Usage

    ntorrent.py -d <directory> -p <port> [-u <upload limit>] [-r <download limit>] [-x]

x - execute torrent payload once complete.

## Self Extracting Payloads

An example payload:

    #!/bin/bash
    set -ex
    sed -e '1,/^#EOF#$/d' "$0" | tar zx
    exit 0
    #EOF#

Put this into a file called payload_extraction.sh. You can create your self extracting file as follows:

    cat payload_extraction.sh data.tar.gz > data.tar.gz.sh

Then, executing your payload file will extract data.tar.gz: 

    sh data.tar.gz.sh



