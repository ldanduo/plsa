import os
import sys
import math as m

doc_size = 0
term_df_dict = {}
term_tf_dict = {}

def load_file(infile,outfile):
	global doc_size
	infp = open(infile,'r')
	for line in infp:
		doc_size += 1
		term_list = line.rstrip().split("\t")[1].strip().split(' ')
		term_dict = {}
		for term in term_list:
			if term in term_dict:
				term_dict[term] += 1
			else:
				term_dict[term] = 1

		for term in term_dict.items():
			if term[0] in term_df_dict:
				term_df_dict[term[0]] += 1
			else:
				term_df_dict[term[0]] = 1
			if term[0] in term_tf_dict:
				term_tf_dict[term[0]] += term[1]
			else:
				term_tf_dict[term[0]] = term[1]
	infp.close()

	outfp = open(outfile,'w')
	for term in term_tf_dict.items():
		feature = term[0]
		tf = term[1]
		df = term_df_dict[feature]
		idf = m.log(doc_size/float(df))
		mtfidf = (tf * idf)/df
		outfp.write('%s\t%d\t%d\t%f\t%f\n'%(feature,tf,df,idf,mtfidf))
	outfp.close()

if __name__ == '__main__':
	load_file(sys.argv[1],sys.argv[2])
