#!/usr/bin/env python
"""
Anime manager

Hacked together by Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes
http://github.com/gelendir

This script is python 3 compatible.

4 reasons why I made this script:

 * I'm a huge japan anime fan (especially fansubs)
 * I like it when my files are neatly organized
 * I was tired of always going through all the files in my Download folder
 * I'm lazy

So, Instead of doing all the boring work myself, I wrote a script to do it.
This script scans a folder for anime files made by fansubbers, regroups
the files by anime serie, creates a folder for each serie and moves the files
accordingly. 

Examples of common anime filenames :

 * [BD]_Bleach_-_202_[A3DR5G34].avi
 * [Commie] Fairy Tail - 45 [720p][V54ER12U].mkv

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
import re
import os
import shutil
import sys

REGEX = r"^\[(.+?)\](.+?)(-[ _](\d+))(.*?)(\[(\w{8})\])?\.(mkv|avi|mp4)$"
regex = re.compile( REGEX )

def normalize_name( name ):
    return name.replace("_", " ").strip()

def find_anime_files( filelist ):

    matching = []
    for filename in filelist:
        match = regex.search( filename )
        if match:
            matching.append( match )

    return matching

def regroup_anime( matches ):

    library = {}
    for match in matches:
        anime = normalize_name( match.group(2) )
        library.setdefault( anime, [] ).append( match.group(0) )

    return library

def folder_name( anime ):

    return anime.lower().replace(" ", "_")

def move_files( origin_folder, target_folder, library ):

    for (anime, files) in library.items():

        anime_folder = folder_name( anime )
        target = os.path.join( target_folder, anime_folder )

        if not os.path.isdir( target ):
            print("making dir {0}".format( target ) )
            os.mkdir( target )

        for filename in files:
            location = os.path.join( origin_folder, filename )
            print("moving {0} to {1}".format( location, target ) )
            shutil.move( location, target )

def main():

    if len( sys.argv ) < 3:
        print("USAGE: {0} ORIGIN_DIR TARGET_DIR".format( sys.argv[0] ) )
        sys.exit(1)

    origin_dir = sys.argv[1]
    target_dir = sys.argv[2]

    if not os.path.isdir( origin_dir ):
        print("ERROR: ORIGIN_DIR does not exist or is not a directory")
        sys.exit(1)
    elif not os.path.isdir( target_dir ):
        print("ERROR: TARGET_DIR does not exist or is not a directory")
        sys.exit(1)

    files = os.listdir( origin_dir )
    matches = find_anime_files( files )
    library = regroup_anime( matches )
    move_files( origin_dir, target_dir, library )

if __name__ == "__main__":
    main()
