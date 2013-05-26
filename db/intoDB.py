#!/usr/bin/python2

#
# poiimport - import nodes from OSM into a spatialite DB
#
# Copyright (C) 2010  Enrico Zini <enrico@enricozini.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# or see <http://www.gnu.org/licenses/>.
#

from pysqlite2 import dbapi2 as sqlite
import xml.sax
import xml.sax.handler
import sys
import os

class OSMPOIReader(xml.sax.handler.ContentHandler):
    '''
    Filter SAX events in a OSM XML file to keep only nodes with names
    '''
    def __init__(self, consumer):
        self.consumer = consumer

    def startElement(self, name, attrs):
        if name == "node":
            self.attrs = attrs
            self.tags = dict()
        elif name == "tag":
            self.tags[attrs["k"]] = attrs["v"]

    def endElement(self, name):
        if name == "node":
            lat = float(self.attrs["lat"])
            lon = float(self.attrs["lon"])
            id = int(self.attrs["id"])

            self.consumer(lat, lon, id, self.tags )

class Importer(object):
    '''
    Create the spatialite database and populate it
    '''

    def __init__(self, filename, country):
        self.db = sqlite.connect(filename) #connect to DB
        self.country = country


    def __call__(self, lat, lon, id, tags):
        name = tags.get("name",None)
        if name is None: return #we don't want places we cannot name

        self.db.execute("INSERT INTO ice (id, lat , lon, name, country)"
                        "     VALUES (?, ?, ?, ?, ?)", 
                (id, lat, lon, name, self.country))

    def done(self):
        self.db.commit()

# Get the DB file name
filename = sys.argv[1]
country = sys.argv[2]

# Import
parser = xml.sax.make_parser()
importer = Importer(filename, country)
handler = OSMPOIReader(importer)
parser.setContentHandler(handler)
parser.parse(sys.stdin)
importer.done()
