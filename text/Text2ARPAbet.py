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
            [u'uô|ua', u'UX '],
            [u'ươ|ưa', u'IXO '],
            [u'e', u'EH '],
            [u'ê', u'EY '],
            [u'a', u'AA '],
            [u'ă', u'AA: '],
            [u'â', u'AX '],
            [u'o', u'AO '],
            [u'ô', u'OW '],
            [u'ơ', u'AX: '],
            [u'u', u'UW '],
            [u'ư', u'IX '],
            [u'i|y', u'IY ']
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
            return '' # không dấu
        except:
            return -1 # error

    def clear_tone(self):
        map = {ord(c): ord(t) for c, t in zip(input, output)}
        return self.str.translate(map)

    
    def num_there(self, data):
        return any(i.isdigit() for i in data)

    def convert(self):
        self.clean()

        for map in self.re_consonant:
            self.str = re.sub(re.compile(map[0], re.UNICODE), map[1], self.str)

        for map in self.re_halfvowel:
            self.str = re.sub(re.compile(map[0], re.UNICODE), map[1], self.str)

        for map in self.re_vowel:
            v_tone = map[1].strip() + str(self.tone) + " "
            self.str = re.sub(re.compile(map[0], re.UNICODE), v_tone, self.str)

        if self.str != u'' or self.str != u' ':
            self.str = self.str

        list_v = re.split(u'\s+', self.str)
        list_v.pop()

        count = 0;
        for child in list_v:
            if self.num_there(child):
                count+=1
        if count >= 2:
            last_v = list_v.pop()
            last_v = last_v[0:len(last_v)-1]
            list_v.append(last_v)

        self.str = " ".join(list_v)
        return self.str + "."

if __name__ == '__main__':
    text = u"Hôm qua em đến trường"
    res = text.split(" ")
    for char in res:
        test = Text2ARPAbet(str=char)
        print(test.convert())