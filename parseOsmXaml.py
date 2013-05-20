#!/usr/bin/python

#
# poifilter - extract interesting nodes from OSM XML files
#
# Copyright (C) 2010  Enrico Zini <enrico@enricozini.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
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
#


import xml.sax
import xml.sax.handler
import xml.sax.saxutils
import sys

class XMLSAXFilter(xml.sax.handler.ContentHandler):
    '''
    A SAX filter that is a ContentHandler.

    There is xml.sax.saxutils.XMLFilterBase in the standard library but it is
    undocumented, and most of the examples using it you find online are wrong.
    You can look at its source code, and at that point you find out that it is
    an offensive practical joke.
    '''
    def __init__(self, downstream):
        self.downstream = downstream

    # ContentHandler methods

    def setDocumentLocator(self, locator):
        self.downstream.setDocumentLocator(locator)

    def startDocument(self):
        self.downstream.startDocument()

    def endDocument(self):
        self.downstream.endDocument()

    def startPrefixMapping(self, prefix, uri):
        self.downstream.startPrefixMapping(prefix, uri)

    def endPrefixMapping(self, prefix):
        self.downstream.endPrefixMapping(prefix)

    def startElement(self, name, attrs):
        self.downstream.startElement(name, attrs)

    def endElement(self, name):
        self.downstream.endElement(name)

    def startElementNS(self, name, qname, attrs):
        self.downstream.startElementNS(name, qname, attrs)

    def endElementNS(self, name, qname):
        self.downstream.endElementNS(name, qname)

    def characters(self, content):
        self.downstream.characters(content)

    def ignorableWhitespace(self, chars):
        self.downstream.ignorableWhitespace(chars)

    def processingInstruction(self, target, data):
        self.downstream.processingInstruction(target, data)

    def skippedEntity(self, name):
        self.downstream.skippedEntity(name)

class OSMPOIHandler(XMLSAXFilter):
    '''
    Filter SAX events in a OSM XML file to keep only nodes with names
    '''
    PASSTHROUGH = ["osm", "bound"]
    #TAG_WHITELIST = set(["amenity", "shop", "tourism", "place"])
    VAL_WHITELIST = set(["ice_cream"])

    def startElement(self, name, attrs):
        if name in self.PASSTHROUGH:
            self.downstream.startElement(name, attrs)
        elif name == "node":
            self.attrs = attrs
            self.tags = []
            self.propagate = False
        elif name == "tag":
            if self.tags is not None:
                self.tags.append(attrs)
                #if attrs["k"] in self.TAG_WHITELIST:
                #TODO: account for typos and things such as amenity:cafe;ice_cream
                if attrs["v"] in self.VAL_WHITELIST:
                    self.propagate = True
        else:
            self.tags = None
            self.attrs = None

    def endElement(self, name):
        if name in self.PASSTHROUGH:
            self.downstream.endElement(name)
        elif name == "node":
            if self.propagate:
                self.downstream.startElement("node", self.attrs)
                for attrs in self.tags:
                    self.downstream.startElement("tag", attrs)
                    self.downstream.endElement("tag")
                self.downstream.endElement("node")

    def ignorableWhitespace(self, chars):
        pass

    def characters(self, content):
        pass

# Simple stdin->stdout XMl filter
parser = xml.sax.make_parser()
handler = OSMPOIHandler(xml.sax.saxutils.XMLGenerator(sys.stdout, "utf-8"))
parser.setContentHandler(handler)
parser.parse(sys.stdin)
