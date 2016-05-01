#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from util import load_all,dump

data = load_all()

PAGE_TMPL = u'''<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>{title}</title>
</head>
<body>
<h1>{title}</h1>
<table>
<thead>
<tr>
<th></th>
<th>文字</th>
<th>影印</th>
<th>简体</th>
<th>限制</th>
</tr>
</thead>
<tbody>
{table}
</tbody>
</table>
</body>
</html>
'''

HAVE = {True:u"有", False:u"无"}

def render_page_row(link):
    return u'''<tr><td><a href="%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>''' % (
        link[u"網址"],link[u"標題"],
        HAVE[link[u"文字"]],
        HAVE[link[u"影印"]],
        HAVE[link[u"简体"]],
        link[u"限制"])


def render_page(x,y,o):
    title = o[u"題目"]
    table = u"\n".join(render_page_row(link) for link in o[u"資料"])

    with open(u"html/"+x +u"/"+y +u"/"+title+u".html","w") as f:
        f.write(PAGE_TMPL.format(title=title,table=table).encode('utf-8'))


def render_list_row(y,o):
    return u'''<tr><td>%s</td><td>%s</td><td><a href="%s">%s</a></td></tr>'''%(
        o[u'朝代'] or u'N/A',
        o[u'作者'] or u'N/A',
        y + u"/" + o[u'題目']  + u".html",
        o[u'題目'])


SUBLST_TMPL = u'''<h2>{title}</h2>
<table>
<thead>
<tr>
<th>朝代</th>
<th>作者</th>
<th></th>
</tr>
</thead>
<tbody>
{table}
</tbody>
</table>
'''


def render_sublist(y,z,l):
    table = "\n".join(render_list_row(y,o) for o in l)
    return SUBLST_TMPL.format(title=z or 'N/A',table=table)

LIST_TMPL = u'''<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>{title}</title>
</head>
<body>
<h1>{title}</h1>
{body}
</body>
</html>
'''

def render_list(x,y,d):
    body = u"\n".join(render_sublist(y,z,l) for z,l in d.iteritems())

    with open(u"html/"+x +u"/"+y +u".html","w") as f:
        f.write(LIST_TMPL.format(title=y,body=body).encode('utf-8'))


for x, ds in data.iteritems():
    try:
        os.makedirs(u"html/"+x)
    except:
        pass

    for y, d in ds.iteritems():
        try:
            os.makedirs(u"html/"+x +u"/"+y)
        except:
            pass

        for _, l in d.iteritems():
            for o in l:
                render_page(x,y,o)

        render_list(x,y,d)


import urlparse
from docutils.core import publish_doctree, publish_from_doctree
from docutils import nodes


with open("README.rst", "r") as f:
    rst = f.read()

doc = publish_doctree(rst)
for node in doc.traverse(nodes.reference):
    uri = urlparse.urlparse(node['refuri'])
    if not uri.netloc and uri.path.endswith(".yaml"):
        node['refuri'] = urlparse.urlunparse(
            (uri.scheme, uri.netloc, uri.path[:-5] + ".html", uri.params, uri.query, uri.fragment))

output = publish_from_doctree(
    doc,
    writer_name='html4css1',
    destination_path="index.html",
    settings_overrides = {
        'stylesheet_path': [],
        'embed_stylesheet': False,
        'xml_declaration': False})

with open("html/index.html", "w") as f:
    f.write(output)
