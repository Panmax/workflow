#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import sys
from xml.etree import ElementTree as ET
from urllib import urlencode

# Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
reload(sys)
sys.setdefaultencoding('utf-8')


def find_zhanghao_url():
    request = urllib2.Request('http://www.521xunlei.com/')
    result = urllib2.urlopen(request).read().decode('gbk')
    str_index = result.find(u'爱密码迅雷共享')
    first_href_index = result.find('href', str_index)
    second_href_index = result.find('href', first_href_index)
    url = 'http://www.521xunlei.com/' + result[second_href_index+6:second_href_index+26]
    return url


def get_all_zhanghao(content):
    username_keyword = u'迅雷共享账号'
    password_keyword = u'密'

    last_index = 0
    all_zhanghao = []
    while True:
        username_index = content.find(username_keyword, last_index)
        password_index = content.find(password_keyword, username_index)
        end_index = content.find('<', password_index)
        last_index = end_index
        if username_index <= 0:
            break
        username = content[username_index+len(username_keyword):password_index]
        password = content[password_index+len(password_keyword):end_index]
        all_zhanghao.append((username, password))
    return all_zhanghao


def get_xlhy():
    url = find_zhanghao_url()
    request = urllib2.Request(url)
    content = urllib2.urlopen(request).read().decode('gbk')
    all_zhanghao = get_all_zhanghao(content)

    items = []
    for zhanghao in all_zhanghao:
        title = u'帐号:%s | 密码:%s' % (zhanghao[0], zhanghao[1])
        arg = '%s,%s' % (zhanghao[0], zhanghao[1])
        items.append({
            'uid': zhanghao[0],
            'title': title,
            'arg': arg,
            'description': zhanghao[0],
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
