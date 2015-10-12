# coding=utf-8
from workflow import Workflow, web, ICON_WEB, ICON_INFO
import sys
import re

__author__ = 'benny'


class Rom:
    inner_reg = r'<form method="POST" action="(http://dfw.coolrom.com/dl/%s.*?)">'

    id = ''
    url = 'http://coolrom.com/dlpop.php?id=%s'
    name = ''
    downloadurl = ''

    def __init__(self, id, name):
        self.id = id
        self.url = self.url % self.id
        self.name = name
        self.inner_reg = self.inner_reg % self.id

    def downloadUrl(self):
        if not self.downloadurl:
            r = web.get(self.url)
            match = re.search(self.inner_reg, r.content)
            if match:
                self.downloadurl = match.group(1)
        return self.downloadurl


url_root = 'http://coolrom.com/'
raw_url = 'http://coolrom.com/search?q=%s'
raw_reg = r'<a href="(/roms/%s/(\d+)/.+?)">(.+?)</a>'


def main(wf):
    args = len(sys.argv)

    emulator = 'mame'
    query = ''

    if args >= 2 :
        query = ' '.join(sys.argv[1:])

    url = raw_url % query
    reg = raw_reg %  emulator
    r = web.get(url)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    # Parse the JSON returned by pinboard and extract the posts
    # print r.content
    matcher = re.findall(reg, r.content)
    if matcher:
        for i, sub in enumerate(matcher):
            rom = Rom(sub[1], sub[2])
            wf.add_item(title=rom.name, icon='zipfile.png', arg=rom.downloadUrl(), copytext=rom.downloadUrl(), valid=True)
            if i == 4:
                break
    else:
        wf.add_item(title='No roms found.', icon=ICON_INFO)


    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
