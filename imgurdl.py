from html.parser import HTMLParser
from urllib import request

"""
IMGur album downloader.

Hacked together by Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes

This script is python 3 compatible
(actually to work on python2 you need to change the imports)

Yet again, another small script I made when I needed to do something
but was too lazy to do it by hand.

As the name suggests, this script downloads all the pictures in an IMGur
album into the specified folder.

License:

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

import os.path
import re
import json
import sys

class ImgListScraper( HTMLParser ):

    IMG_URL = "http://i.imgur.com/{hash}{ext}"

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.in_javascript = False
        self.data = None

    def handle_starttag( self, tag, attrs ):

        attrs = dict( attrs )

        if tag == "script" and attrs['type'] == "text/javascript":
            self.in_javascript = True

    def handle_data( self, data ):

        if self.in_javascript:

            img_block = False
            for line in data.splitlines():

                if line.find("ImgurAlbum") > -1:
                    img_block = True
                elif img_block and line.strip().startswith("images:"):
                    data = line.strip()[ len( "images: " ) : -1 ]
                    self.data = json.loads( data )
                    img_block = False

            self.in_javascript = False

    def img_urls( self ):
        for image in self.data['items']:
            yield self.IMG_URL.format( **{
                    'hash': image['hash'],
                    'ext': image['ext']
                    })

def download_image( url, folder ):

    path = os.path.join( folder, url.split("/")[-1] )
    res = request.urlopen( url )

    with open( path, 'wb' ) as f:
        f.write( res.read() )

    res.close()

def download_album( album_url, folder ):

    print( "Scraping album..." )
    scraper = ImgListScraper()
    html = request.urlopen( album_url ).read().decode( 'utf8' )
    scraper.feed( html )

    total = scraper.data['count']

    for ( pos, img_url ) in enumerate( scraper.img_urls(), 1 ):

        print( "downloading {img_url} ({pos} of {total})".format( 
            img_url = img_url,
            pos = pos,
            total = total ) )

        download_image( img_url, folder )

if __name__ == '__main__':

    if len( sys.argv ) < 3:
        print( "Usage: {script} ALBUM_URL FOLDER".format( script = sys.argv[0]
            ) )
    else:
        download_album( sys.argv[1], sys.argv[2] )


