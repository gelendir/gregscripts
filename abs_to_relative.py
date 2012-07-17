#!/usr/bin/env python
"""
HTML absolute to relative path converter

Hacked together by Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes
http://github.com/gelendir

This script requires the python package BeautifulSoup 4

Back in college when I was working on the HTCPCPD project
(http://github.com/gelendir/htcpcpd) the teacher told us
that all image and page paths had to be relative, NOT absolute
(so that it would be easier for him when he moved the web sites around).

Our problem was that the HTCPCPD website was generated using Jekyll, 
which hard-coded absolute paths. So, I hacked together this script to
parse every page and convert absolute paths to relative ones.

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

import sys
import os
import re

from bs4 import BeautifulSoup as Soup

regex = re.compile( r"^.+?://" )

def backpath( base, current ):

    return os.path.relpath( base, current )

def relpath( base, current, prefix, path ):

    return  backpath( base, current) + path[ len(prefix): ]

def transform_paths( elements, attr, base, current, prefix ):

    for tag in elements:
        tag[attr] = relpath( base, current, prefix, tag[attr] )

def transform_soup( soup, base, current, prefix ):

    condition = lambda x, attr: not regex.match( x[attr] ) if x.get(attr) else False

    links = soup.find_all( lambda x: condition( x, 'href' ) )
    images = soup.find_all( lambda x: condition( x, 'src' ) )

    transform_paths( links, 'href', base, current, prefix )
    transform_paths( images, 'src', base, current, prefix )

def transform_dir( base, prefix ):

    for ( dirpath, dirnames, filenames ) in os.walk( base ):

        for filename in ( x for x in filenames if x.endswith('html') ):

            filename = os.path.join( dirpath, filename )

            soup = Soup( open( filename, 'r' ).read() )
            transform_soup( soup, base, dirpath, prefix )
            with open( filename, 'w' ) as f:
                f.write( str( soup ) )
            print "file %s transformed" % filename

if __name__ == "__main__":

    if len( sys.argv ) < 3:
        print "USAGE: %s DIR PREFIX"
        sys.exit(1)

    base, prefix = sys.argv[1:]

    transform_dir( base, prefix )


