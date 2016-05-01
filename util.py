#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import yaml
from collections import OrderedDict

def load(stream):
    class Loader(yaml.CSafeLoader):
        pass

    def constructor(loader,node):
        return OrderedDict(loader.construct_pairs(node))

    Loader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        constructor)

    return yaml.load(stream, Loader=Loader)


def dump(data, stream=None):
    class Dumper(yaml.CSafeDumper):
        pass

    def representer(dumper, data):
        return dumper.represent_dict(data.iteritems())

    Dumper.add_representer(OrderedDict, representer)

    return yaml.dump(data, stream, Dumper=Dumper, encoding='utf-8', default_flow_style=False, allow_unicode=True)


def loadf(filename):
    print 'load', filename
    with open(filename,'r') as f:
        return load(f)

def dumpf(data, filename):
    print 'save', filename
    with open(filename,'w') as f:
        return dump(data, f)

DIRS = u"經史子集"

def load_all():
    return {
        x:
        {y[:-5]: loadf(x+u"/"+y)
         for y in os.listdir(x)
         if y.endswith(u".yaml")}
        for x in DIRS}

def save_all(data):
    for x, d in data.iteritems():
        for y, o in d.iteritems():
            dumpf(o,x+u"/"+y+u".yaml")

def index_by_title(data):
    return {o[u"題目"]: o
            for _,x in data.iteritems()
            for _,y in x.iteritems()
            for _,z in y.iteritems()
            for o in z}
