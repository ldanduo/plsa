#!/usr/bin/python
#-*-coding:utf-8

import sys
import os
import pdb

def main():
    #pdb.set_trace()
    doc_id = 0
    file_list = os.listdir("./data")
    for item in file_list:
        file_name = item.split(".")[0]
        file_path = "./data/" + item
        file_class = ""
        if item.find("auto") != -1:
            file_class = "auto"
        if item.find("sport") != -1:
            file_class = "sport"
        if item.find("business") != -1:
            file_class = "business"
        doc_id += 1
        output = ""
        infp = file(file_path)
        for line in infp:
            line = line.strip() + " "
            output += line
        output = output.rstrip()
        print "%d\t%s\t%s\t%s" % (doc_id,file_name,file_class,output)
        infp.close()

if __name__ == '__main__':
    main()
