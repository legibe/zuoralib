import json
import xml.etree.ElementTree as ET
#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
class MultiFormat(object):
    
    def __init__(self):
        self._headers = { 'Content-Type': 'application/json' }

    def httpheaders(self):
        return self._headers

    def decode(self, headers, string):
        self._headers['Content-Type'] = headers['content-type']
        content = headers['content-type'].split(';')[0].split('/')[-1]
        return getattr(self,'from%s' % content)(string)

    def encode(self,data):
        return getattr(self,'to%s' % self._headers['Content-Type'].split(';')[0].split('/')[-1])(data)

    def fromjson(self,string):
        return json.loads(string)

    def tojson(self,data):
        return json.dumps(data)

    def fromxml(self,string):
        root = ET.fromstring(string)
        result = {}
        for child in root:
            if child.tag == 'parameter':
                result[child.attrib['name']] = child.text
        return result

    def toxml(self,data):
        header = '<?xml version="1.0" encoding="UTF-8"?><response>'
        footer = '</response>'
        params = []
        if isinstance(data,dict):
            for k,i in data.items():
                params.append('<parameter name="%s">%s</parameter>' % (k,i)) 
            s = header + ''.join(params) + footer
        else:
            s = str(data)
        return s
