#!/usr/bin/python
'''
Extract _("...") strings for translation and convert to Qt4 stringdefs so that
they can be picked up by Qt linguist.
'''
from subprocess import Popen, PIPE

OUT_CPP="src/qt/bitcoinstrings.cpp"
EMPTY=['""']

def parse_po(text):
    """
    Parse 'po' format produced by xgettext.
    Return a list of (msgid,msgstr) tuples.
    """
    messages = []
    msgid = []
    msgstr = []
    in_msgid = False
    in_msgstr = False

    for line in text.split('\n'):
        line = line.rstrip('\r')
        if line.startswith('msgid '):
            if in_msgstr:
                messages.append((msgid, msgstr))
                in_msgstr = False
            # message start
            in_msgid = True
            
            msgid = [line[6:]]
        elif line.startswith('msgstr '):
            in_msgid = False
            in_msgstr = True
            msgstr = [line[7:]]
        elif line.startswith('"'):
            if in_msgid:
                msgid.append(line)
            if in_msgstr:
                msgstr.append(line)

    if in_msgstr:
        messages.append((msgid, msgstr))

    return messages

files = ['src/base58.h', 'src/bignum.h', 'src/db.cpp', 'src/db.h', 'src/headers.h', 'src/init.cpp', 'src/init.h', 'src/irc.cpp', 'src/irc.h', 'src/key.h', 'src/main.cpp', 'src/main.h', 'src/net.cpp', 'src/net.h', 'src/noui.h', 'src/script.cpp', 'src/script.h', 'src/serialize.h', 'src/strlcpy.h', 'src/uint256.h', 'src/util.cpp', 'src/util.h']

# xgettext -n --keyword=_ $FILES
child = Popen(['xgettext','--output=-','-n','--keyword=_'] + files, stdout=PIPE)
(out, err) = child.communicate()

messages = parse_po(out) 

f = open(OUT_CPP, 'w')
f.write('#include <QtGlobal>\n')
f.write('// Automatically generated by extract_strings.py\n')
f.write('static const char *bitcoin_strings[] = {')
for (msgid, msgstr) in messages:
    if msgid != EMPTY:
        f.write('QT_TRANSLATE_NOOP("bitcoin-core", %s),\n' % ('\n'.join(msgid)))
f.write('};')
f.close()