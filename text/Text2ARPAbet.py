#!/usr/bin/python
# -*- coding: utf8 -*-
import re
import string

__up__ =    u'áắấéếíóốớúứý'
__down__ =  u'àằầèềìòồờùừỳ'
__hook__ =  u'ảẳẩẻểỉỏổởủửỷ'
__wave__ =  u'ãẵẫẽễĩõỗỡũữỹ'
__dot__ =   u'ạặậẹệịọộợụựỵ'

input = u'áàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ'
output= u'aaaaaăăăăăâââââeeeeeêêêêêiiiiioooooôôôôôơơơơơuuuuuưưưưưyyyyy'

class Text2ARPAbet(object):
    def __init__(self, str):
        self.str = str
        self.raw = str
        self.tone = 0

        # Phụ âm
        self.re_consonant = [
            [ur'b', u'B '],
            [ur'đ', u'D '],
            [ur'ph', u'F '],
            [ur'th', u'TCL '],
            [ur'tr', u'TSH '],
            [ur'd|gi', u'Z '],
            [ur'ch', u'CH '],
            [ur'ngh|ng', u'NG '],
            [ur'kh', u'KX '],
            [ur'gh|g', u'G '],
            [ur'nh', u'NH '],
            [ur't(?!(h|r))', u'T '],
            [ur'c(?!h)|k|q', u'K '],
            [ur'r', u'R '],
            [ur'h', u'HH '],
            [ur'm', u'M '],
            [ur'v', u'V '],
            [ur'n(?!(h|g))', u'N '],
            [ur'l', u'L '],
            [ur'x', u'S '],
            [ur'p(?!h)', u'P '],
            [ur's', u'AH ']
        ]

        # Bán nguyên âm
        self.re_halfvowel = [
            [ur'u(?!(ô|a))', u'W '],
            [ur'o(?=(a|ă|e))', u'W ']
        ]

        # Nguyên âm
        self.re_vowel = [
            [ur'ia|ya|iê|yê', u'IY IE '],
            [ur'uô|ua', u'UX '],
            [ur'ươ|ưa', u'IXO '],
            [ur'i|y', u'IY '],
            [ur'e', u'EH '],
            [ur'ê', u'EY '],
            [ur'a', u'AA '],
            [ur'ă', u'AA: '],
            [ur'â', u'AX '],
            [ur'o', u'AO '],
            [ur'ô', u'OW '],
            [ur'ơ', u'AX: '],
            [ur'u', u'UW '],
            [ur'ư', u'IX ']
        ]
        
    def clean(self):
        self.str = self.str.lower()
        self.tone = self.definite_tone()
        self.str = self.clear_tone()

    def definite_tone(self):
        try:
            for char in self.str:
                if char in __up__:
                    return 1 # sắc
                elif char in __down__:
                    return 2 # huyền
                elif char in __hook__:
                    return 3 # hỏi
                elif char in __wave__:
                    return 4 # ngã
                elif char in __dot__:
                    return 5 # nặng
            return 0 # không dấu
        except:
            return -1 # error

    def clear_tone(self):
        map = {ord(c): ord(t) for c, t in zip(input, output)}
        return self.str.translate(map)

    def convert(self):
        self.clean()

        for map in self.re_consonant:
            self.str = re.sub(re.compile(map[0], re.UNICODE), map[1], self.str)

        for map in self.re_halfvowel:
            self.str = re.sub(re.compile(map[0], re.UNICODE), map[1], self.str)

        for map in self.re_vowel:
            self.str = re.sub(re.compile(map[0], re.UNICODE), map[1], self.str)
        if self.str != u'' or self.str != u' ':
            self.str = self.str + str(self.tone) + '.'
        return self.str

if __name__ == '__main__':
    text = u"Hôm qua em đến trường"
    res = text.split(" ")
    for char in res:
        test = Text2ARPAbet(str=char)
        print test.convert()