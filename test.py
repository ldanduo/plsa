from plsa import *

def main():
	'''
	Usage program train.dat doc_count words_count topic_count max_iters
	'''
	p = Plsa("../data_process/train.dat",3066,25244,10,1)
	p.train()
if __name__ == '__main__':
	main()
