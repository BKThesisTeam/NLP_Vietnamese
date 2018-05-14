#!/usr/bin/python
# -*- coding: utf8 -*-
import re

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

        # Phụ âm 23
        self.re_consonant = [
            [u'b', u'B '],
            [u'đ', u'D '],
            [u'ph', u'F '],
            [u'th', u'TH '],
            [u'tr', u'TSH '],
            [u'd|gi', u'Z '],
            [u'ch', u'CH '],
            [u'ngh|ng', u'NG '],
            [u'kh', u'X '],
            [u'gh|g', u'G '],
            [u'nh', u'NH '],
            [u't(?!(h|r))', u'T '],
            [u'qu', u'KW '],
            [u'c(?!h)|k|q', u'K '],
            [u'r', u'R '],
            [u'h', u'HH '],
            [u'm', u'M '],
            [u'v', u'V '],
            [u'n(?!(h|g))', u'N '],
            [u'l', u'L '],
            [u'x', u'S '],
            [u'p(?!h)', u'P '],
            [u's', u'SH ']
        ]

        # Bán nguyên âm 2
        self.re_halfvowel = [
            [u'u(?=(yê|ya))', u'W '],
            [u'o(?=(a|ă|e))', u'W ']
        ]

        # Nguyên âm 84
        self.re_vowel = [
            [u'ia|ya|iê|yê', u'IYE '],
            [u'ía|ýa|iế|yế', u'IYE1 '],
            [u'ìa|ỳa|iề|yề', u'IYE2 '],
            [u'ỉa|ỷa|iể|yể', u'IYE3 '],
            [u'ĩa|ỹa|iễ|yễ', u'IYE4 '],
            [u'ịa|ỵa|iệ|yệ', u'IYE5 '],

            [u'uô|ua', u'UX '],
            [u'uố|úa', u'UX1 '],
            [u'uồ|ùa', u'UX2 '],
            [u'uổ|ủa', u'UX3 '],
            [u'uỗ|ũa', u'UX4 '],
            [u'uộ|ụa', u'UX5 '],

            [u'ươ|ưa', u'IXO '],
            [u'ướ|ứa', u'IXO1 '],
            [u'ườ|ừa', u'IXO2 '],
            [u'ưở|ửa', u'IXO3 '],
            [u'ưỡ|ữa', u'IXO4 '],
            [u'ượ|ựa', u'IXO5 '],

            [u'i|y', u'IY '],
            [u'í|ý', u'IY1 '],
            [u'ì|ỳ', u'IY2 '],
            [u'ỉ|ỷ', u'IY3 '],
            [u'ĩ|ỹ', u'IY4 '],
            [u'ị|ỵ', u'IY5 '],

            [u'e', u'EH '],
            [u'é', u'EH1 '],
            [u'è', u'EH2 '],
            [u'ẻ', u'EH3 '],
            [u'ẽ', u'EH4 '],
            [u'ẹ', u'EH5 '],

            [u'ê', u'EY '],
            [u'ế', u'EY1 '],
            [u'ề', u'EY2 '],
            [u'ể', u'EY3 '],
            [u'ễ', u'EY4 '],
            [u'ệ', u'EY5 '],

            [u'a', u'AA '],
            [u'á', u'AA1 '],
            [u'à', u'AA2 '],
            [u'ả', u'AA3 '],
            [u'ã', u'AA4 '],
            [u'ạ', u'AA5 '],

            [u'ă', u'AA: '],
            [u'ắ', u'AA:1 '],
            [u'ằ', u'AA:2 '],
            [u'ẳ', u'AA:3 '],
            [u'ẵ', u'AA:4 '],
            [u'ặ', u'AA:5 '],

            [u'â', u'AX '],
            [u'ấ', u'AX1 '],
            [u'ầ', u'AX2 '],
            [u'ẩ', u'AX3 '],
            [u'ẫ', u'AX4 '],
            [u'ậ', u'AX5 '],

            [u'o', u'AO '],
            [u'ó', u'AO1 '],
            [u'ò', u'AO2 '],
            [u'ỏ', u'AO3 '],
            [u'õ', u'AO4 '],
            [u'ọ', u'AO5 '],

            [u'ô', u'OW '],
            [u'ố', u'OW1 '],
            [u'ồ', u'OW2 '],
            [u'ổ', u'OW3 '],
            [u'ỗ', u'OW4 '],
            [u'ộ', u'OW5 '],

            [u'ơ', u'AX: '],
            [u'ớ', u'AX:1 '],
            [u'ờ', u'AX:2 '],
            [u'ở', u'AX:3 '],
            [u'ỡ', u'AX:4 '],
            [u'ợ', u'AX:5 '],

            [u'u', u'UW '],
            [u'ú', u'UW1 '],
            [u'ù', u'UW2 '],
            [u'ủ', u'UW3 '],
            [u'ũ', u'UW4 '],
            [u'ụ', u'UW5 '],

            [u'ư', u'IX '],
            [u'ứ', u'IX1 '],
            [u'ừ', u'IX2 '],
            [u'ử', u'IX3 '],
            [u'ữ', u'IX4 '],
            [u'ự', u'IX5 ']
        ]
        
    def clean(self):
        self.str = self.str.lower()
        # self.tone = self.definite_tone()
        # self.str = self.clear_tone()

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
            self.str = self.str + '-'
        return self.str

if __name__ == '__main__':
    text = u"Hôm qua em đến trường"
    res = text.split(" ")
    for char in res:
        test = Text2ARPAbet(str=char)
        print(test.convert())