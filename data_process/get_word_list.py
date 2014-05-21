#!/usr/bin/python
#-*-coding:utf-8

import sys
import pdb

sw_dict = {}
def load_dict(sw_file):
    infp = file(sw_file)
    for line in infp:
        line = line.strip()
        sw_dict[line] = 1
    infp.close()


def main():
    load_dict("./stop_words.txt_utf8")

    infp = file("./word.dat")

    for line in infp:
        line = line.strip()
        if not line:continue
        array = line.split(" ")
        if len(array) != 2:continue
        word = array[0]
        word_unicode = word.decode("utf-8","ignore")
        if len(word_unicode) == 1:
            continue
        if word in sw_dict:
            continue
        if not word:continue
        print line

    infp.close()
if __name__ == "__main__":
    main()
