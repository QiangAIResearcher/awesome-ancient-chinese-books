#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
from urllib import urlopen
from util import OrderedDict,load_all,save_all,index_by_title, dump

PATTERN = re.compile(r'''<a href="(/text/[^"]+/)"[^>]*>[^<]+</a></td>\s*<td [^>]*>([^-]*)-([^-]*)-([^<]*)</td>''')

def fetch_all_entries():
    result = []

    for i in xrange(1,7):
        response = urlopen("https://www.kanripo.org/catalog?coll=KR%d"%i)
        data = response.read()
        result.extend(PATTERN.findall(data))

    return result


entries = fetch_all_entries()

NAME = u"Kanripo 漢籍リポジトリ"

data = load_all()
by_title = index_by_title(data)

for url, title, dyna, auth in entries:
    url = url.decode("utf-8")
    title = title.decode("utf-8")
    dyna = dyna.decode("utf-8")
    auth = auth.decode("utf-8")

    o = by_title.get(title, None)

    if o is None:
        print title
        continue

    links = o[u"資料"]

    if any((link[u"標題"] == NAME) for link in links):
        continue

    d = OrderedDict()
    d[u"標題"] = NAME
    d[u"網址"] = u"https://www.kanripo.org" + url
    d[u"限制"] = u"无"
    d[u"文字"] = True
    d[u"影印"] = False
    d[u"简体"] = False
    links.append(d)

    if o[u"朝代"] is None:
        if dyna:
            o[u"朝代"] = dyna

    if o[u"作者"] is None:
        if auth:
            o[u"作者"] = auth

save_all(data)
