#!/usr/bin/env python2
from fractions import Fraction
import ImageFile
import sys

"""
Print image aspect ratios

Hacked together by Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes
Requires the python imaging library (PIL)

I'm a huge anime fan and sometimes when I'm in a frenzy I'll blindly go
RAIDING TEH INTERNETZ for any anime wallpaper that I can find. The problem is
that afterwards I find myself with ~= 3GB of pictures in varying shapes and
sizes. So I quickly hacked this script to help me categorize the pictures more
easily.

Prints the aspect ratio (16/9, 4/3, etc) for the files passed on the command
line.

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

if len( sys.argv ) <= 1:
    print "USAGE : %s PICTURES" % sys.argv[1]
    sys.exit(1)

files = []
for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
        parser = ImageFile.Parser()
        parser.feed( f.read() )
        dimensions = parser.image.size
        ratio = Fraction(dimensions[0], dimensions[1])
        info = {
            'filename' : filename,
            'ratio' : ratio,
            'aspect' : float(dimensions[0]) / float(dimensions[1]),
        }
        files.append( info )

files.sort( key = lambda x: x['aspect'] )
for f in files:
    f['num'] = f['ratio'].numerator
    f['den'] = f['ratio'].denominator
    print "%(num)d/%(den)d\t(%(aspect).02f)\t: %(filename)s" % f

