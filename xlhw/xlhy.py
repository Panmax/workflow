#!/usr/bin/env python
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import urllib2
import json
import sys
from xml.etree import ElementTree as ET
from urllib import urlencode, urlopen

# Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
reload(sys)
sys.setdefaultencoding('utf-8')


class HandleHtml(HTMLParser):
    def __init__(self):
        self.data = []
        self.is_find = False
        self.zhanghao = ''
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'font':
            for name, value in attrs:
                if name == 'size' and value == '4':
                    self.is_find = True

    def handle_data(self, data):
        if self.is_find and not (data.find('(') >= 0 and data.find(')') >= 0 or data.find(u'点击查看') >= 0):
            self.zhanghao = data

    def handle_endtag(self, tag):
        if tag == 'font':
            if self.zhanghao and len(self.zhanghao.strip()):
                self.data.append(self.zhanghao)
            self.zhanghao = ''
            self.is_find = False

    def get_result(self):
        return self.data


def find_zhanghao_url():
    request = urllib2.Request('http://www.521xunlei.com/')
    result = urllib2.urlopen(request).read().decode('gbk')
    str_index = result.find(u'爱密码迅雷共享')
    first_href_index = result.find('href', str_index)
    second_href_index = result.find('href', first_href_index)
    url = 'http://www.521xunlei.com/' + result[second_href_index+6:second_href_index+26]
    return url


def get_all_zhanghao(content):
    parser = HandleHtml()
    parser.feed(content)
    all_zhanghao = parser.get_result()

    return all_zhanghao


def get_xlhy():
    url = find_zhanghao_url()
    request = urllib2.Request(url)
    content = urllib2.urlopen(request).read().decode('gbk')
    all_zhanghao = get_all_zhanghao(content)

    items = []
    for zhanghao in all_zhanghao:
        title = zhanghao
        arg = zhanghao
        items.append({
            'uid': zhanghao,
            'title': title,
            'arg': arg,
            'description': zhanghao,
            'icon': 'icon.jpg',
        })
    xml = generate_xml(items)
    return xml


def generate_xml(items):
    xml_items = ET.Element('items')
    for item in items:
        xml_item = ET.SubElement(xml_items, 'item')
        for key in item.keys():
            if key in ('arg',):
                xml_item.set(key, item[key])
            else:
                child = ET.SubElement(xml_item, key)
                child.text = item[key]
    return ET.tostring(xml_items)

if __name__ == '__main__':
    print get_xlhy()

