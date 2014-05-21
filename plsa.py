import os
import sys
import math
import random

def cos_sim(p,q):
	sum0 = sum(map(lambda x:x*x,p))
	sum1 = sum(map(lambda x:x*x,q))
	sum2 = sum(map(lambda x:x[0]*x[1],zip(p,q)))

	return sum2 / (sum0**0.5) / (sum1**0.5)

def _rand_mat(sizex, sizey):
	ret = []
	for i in xrange(sizex):
		ret.append([])
		for k in xrange(sizey):
			ret[-1].append(random.random())
		norm = sum(ret[-1])
		for j in xrange(sizey):
			ret[-1][j] /= norm
	return ret

class Plsa:

	def __init__(self,corpus,doc_count,word_count,tpc_count,max_iters):
		self.corpus = corpus
		self.doc_count = doc_count
		self.word_count = word_count
		self.tpc_count = tpc_count
		self.max_iters = max_iters
	
		self.log_likelihood = 0.0
		self.pre_zw = _rand_mat(self.tpc_count, self.word_count)
		self.now_zw = _rand_mat(self.tpc_count, self.word_count)
		self.pre_dz = _rand_mat(self.doc_count, self.tpc_count)
		self.now_dz = _rand_mat(self.doc_count, self.tpc_count)
	
		self.corpus_list = []
		self.setup()
	
	def setup(self):
		ifp = file(self.corpus)
		for line in ifp:
			tmp_dict = {}
			line = line.strip()
			if not line:continue
			array = line.split("\t")
			doc_id = int(array[0])
			word_list = [int(item) for item in array[1].split(" ")]
			for word in word_list:
				if not tmp_dict.has_key(word):
					tmp_dict[word] = 0
				tmp_dict[word] += 1
			self.corpus_list.append(tmp_dict)
		ifp.close()
	
	
	def train(self):
		iters_count = 0
		log_likelihood = 0.0
		for i in xrange(self.max_iters):
			print "[------------iters %d...-----------------]" % (iters_count)
			'''E-setp:'''
			print "E-setp..."
			iters_count += 1
			tpc_buf = [0.0] * self.tpc_count
			for d in xrange(self.doc_count):
				print "[docid = %d]" % (d)
				for w in xrange(self.word_count):
					denom = 0.0
					for z in xrange(self.tpc_count):
						numer = self.pre_zw[z][w] * self.pre_dz[d][z]
						tpc_buf[z] = numer
						denom += numer
	
					for z in xrange(self.tpc_count):
						tpc_buf[z] /= denom
			if self.corpus_list[d].has_key(w):
				tpc_buf[z] *= self.corpus_list[d][w]
				self.now_dz[d][z] += tpc_buf[z]
				self.now_zw[z][w] += tpc_buf[z]
	
			'''M-step'''
			print "M-step..."
			for z in xrange(self.tpc_count):
				denom = 0.0
				for w in xrange(self.word_count):
					denom += self.now_zw[z][w]
				for w in xrange(self.word_count):
					self.now_zw[z][w] /= denom
	
			for d in xrange(self.doc_count):
				for z in xrange(self.tpc_count):
					self.now_dz[d][z] /= sum(self.corpus_list[d].values())
	
			'''check convergence'''
			print "check convergence..."
			for d in xrange(self.doc_count):
				for w in xrange(self.word_count):
					llf_temp = 0.0
					for z in xrange(self.tpc_count):
						llf_temp += self.now_dz[d][z] * self.now_zw[z][w]
					if llf_temp > 0:
						if self.corpus_list[d].has_key(w):
							log_likelihood += self.corpus_list[d][w] * math.log(llf_temp)
			if abs(log_likelihood - self.log_likelihood) < 0.01:
				break
			else:
				self.log_likelihood = log_likelihood
	
	
		self.save_model()
	def save_model(self):
		ofp = file("model.doc","w")
		for d in xrange(self.doc_count):
			tmp = ""
			for z in xrange(self.tpc_count):
				tmp += ("%lf ") % (self.now_dz[d][z])
			print >> ofp,tmp.strip()
		ofp.close()
	
		ofp = file("model.tpc","w")
		for z in xrange(self.tpc_count):
			tmp = ""
			for w in xrange(self.word_count):
				tmp += ("%lf ") % (self.now_zw[z][w])
			print >> ofp,tmp.strip()
		ofp.close()
	
