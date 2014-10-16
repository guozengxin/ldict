#!/usr/bin/env python
# encoding=utf-8

import sys
import os
import getopt
from ldutil import htmlfetcher
from ldutil.htmlparser import HtmlXPathParser
from ldutil import colorprint

outputEncoding = 'gb18030'
historyFile = os.path.join(os.path.expanduser('~'), '.iciba_history')
historyList = []


class _GetchUnix:

    def __init__(self):
        pass

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


getch = _GetchUnix()


def readHistory():
    global historyList, historyFile
    try:
        fp = open(historyFile, 'r')
        for line in fp:
            historyList.append(line.strip())
    except IOError:
        pass
    return len(historyList)


def writeHistory():
    global historyList, historyFile
    keepHistory = historyList[-1000:]
    fp = open(historyFile, 'w')
    for item in keepHistory:
        print >> fp, item
    fp.close()


def usage():
    print '''iciba.py [-d(--daemon)|-h(--help)|word]'''


def myinput(flag='> '):
    chars = []
    sys.stdout.write(flag)
    while True:
        newChar = getch()
        if newChar in '\r\n':
            print ''
            break
        elif newChar == '\b':
            if chars:
                del chars[-1]
                sys.stdout.write('\b \b')
        elif newChar in '\03\04':
            sys.exit(-1)
        elif ord(newChar) == 72:
            pass
        else:
            sys.stdout.write(newChar)
            chars.append(newChar)
    return ''.join(chars)


def parseOpt(args):
    config = {'daemon': False}
    try:
        opts, args = getopt.getopt(args, 'hd', ['help', 'daemon'])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-d', '--daemon'):
            config['daemon'] = True
        else:
            assert False, "unhandled option"
    return config, args


def getFirstText(tree, encoding=outputEncoding):
    try:
        if type(tree) is list:
            t = tree[0].text
        else:
            t = tree.text
        if t is not None:
            return t.encode(encoding)
        else:
            return ''
    except IndexError:
        return ''


def printResult(word, result):
    tColor = 'green'
    vColor = 'cyan'
    print word
    if len(result['prons']) > 0:
        print '发音'.decode('utf-8').encode(outputEncoding)
        for t, v in result['prons']:
            colorprint.colorPrint('  %s' % t, tColor, attr=1)
            colorprint.colorPrint('%s' % v, vColor, attr=4)
        print
    if len(result['groupPos']) > 0:
        print '释义'.decode('utf-8').encode(outputEncoding)
        for t, v in result['groupPos']:
            colorprint.colorPrint('  %s' % t, tColor, attr=1)
            colorprint.colorPrint(v, vColor, attr=4)
            print
    if len(result['netContent']) > 0:
        print '网络'.decode('utf-8').encode(outputEncoding)
        colorprint.colorPrint('  %s' % result['netContent'], vColor, attr=1)
        print


def parseHtml(data):
    result = {'prons': [], 'groupPos': [], 'netContent': []}
    parser = HtmlXPathParser()
    parser.feed(data, encode='utf-8')
    dictMainDiv = parser.etlist_xpath('//div[@id="dict_main"]')[0]
    tmpParser = HtmlXPathParser()
    tmpParser.feed_etree(dictMainDiv)
    pronsList = tmpParser.etlist_xpath('.//span[@class="fl"]')
    for prons in pronsList:
        pronsType = getFirstText(prons).strip('\r\n\t')
        pronsStr = getFirstText(prons.xpath('.//strong[@lang]')).strip()
        if pronsStr == '':
            pronsStr = getFirstText(prons.xpath('.//strong'))
        else:
            pronsStr = '[' + pronsStr + ']'
        if len(pronsType) == 0 and len(pronsStr) == 0:
            continue
        result['prons'].append([pronsType, pronsStr])
    groupPosList = tmpParser.etlist_xpath('.//div[@class="group_pos"]/p')
    for groupPos in groupPosList:
        posType = getFirstText(groupPos.xpath('.//strong'))
        if posType is None:
            continue
        posContent = ''
        contentList = groupPos.xpath('.//label//text()')
        for c in contentList:
            posContent += c.encode(outputEncoding)
        if len(posType) == 0 and len(posContent) == 0:
            continue
        result['groupPos'].append([posType, posContent])
    netContentList = tmpParser.etlist_xpath('.//div[@class="net_paraphrase"]/ul/li')
    netContent = ''
    for nc in netContentList:
        netContent += nc.text.encode(outputEncoding).strip()
    result['netContent'] = netContent

    return result


def translate(word):
    global historyList
    historyList.append(word)
    writeHistory()
    url = 'http://www.iciba.com/' + word.decode(outputEncoding).encode('utf8')
    home = 'http://www.iciba.com/'
    data = htmlfetcher.http_get(url, referer=home)
    if data is None:
        print >> sys.stderr, 'Fetch result from iciba.com failed!'
    else:
        result = parseHtml(data)
        printResult(word, result)


def main():
    config, args = parseOpt(sys.argv[1:])
    if config['daemon']:
        readHistory()
        while True:
            # line = raw_input('> ')
            line = myinput()
            word = line.strip()
            translate(word)
            sys.stdout.flush()
            sys.stderr.flush()
    else:
        if len(args) == 0:
            usage()
            sys.exit()
        word = args[0]
        translate(word)


if __name__ == '__main__':
    main()
