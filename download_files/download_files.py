#-------------------------------------------------------------------------------
# Name:        download_files
# Purpose: This script autmatically connects to an Toshiba AirFlash webserver
# and downloads all files available on the selected directory
# The computer must be already connected to AirFlash Wi-Fi network before
# running the script
#
# Author:      Alex Porto
#
# Created:     20/04/2019
# Copyright:   (c) aporto 2019
# Licence:     GPL 3.0
#-------------------------------------------------------------------------------

import os
import urllib2
import time
import datetime

#-------------------------------------------------------------------------------
# Configure the script here:
DOWNLOAD_PATH = '/DCIM/100__TSB'
IP_ADDRESS = '192.168.0.1'
UPDATE_TIME_SECONDS = 10 # Wait this amount of time between each check
# End of script configuration
#-------------------------------------------------------------------------------

def download_file(filename):
    print "\tDownloading", filename, "  0%",
    url = 'http://%s/%s/%s' % (IP_ADDRESS, DOWNLOAD_PATH, filename)
    urlconn = urllib2.urlopen(url)
    total_size = int(urlconn.info().getheader('Content-Length').strip())
    bytes_so_far = 0
    downloaded_data = ''

    while 1:
        chunk = urlconn.read(8192)
        bytes_so_far += len(chunk)
        if not chunk:
            break
        print "\b\b\b\b\b% 3d%%" % (bytes_so_far * 100 / total_size),

        downloaded_data += chunk

    path = os.path.dirname(__file__)
    picture_path = os.path.join(path, 'downloaded_files')
    try:
        os.mkdir(picture_path)
    except:
        pass

    with open (os.path.join(picture_path, filename), 'wb') as f:
        f.write(downloaded_data)
    print "Done"

def update():
    path = os.path.dirname(__file__)
    downloaded_list_file = os.path.join(path, 'downloaded.lst')

    if os.path.isfile(downloaded_list_file):
        with open(downloaded_list_file) as f:
            downloaded_list = f.readlines()
            downloaded_list = [_.strip() for _ in downloaded_list if _.strip() != '']
    else:
        downloaded_list = []

    ctime = datetime.datetime.now().strftime('%H:%M:%S')
    print '%s: Checking files in SD card via Wi-Fi...' % (ctime),
    url = 'http://%s/%s' % (IP_ADDRESS, DOWNLOAD_PATH)
    url = 'http://%s/command.cgi?op=100&DIR=%s' % (IP_ADDRESS, DOWNLOAD_PATH)

    urlconn = urllib2.urlopen(url)
    downloaded_html = urlconn.read()
    downloaded_html = downloaded_html.split('\n')
    new_file = False
    count = 0
    for line in downloaded_html:
        #if '"fname":"' in line:
            line = line.split(',')
            if len(line) < 2:
                continue
            filename = line[1]
            #filename = line[line.index('"fname":"')+9:]
            #filename = filename[:filename.index('"')]
            if not filename in downloaded_list:
                if new_file == False:
                    print ''
                new_file = True
                download_file(filename)
                downloaded_list.append(filename)
                with open(downloaded_list_file, 'w') as f:
                    for filename in downloaded_list:
                        f.write(filename + '\n')

    if new_file:
        print 'Done'
    else:
        print "No new files to download!"


def main():
    print ""
    print "=========================================================================="
    print "Make sure this computer is connected to AirFlash Wi-Fi network!"
    print "=========================================================================="
    print ""
    print "Delete the file downloaded.lst if you want to re-download these files"
    print ""
    print "--------------------------------------------------------------------------"

    while True:
        update()
        time.sleep(UPDATE_TIME_SECONDS)

if __name__ == '__main__':
    main()
