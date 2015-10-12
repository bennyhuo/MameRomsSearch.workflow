# coding=utf-8
from workflow import Workflow, web, ICON_WEB, ICON_INFO
import sys
import re

__author__ = 'benny'


class Rom:
    id = ''
    name = ''
    size = ''
    downloadurl = 'http://edgeemu.net/download.php?id=%s'

    def __init__(self, id, name, size):
        self.id = id
        self.name = name
        self.size = size.upper()
        self.downloadurl = self.downloadurl % self.id


raw_url = 'http://edgeemu.net/results.php?q=%s&system=%s'
pattern = r'<tr><td>(\d+)</td><td><a href="details-(\d+).htm">(.+?)</a></td><td>MAME .158 ROMs</td><td>(.+?)</td>'

def main(wf):
    args = len(sys.argv)

    emulator = 'mame'
    query = ''

    if args >= 2:
        query = ' '.join(sys.argv[1:])

    url = raw_url % (query, emulator)
    r = web.get(url)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    # Parse the JSON returned by pinboard and extract the posts
    # print r.content
    matcher = re.findall(pattern, r.content)
    if matcher:
        for i, sub in enumerate(matcher):
            rom = Rom(sub[1], sub[2], sub[3])
            wf.add_item(title=rom.name, subtitle=rom.size + ' - MAME .158 ROMs', icon='zipfile.png',
                        arg=rom.downloadurl, copytext=rom.downloadurl,
                        valid=True)
            if i == 50:
                break
    else:
        wf.add_item(title='No roms found.', icon=ICON_INFO)

    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
