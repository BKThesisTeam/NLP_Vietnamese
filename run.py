#!/usr/bin/python
# -*- coding: utf8 -*-
import io
import re
from text.NLPVN import nlp_vn as nlp
from text.Text2ARPAbet import Text2ARPAbet as t2a


def run(input, output):
    f_out = io.open(output, 'w', encoding="utf-8")
    f_in = io.open(input, 'r', encoding="utf-8")
    result = []
    for line in f_in.readlines():
        # Tiền xử lý
        words = nlp(line)
        words.clean()
        words.split_word_sent()
        words.convert()
        new_str = words.join_str(words.result)
        f_out.write(u"TEXT: "+new_str+u"\n")

        # Text to ARPABET
        list_str = re.split(u"\s+", new_str)
        for word in list_str:
            arpabet = t2a(word)
            res = arpabet.convert()
            result.append(res)
        out = " ".join(result)
        f_out.write(u"ARPABET: "+out+u"\n")
        result = []
    
    f_in.close()
    f_out.close()
        
if __name__ == "__main__":
    run("input.txt", "output.txt")

    