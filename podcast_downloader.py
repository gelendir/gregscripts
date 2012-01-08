#!/usr/bin/python
"""
Simple Podcast Downloader, by Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes
v0.1.0

During a python workshop at my local linux user group, We made a list of 'small projects' as a source of ideas that could be used to practice programming apps in python. One of the ideas that came up was to do a simple batch podcast downloader from rss feeds. This is my response to who ever came up with the idea (can't remember who it was, might even be me). 

The app parses a rss feed using the universal feedparser library (available at www.feedparser.org). It iterates through each item in the feed, searching each item  for text that looks like a link to a audio file. (a.k.a looks inside each xml tag) It then downloads all the files. 

GOTCHAS:
The app systematically searches all elements because each podcasting feed doesn't place their content/file links at the same place. Because of this, a same link can be found multiple times inside the same item. Fortunately, the app checks if a file with the same name already exists before downloading.
Right now the app will only work if its executed as a script. It might be interesting to create a PodcastDownloader class that encapsualtes the whole process so that it can be used elsewhere

TODO:
- encapsualte the whole downloading process into a class (class PodcastDownloader) so that it can be used as a module
- compile most used regexps (re.compile)
- find out more about how podcasts are embedded in a rss/atom feed so that we don't need to rely on the file extension to download the content. Idea : use mimetype to determine what to download
- add meta-info (id3 tags probably) from feed to downloaded content 

    Copyright 2010 Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import urllib2
import feedparser
import optparse
import re
import os
import time
import sys

EXTENSIONS = ['wav', 'mp3', 'ogg', 'flac']

def check_commalist(option, opt, value):
    if not re.match("(\\w+,)*\\w+", value):
        raise OptionValueError("option %s: comma list isn't well formed or contains non alapha-numeric characters" % opt) 
    return [x for x in value.split(",")]

class CommaListOption(optparse.Option):
    TYPES = optparse.Option.TYPES + ("commalist",)
    TYPE_CHECKER = dict(optparse.Option.TYPE_CHECKER)
    TYPE_CHECKER['commalist'] = check_commalist


def get_links(regex, item):
    links = []
    if isinstance(item, dict):
        for key in item:
            links.extend(get_links(regex, item[key]))
    elif isinstance(item, list):
        for i in item:
            links.extend(get_links(regex, i))
    elif isinstance(item, unicode):
        for match in re.finditer(regex, item):
            links.append(match.group(0))
    return links

def download_file(link, dir, buffer=1024*1024):
    name = link.split("/")[-1]
    handler = urllib2.urlopen(link)
    file = open(os.path.join(dir, name), 'wb')
    data = handler.read(buffer)
    while data != "":
        file.write(data)
        data = handler.read(buffer)
    file.close()
    handler.close()


if __name__ == '__main__':
    parser = optparse.OptionParser(usage='%prog [options] feeds', option_class=CommaListOption)
    parser.add_option('-d', '--directory', dest='dir', metavar='DIR', default='.', help='downloaded podcasts will be saved in DIR. Default : current directory')
    parser.add_option('-e', '--extensions', dest='extensions', metavar='EXTENSIONS', default=EXTENSIONS, type='commalist',
            help="comma-seperated list of audio file extensions to look for. Default : %s " % ",".join(EXTENSIONS))
    parser.add_option('-f', '--force', dest='force', default=False, help='Flag to force overwriting of files if they already exist.', action='store_true')

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error('No feeds have been passed to the program !')

    file_regex = "http://\\S+\\.(%s)" % "|".join(options.extensions)
    links = []
    state = 0

    for feed_link in args:
        feed = feedparser.parse(feed_link)
        links.extend(get_links(file_regex, feed.entries))

    if len(links) == 0:
        print 'ERROR: no links have been found in the feeds !'
        sys.exit(1)

    for link in links:
        if link not in os.listdir(options.dir) or options.force:
            try:
                print "Started download of %s at %s" % (link, time.strftime("%x %X"))
                download_file(link, options.dir)
                print "Finished download of %s at %s" % (link, time.strftime("%x %X"))
            except Exception, e:
                state = 1
                print "ERROR : Error was encountered while downloading %s. Will proceed to next link. Error was : %s" % (file, e)

sys.exit(state)
