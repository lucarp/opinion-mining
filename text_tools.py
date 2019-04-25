import sys
import numpy as np
from scipy import io
from scipy import sparse
import pandas as pd
import heapq
import gensim



def get_most_frequent_words(bow_mat, inds, vocab, n = 100):
	mat_sum = bow_mat[inds].sum(axis = 0)
	mat_sum = np.reshape(mat_sum, (mat_sum.shape[1], 1))

	idx = heapq.nlargest(n, range(len(mat_sum)), mat_sum.take)
	
	words = np.array(vocab.iloc[idx])
	words = np.reshape(words, (words.shape[0], ))
	
	return words

def compare_with_lexicon_positive(bow_mat, labels, vocab, lex_labels):
	model = gensim.models.doc2vec.Doc2Vec.load("doc2Vec.model")
	
	lab_values = [1, 2]
	for lab in lab_values:
		inds = np.where(labels == lab)[0]
		words = get_most_frequent_words(bow_mat, inds, vocab)

		# Get the most frequent words of the positive group lexicon-based
		lex_inds = np.where(lex_labels == 1)[0]
		lexicon_words = get_most_frequent_words(bow_mat, lex_inds, vocab)
		
		sim = model.n_similarity(words, lexicon_words)
		print(lab)
		print(sim)
	
if __name__ == "__main__":
	bow_mat = io.loadmat(sys.argv[1])['X']
	labels = pd.read_csv(sys.argv[2], index_col = 0)
	vocab = pd.read_csv(sys.argv[3], index_col = 0)
	lexicon = pd.read_csv(sys.argv[4], index_col = 0)
	
	print(bow_mat.shape)
	print(labels.shape)
	print(vocab.shape)

	compare_with_lexicon_positive(bow_mat, labels, vocab, lexicon)
	
	"""inds_1 = np.where(labels == 1)[0]
	words = get_most_frequent_words(bow_mat, inds_1, vocab)
	
	inds_2 = np.where(labels == 2)[0]
	words = get_most_frequent_words(bow_mat, inds_2, vocab)"""
