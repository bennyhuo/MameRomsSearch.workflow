# coding=utf-8
import sys
import re
import web
from web import Response
from urllib2 import Request

__author__ = 'benny'


class Rom:
    id = ''
    name = ''
    size = ''
    downloadurl = 'http://edgeemu.net/download.php?id=%s'

    def __init__(self, index, id, name, size):
        self.index = int(index)
        self.id = id
        self.name = name
        self.size = size.upper()
        self.downloadurl = self.downloadurl % self.id

    def __str__(self):
        return '[%02d] %s - %s' % (self.index, self.name, self.size)

    def download(self):
        rsp = Response(Request(self.downloadurl))
        content_disposition = rsp.headers['Content-Disposition']

        filename = ''
        if content_disposition:
            match = re.search(r'filename="(.+?)"', content_disposition)
            if match:
                filename = match.group(1)

        if not filename:
            filename = self.name + '.zip'

        print '\nDownloading %s as %s ...' % (self, filename),
        rsp.save_to_path(filename)


raw_url = 'http://edgeemu.net/results.php?q=%s&system=%s'
pattern = r'<tr><td>(\d+)</td><td><a href="details-(\d+).htm">(.+?)</a></td><td>MAME .158 ROMs</td><td>(.+?)</td>'


def main():
    args = len(sys.argv)

    emulator = 'mame'
    query = ''

    if args >= 2:
        query = ' '.join(sys.argv[1:])

    print 'Searching for "%s", please wait ...' % query
    url = raw_url % (query, emulator)
    r = web.get(url)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    # Parse the JSON returned by pinboard and extract the posts
    # print r.content
    matcher = re.findall(pattern, r.content)

    roms = []
    if matcher:
        for i, sub in enumerate(matcher):
            rom = Rom(sub[0], sub[1], sub[2], sub[3])
            roms.append(rom)
            print rom
            if i == 50:
                break
    if len(roms) > 0:
        raw_inputs = raw_input(
            'Input indexes of roms to be downloaded seperated with a space, ie."1 2 5"[Default for all.]\n')
        raw_splits = raw_inputs.split(' ')

        for split in raw_splits:
            try:
                index = int(split)
                if index > len(roms):
                    print 'Invalid index "%s", ignore it.' % split
                    continue
                roms[index - 1].download()
            except ValueError:
                print 'Invalid index "%s", ignore it.' % split
    else:
        print 'No roms are found.'


if __name__ == u"__main__":
    main()
