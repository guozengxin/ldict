#!/usr/bin/env python
# coding=utf-8

import StringIO
import logging
import re

from lxml import etree

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y%m%d %H:%M:%S')


class HtmlXPathParser:
    '''parse html with xpath
    '''
    def __init__(self):
        self.tree = None

    def feed(self, data, encode='utf-8', isgzip=False):
        '''input data to HtmlXPathParser object
        feed(self, data, encoding='utf-8')
        '''
        if isgzip:
            import gzip
            gzipper = gzip.GzipFile(fileobj=StringIO.StringIO(data))
            data = gzipper.read()
        parser = etree.HTMLParser(encoding=encode)
        self.tree = etree.parse(StringIO.StringIO(data), parser)

    def feed_etree(self, tree):
        '''assign tree by a argument
        '''
        self.tree = tree

    def etlist_xpath(self, xpath):
        '''return ElementTree list by a xpath str
        etlist_xpath(self, xpath)
        '''
        return self.tree.xpath(xpath)

    def attrlist_xpath(self, xpath, attr):
        '''return attribute list by a xpath str and attribute name
        attrlist_xpath(self, xpath, attr)
        '''
        ret = []
        etlist = self.tree.xpath(xpath)
        for et in etlist:
            ret.append(et.attrib[attr])
        return ret

    def textlist_xpath(self, xpath, encode=None):
        '''return text list by a xpath str, provide encode if need
        textlist_xpath(self, xpath, encode=None)
        '''
        ret = []
        etlist = self.tree.xpath(xpath)
        for et in etlist:
            if encode is not None:
                text = et.text.encode(encode)
            else:
                text = et.text
            ret.append(text)
        return ret

    def attr_text_from_tag_a(self, xpath, attr, attrencode=None, textencode=None):
        '''return a list, each element contains a attr ans text, which is parsed from xpath str. provide encode if need.
        attr_text_from_tag_a(self, xpath, attr, attrencode = None, textencode = None)
        '''
        ret = []
        etlist = self.tree.xpath(xpath)
        for et in etlist:
            if textencode is None:
                text = et.text
            else:
                text = et.text.encode(textencode)
            if attrencode is None:
                attrcontent = et.attrib[attr]
            else:
                attrcontent = et.attrib[attr].encode(attrencode)
            ret.append({attr: attrcontent, 'text': text})
        return ret

    def first_et_xpath(self, xpath):
        '''return the first element by a xpath
        first_et_xpath(self, xpath)
        '''
        etlist = self.tree.xpath(xpath)
        if len(etlist) > 0:
            return etlist[0]
        else:
            return None

    def first_attr_xpath(self, xpath, attr, attrencode=None):
        '''return attr of the first element, provide encode if need.
        '''
        et = self.first_et_xpath(xpath)
        if et is not None and attr in et.attrib:
            text = et.attrib[attr]
            if attrencode is not None:
                text = text.encode(attrencode)
            return text
        else:
            return None

    def first_text_xpath(self, xpath, textencode=None):
        '''return text of the first element, provide encode if need.
        '''
        et = self.first_et_xpath(xpath)
        if et is not None and et.text:
            if textencode is not None:
                text = et.text.encode(textencode)
            else:
                text = et.text
            return text
        else:
            return None

    def first_attr_text_xpath(self, xpath, attr, attrencode=None, textencode=None):
        '''return attr and text of the first element, provide encode if need
        '''
        ret = {}
        et = self.first_et_xpath(xpath)
        if et is not None and attr in et.attrib:
            attrtext = et.attrib[attr]
            if attrencode is not None:
                attrtext = attrtext.encode(attrencode)
            ret[attr] = attrtext
        else:
            ret[attr] = None
        if et is not None:
            if textencode is not None:
                ret['text'] = et.text.encode(textencode)
            else:
                ret['text'] = et.text
        else:
            ret['text'] = None
        return ret

    def first_attrs_xpath(self, xpath, attrs, attrencode=None):
        '''return attrs of the first element, provide encode if need
        '''
        ret = {}
        et = self.first_et_xpath(xpath)
        for attr in attrs:
            if et is not None and attr in et.attrib:
                attrtext = et.attrib[attr]
                if attrencode is not None:
                    attrtext = attrtext.encode(attrencode)
                ret[attr] = attrtext
            else:
                ret[attr] = None
        return ret

    def first_attrs_text_xpath(self, xpath, attrs, attrencode=None, textencode=None):
        '''return attrs and text of the first element, provice encode if need
        '''
        ret = {}
        et = self.first_et_xpath(xpath)
        for attr in attrs:
            if et is not None and attr in et.attrib:
                attrtext = et.attrib[attr]
                if attrencode is not None:
                    attrtext = attrtext.encode(attrencode)
                ret[attr] = attrtext
            else:
                ret[attr] = None
        if et is not None:
            if textencode is not None:
                ret['text'] = et.text.encode(textencode)
            else:
                ret['text'] = et.text
        else:
            ret['text'] = None
        return ret

    @classmethod
    def fetch_encoding(cls, data):
        '''从原网页html中分析网页的encoding
        '''
        encode = None
        pattern = re.compile('content=\"[\w/]+;\W+charset=(.*?)\"')
        m = pattern.search(data)
        if m:
            encode = m.group(1).strip()

        if encode is None:
            pattern = re.compile('<meta.*charset=\"(.*)\"')
            m = pattern.search(data)
            if m:
                encode = m.group(1).strip()

        if encode is None:
            pattern = re.compile('<meta.*charset=(.*)')
            m = pattern.search(data)
            if m:
                encode = m.group(1).strip()

        if encode == 'gb2312' or encode == 'gbk':
            encode = 'gb18030'

        if encode is None:
            encode = 'gb18030'

        return encode


class UrlNormalize:
    def __init__(self):
        self.patternset = []

    def initialize(self, pattern_file):
        fp = open(pattern_file, 'r')
        lines = fp.readlines()
        for line in lines:
            arr = line.strip().split('\t')
            self.patternset.append([arr[0], arr[1]])
        fp.close()

    def normal(self, url):
        for p1, p2 in self.patternset:
            if re.search(p1, url):
                url = re.sub(p1, p2, url)
        return url
