#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from urllib import urlencode, urlopen
import re
from util import dump, load, dumpf,OrderedDict,load_all,save_all,index_by_title

END = '''<div class="no-results">No results matched your criteria.</div>'''

DYNAS1 = u"清宋"

CATES =[u"子部",u"史部",u"集部",u"經部"]

DYNAS2 = [
    u"明",u"元",u"唐",u"漢",u"晉",u"梁",u"後晉",u"魏",u"金",u"周",u"北齊",
    u"北周",u"吳",u"後魏",u"南唐",u"陳",u"隋",u"楚",u"五代",u"南朝宋",u"吴",
    u"後周",u"後蜀",u"隨",u"晋",u"遼",u"齊",u"苻秦",u"宋、明",u"清 清",u"蜀",
    u"義"]

URL = "https://archive.org/details/universallibrary?"

def make_url(page,args):
    l = [("scroll", 1),
         ("page", page),
         ("sort", "creatorSorter")]
    l.extend(
        [ ("and[]", 'subject:"%s"'%(a.encode('utf-8')))
          for a in args])

    return URL + urlencode(l)

ARGS = [(d,c) for d in DYNAS1 for c in CATES] + [(d,) for d in DYNAS2]

PATTERN = re.compile(r'''<a href="(/details/\d+.cn)" title="([^"]+)">''')

NAME = u"Universal Library - "


def fetch_with_cache(page, arg):
    filename = u'-'.join(arg+(u"%d"%page,))
    filename = u"cache/"+filename+u".yaml"
    try:
        f = open(filename, 'r')
        with f:
            return load(f)
    except:
        pass

    # response = urlopen(make_url(page, arg))
    # assert response.getcode() == 200
    # data = response.read()
    # if data == END:
    #     return

    # result = PATTERN.findall(data)
    # dumpf(result,filename)
    # return result
    return


def fetch(arg, entries):
    page = 1
    while True:
        print 'fetch', u" ".join(arg), 'page', page
        result = fetch_with_cache(page,arg)
        if result is None:
            return
        entries.extend(result)
        page += 1

entries = []

for arg in ARGS:
    fetch(arg, entries)

data = load_all()
by_title = index_by_title(data)

SEP = re.compile(ur'[·(\[]')


for url, title in entries:
    name = SEP.split(title)[0]

    o = by_title.get(name, None)
    if o is None:
        print title
        continue

    links = o[u"資料"]
    link_name = NAME + title
    if any((link[u"標題"] == link_name) for link in links):
        continue

    d = OrderedDict()
    d[u"標題"] = link_name
    d[u"網址"] = u"https://archive.org" + url
    d[u"限制"] = u"无"
    d[u"文字"] = False
    d[u"影印"] = True
    d[u"简体"] = False
    links.append(d)

save_all(data)
