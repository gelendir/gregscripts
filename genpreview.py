#!/usr/bin/python2
"""
Preview Generator

Hacked together by Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes

I needed to select a bunch of pictures in a folder (and their sub-folders)
and do some processing on them with a bash script. Having nothing better to do,
I made this script. It generates a HTML page with thumbnails of all the pictures
in a folder.  A list of pictures that you have clicked on will appear at the
bottom of the page. Copy/paste the list and do something with it
through bash + xargs

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
import Image

HEADER = """
<html>
<head>
    <title>Simple thumbnail generator (http://github.com/gelendir)</title>

    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>

    <style type="text/css">
        table {
            width: 100%;
        }

        img {
            width: 100%;
        }

        td {
            padding: 3px 3px 3px 3px;
            border: 2px solid gray;
        }

        .dim {
            opacity: 0.2;
        }
    </style>

    <script type="text/javascript">

    $( function() {
        var selected = [];

        $("img").click( function() {

            var file = $(this).attr("src");
            var img = $(this);

            if( img.hasClass("dim") ) {
                img.removeClass("dim");
                selected.splice( $.inArray( file, selected ), 1 );
            } else {
                img.addClass("dim");
                selected.push( file );
            }

            $("#remove").empty();
            for( index in selected ) {
                file = selected[index];
                $("#remove").append(file + "<br />");
            }

        });
    });
    </script>

</head>
<body>
<table>
<tr>
"""
FOOTER = """
</tr>
</table>

<div id="remove">
</div>

</body>
</html>
"""

EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
COLUMNS = 3
SCREEN_SIZE = ( 1280, 800 )

def is_image_file( path ):

    extension = path.lower().split(".")[-1]
    return extension in EXTENSIONS

def image_files( dirpath, filelist, target_folder ):

    images = []
    for f in filelist:

        path = os.path.join( target_folder, dirpath, f )

        exists = os.path.isfile( path )

        if is_image_file( f ) and not exists:
            images.append( f )

    return images

def resize_images( folder, target_folder, thumbnail ):

    for(dirpath, dirnames, filenames) in os.walk( folder ):

        destination_folder = os.path.join( target_folder, dirpath )

        if not os.path.isdir( destination_folder ):
            os.mkdir( destination_folder )

        for filename in image_files( dirpath, filenames, target_folder ):

            origin = os.path.join( dirpath, filename )
            destination = os.path.join( destination_folder, filename )

            print( "resizing {0}".format( origin ) )

            image = Image.open( origin )
            image.thumbnail( thumbnail, Image.ANTIALIAS )
            image.convert('RGB').save( destination, "JPEG" )


def create_html_file( origin_folder, target_folder, columns ):

    destination = os.path.join( target_folder, "index.html" )
    tmpl = '<td><img src="{filename}" /></td>'
    counter = 1

    with open( destination, 'w' ) as html:

        html.write( HEADER )

        for (dirpath, dirnames, filenames) in os.walk( origin_folder ):

            filenames = ( f for f in filenames if is_image_file( f ) )
            for (pos, filename) in enumerate( filenames ):

                path = "/".join([dirpath, filename])
                code = tmpl.format( filename = path )
                html.write( code )

                if counter % columns == 0:
                    html.write("</tr><tr>")

                counter += 1

        html.write( FOOTER )

def main():

    if len( sys.argv ) < 3:
        print( "USAGE: {0} SOURCE_DIR DEST_DIR [COLUMNS] [SCREEN_WIDTH SCREEN_HEIGHT]".format( sys.argv[0] ) )
        sys.exit(1)

    columns = COLUMNS
    screen_size = SCREEN_SIZE

    origin_folder = sys.argv[1]
    target_folder = sys.argv[2]

    if len( sys.argv ) >= 4:
        columns = int( sys.argv[3] )
    if len( sys.argv ) >= 6:
        screen_size = ( int( x ) for x in sys.argv[5:7] )

    thumbnail = (
        screen_size[0] / columns,
        screen_size[1] / columns )

    if not os.path.isdir( target_folder ):
        os.mkdir( target_folder )

    resize_images( origin_folder, target_folder, thumbnail )
    create_html_file( origin_folder, target_folder, columns )

if __name__ == "__main__":
    main()

