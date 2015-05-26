#!/usr/bin/env python
import sys
import os
from collections import OrderedDict


# {keyword : app}
myapps = {
    'apple': 'apple apps',
    'google': 'google apps',
    'renren': 'renren',
    'sina': 'weibo',
    'weibo': 'weibo',
    'baidu': 'baidu apps',
    'skype': 'skype',
    'adobe': 'adobe reader',
    'piazza': 'piazza',
    'tencent': 'tencent QQ/WeChat',
    'dropbox': 'Dropbox',
    'facebook': 'Facebook',
    'twitter': 'Twitter',
    'wikipedia': 'Wikipedia',
    'bankofamerica': 'BofA',
    'linkedin': 'LinkedIn',
    'amazon': 'Amazon.com',
    'yahoo': 'Yahoo.com',
}


def loadanddedup(orgmapfile):
    dedupmap = {}
    with open(orgmapfile, 'r') as f:
        for line in f:
            parts = line.split('<->')
            orgname = parts[0]
            count = int(parts[1])
            if orgname in dedupmap:
                dedupmap[orgname] += count
            else:
                dedupmap[orgname] = count
    return dedupmap


def mapappanddedup(orgmap):
    appmap_deduped = {}
    for orgname, count in orgmap.items():
        orgname = orgname.lower()
        for keyword, appname in myapps.items():
            # found an app
            if keyword in orgname:
                if appname in appmap_deduped:
                    appmap_deduped[appname] += count
                else:
                    appmap_deduped[appname] = count
                break
    return appmap_deduped


def sort(map):
    key_list = sorted(map, key=map.get, reverse=True)
    od = OrderedDict({})
    for key in key_list:
        od[key] = map[key]
    return od


def savemap(map, path, filename):
    with open('/'.join([path, filename]), 'w') as f:
        for k, v in map.items():
            f.write('%s %d\n' % (k, v))


def main():
    orgmapfile = sys.argv[1]
    orgmap_deduped = loadanddedup(orgmapfile)
    appmap_deduped = mapappanddedup(orgmap_deduped)
    outpath = os.path.dirname(orgmapfile)
    savemap(sort(appmap_deduped), outpath, 'appmap.deduped.txt')
    savemap(sort(orgmap_deduped), outpath, 'orgmap.deduped.txt')


if __name__ == '__main__':
    main()
