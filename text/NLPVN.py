#!/usr/bin/python
# -*- coding: utf-8 -*-
from underthesea import word_sent

__specChar__ = {u'@': u'a còng', u'^': u'mũ', u'$': u'đô la', u'%': u'phần trăm', u'*' : u'sao', u'+': u'cộng', u'>': u'dấu lớn', u'<': u'dấu bé', u'/': u'phần', u'=': u'bằng'}
__number__ = {0: u'không', 1: u'một', 2: u'hai', 3: u'ba', 4: u'bốn', 5: u'năm', 6: u'sáu', 7: u'bảy', 8: u'tám', 9: u'chín', 10: u'mười'}
__currency__ = {u'VND': u'việt nam đồng', u'USD': 'đô la mỹ'}
__doluong__ = {u'km': u'ki lô mét', u'cm': u'xen ti mét', u'dm': u'đề xi mét', u'mm': u'mi li mét', u'nm':u'na nô mét'}
__cannang__ = {u'kg': u'ki lô gam', u'g': 'gờ ram'}

specChar = u'@^$%*+-><='

class nlp_vn(object):
    def __init__(self, text=None):
        self.str = text
        self.raw = text
        self.word_sent = None
        self.result = []

    def split_word_sent(self):
        self.word_sent = word_sent(self.str)
        return self.word_sent
    
    def convert(self):
        for char in self.word_sent:
            char = self.specChar(char)
            char = self.currency(char)
            char = self.doluong(char)
            char = self.cannang(char)
            char = self.processNum(char)
            self.result.append(char)
        return self.result

    def clean(self):
        self.str = self.str.strip()
        return self.str

    def join_str(self, list_str):
        return " ".join(list_str)

    def specChar(self, text):
        try:
            if len(text) == 1:
                return __specChar__[text]
            else:
                for char in specChar:
                    if char in text:
                        text = text.replace(char,u" " + __specChar__[char] + u" ")
                result = []
                for char in text.split():
                    char = self.currency(char)
                    char = self.doluong(char)
                    char = self.cannang(char)
                    char = self.processNum(char)
                    result.append(char)
                return self.join_str(result)
        except:
            return text

    def currency(self, text):
        try:
            return __currency__[text]
        except:
            return text

    def doluong(self, text):
        try:
            return __doluong__[text]
        except:
            return text  

    def cannang(self, text):
        try:
            return __cannang__[text]
        except:
            return text

    def processNum(self, text):
        try:
            if len(text) > 1:
                if u'.' in text:
                    res = text.split(u'.')
                    return self.num_to_text(u''.join(res), 0)

                output = u''
                if u',' in text:
                    res = text.split(u',')
                    if len(res) > 1:
                        count = 0
                        for map in res:
                            count +=1
                            if count <= len(res) - 1:
                                output += self.num_to_text(map, 0) + u" phẩy "
                            else: output += self.num_to_text(map, 0)
                        return output
                    else: return self.num_to_text(res[0], 0)

                if u'/' in text:
                    res = text.split(u'/')
                    if len(res) == 3:
                        if int(res[0]) <=31 and int(res[1]) <=12:
                            return u"ngày " + self.num_to_text(res[0], 0) + u" tháng " + self.num_to_text(res[1], 0) + u" năm " + self.num_to_text(res[2], 0)
                    else:
                        count = 0
                        for map in res:
                            count +=1
                            if count <= len(res) - 1:
                                output += self.num_to_text(map, 0) + u" phần "
                            else: output += self.num_to_text(map, 0)
                        return output

            if str(text).isdigit():
                return self.num_to_text(text, 0)
            return text
        except:
            return text

    def num_to_text(self, text, flag):
        try:
            num = int(text)
            if num <= 10: 
                if flag==0:
                    return __number__[num]
                return u"linh " + __number__[num]
            if num//1000000000 > 0:
                if num%1000000000 == 0: 
                    return self.num_to_text(num//1000000000, 0) + u" tỷ"
                if num%1000000000 != 0: 
                    return self.num_to_text(num//1000000000, 0) + u" tỷ " + self.num_to_text(num%1000000000, 1)
            if num//1000000 > 0:
                if num%1000000 == 0: 
                    return self.num_to_text(num//1000000, 0) + u" triệu"
                if num%1000000 != 0: 
                    return self.num_to_text(num//1000000, 0) + u" triệu " + self.num_to_text(num%1000000, 2)
            else:
                if flag==1:
                    return self.num_to_text(num//1000000, 0) + u" triệu " + self.num_to_text(num%1000000, 2)
            if num//1000 > 0:
                if num%1000 == 0: 
                    return self.num_to_text(num//1000, 0) + u" nghìn"
                if num%1000 != 0: 
                    return self.num_to_text(num//1000, 0) + u" nghìn " + self.num_to_text(num%1000, 3)
            else:
                if flag==2:
                    return self.num_to_text(num//1000, 0) + u" nghìn " + self.num_to_text(num%1000, 3)
            if num//100 > 0:
                if num%100 == 0: 
                    return self.num_to_text(num//100, 0) + u" trăm"
                if num%100 != 0: 
                    return self.num_to_text(num//100, 0) + u" trăm " + self.num_to_text(num%100, 4)
            else:
                if flag==3:
                    return self.num_to_text(num//100, 0) + u" trăm " + self.num_to_text(num%100, 4)
            if num//10 > 0:
                if num >= 20:
                    if num%10 != 0:
                        if num%10 == 1:
                            return self.num_to_text(num//10, 0) + u" mươi mốt"
                        if num%10 == 5:
                            return self.num_to_text(num//10, 0) + u" mươi lăm"
                        return self.num_to_text(num//10, 0) + u" mươi " + self.num_to_text(num%10, 0)
                    else:
                        return self.num_to_text(num//10, 0) + u" mươi"
                else:
                    if num == 15: 
                        return u"mười lăm"
                    return u"mười " + self.num_to_text(num%10, 0)
        except:
            return text

if __name__ == "__main__":
    text = u"12/8 trường đại học bách khoa"
    nlp = nlp_vn(text)
    nlp.split_word_sent()
    nlp.convert()
    print(nlp.join_str(nlp.result))
    


    

    


    



    

