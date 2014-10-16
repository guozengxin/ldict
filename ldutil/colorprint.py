#!/usr/bin/env python
# encoding=utf-8

'''
0  All attributes off 默认值
1  Bold (or Bright) 粗体 or 高亮
4  Underline 下划线
5  Blink 闪烁
7  Invert 反显
30 Black text
31 Red text
32 Green text
33 Yellow text
34 Blue text
35 Purple text
36 Cyan text
37 White text
40 Black background
41 Red background
42 Green background
43 Yellow background
44 Blue background
45 Purple background
46 Cyan background
47 White background
'''

textValues = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'purple': 35,
    'cyan': 36,
    'white': 37,
}

backValues = {
    'black': 40,
    'red': 41,
    'green': 42,
    'yellow': 43,
    'blue': 44,
    'purple': 45,
    'cyan': 46,
    'white': 47,
}


def baseColorPrint(message, attr=0, fore=37, back=40):
    colorStr = '\x1b[%d;%d;%dm' % (attr, fore, back)
    print '%s%s' % (colorStr, message),
    colorClear()


def colorPrint(message, fore='white', back='black', attr=1):
    baseColorPrint(message, attr=1, fore=textValues[fore], back=backValues[back])


def colorClear():
    print '\x1b[0m',
