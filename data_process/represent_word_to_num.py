#!/usr/bin/python
#-*-coding:utf8

import os
import sys
import pdb

word_dic = {}
def load_word_dic(word_file):
    word_id = 1
    ifp = file(word_file)
    for line in ifp:
        line = line.strip()
        if not line:continue
        array = line.split(" ")
        if len(array) != 2:continue
        word = array[0]
        if not word_dic.has_key(word):
            word_dic[word] = word_id
        word_id += 1
    ifp.close()

def main():
    load_word_dic("word_list.dat")
    ifp = file(sys.argv[1])
    for line in ifp:
        line = line.strip()
        array = line.split("\t")
        if len(array) != 2:continue
        docid = array[0]
        word_list = array[1].strip().split(" ")
        word_num = []
        for item in word_list:
            if item in word_dic:
                word_num.append(str(word_dic[item]))
        if len(word_num) == 0:continue
        print "%s\t%s" % (docid," ".join(word_num))


    ifp.close()
if __name__ == '__main__':
    main()
