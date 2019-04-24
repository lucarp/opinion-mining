import sys
import numpy as np
from scipy import io
from scipy import sparse
import pandas as pd
import heapq



def get_most_frequent_words(bow_mat, inds, vocab_csv, n = 20):
	mat_sum = sparse.csr_matrix((1, bow_mat.shape[1]))
	for i in inds:
		mat_sum += bow_mat[i]
	
	mat_sum = np.reshape(mat_sum.todense(), (mat_sum.shape[1], 1))
	idx = heapq.nlargest(n, range(len(mat_sum)), mat_sum.take)
	
	words = np.array(vocab_csv.iloc[idx])
	
	return words
	
	
if __name__ == "__main__":
	bow_mat = io.loadmat(sys.argv[1])['X']
	labels = pd.read_csv(sys.argv[2], index_col = 0)
	vocab = pd.read_csv(sys.argv[3], index_col = 0)
	
	print(bow_mat.shape)
	print(labels.shape)
	print(vocab.shape)
		
	inds_1 = np.where(labels == 1)[0]
	words = get_most_frequent_words(bow_mat, inds_1, vocab)
	print(words)
	
	inds_2 = np.where(labels == 2)[0]
	get_most_frequent_words(bow_mat, inds_2, vocab)
	print(words)	
	
