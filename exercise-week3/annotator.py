class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

import xml.etree.ElementTree as ET

tree = ET.parse('30zbtu.xml')
root = tree.getroot()

posts = {}

for p in root[0][1]:
    posts[p.attrib['id']] = p[3].text

parents = {}
for p in root[0][1]:
    if p[2].text in posts:
        parents[p.attrib['id']] = posts[p[2].text]
    else:
        parents[p.attrib['id']] = ""

with open('post_ids.txt', 'r') as f:
    id_list = f.read().split('\n')

    del id_list[-1]

n = 1;
nmax = len(id_list)

with open('annotation.txt','w') as f:
    for id in id_list:
        print 'Post id: ' + id + " (" + str(n) + "/" + str(nmax) + ")"
        print "Parent: " + parents[id]
        print "Post: " + posts[id]
        print "Hit n for negative, p for positive, q to quit."

        x = getch()
        while not (x ==  'n' or x == 'p' or x == 'q'):
            x = getch()

        if x == 'p':
            sentiment = 'positive'
        elif x == 'n':
            sentiment = 'negative'
        else:
            break

        f.write(id + "\t" + sentiment + "\n")
        print ""
        n = n + 1
