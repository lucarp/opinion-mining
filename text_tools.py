import sys
import numpy as np
from scipy import io
from scipy import sparse
import pandas as pd
import heapq
import gensim
from lexicon_sentiment_analysis import make_dict_term_sentiment_matrix, make_dict_emoji_sentiment_matrix




def get_most_positive_words(vocab_file, sentiment_dict_file, emoji_sentiment_dict_file, n = 100):	
	dict_term_sentiment_matrix = make_dict_term_sentiment_matrix(sentiment_dict_file)
	dict_emoji_sentiment_matrix = make_dict_emoji_sentiment_matrix(emoji_sentiment_dict_file)	
	vocab_df = pd.read_csv(vocab_file, index_col = 0)
	
	term_sentiment_matrix = []
	
	for _, word in vocab_df.iterrows():
		word = word[0]
		sent_pos = 0
		# Search in TERM dictionary
		if word in dict_term_sentiment_matrix:
			sent_pos += dict_term_sentiment_matrix[word][0]
		# Search in EMOJI dictionary				
		if word in dict_emoji_sentiment_matrix:
			sent_pos += dict_emoji_sentiment_matrix[word][0]
		if word in dict_term_sentiment_matrix and word in dict_emoji_sentiment_matrix:
			sent_pos /= 2
		print(word)
		term_sentiment_matrix.append(sent_pos)
		
	term_sentiment_matrix = np.matrix(term_sentiment_matrix)
	term_sentiment_matrix = np.reshape(term_sentiment_matrix, (term_sentiment_matrix.shape[1], 1))
	idx = heapq.nlargest(n, range(len(term_sentiment_matrix)), term_sentiment_matrix.take)
	
	best_words = vocab_df.iloc[idx]
	best_words.to_csv("dataset/tweets_clean10.csv_best_words")
	
def get_most_frequent_words(bow_mat, inds, vocab, n = 100):
	mat_sum = bow_mat[inds].sum(axis = 0)
	mat_sum = np.reshape(mat_sum, (mat_sum.shape[1], 1))

	idx = heapq.nlargest(n, range(len(mat_sum)), mat_sum.take)
	
	words = np.array(vocab.iloc[idx])
	words = np.reshape(words, (words.shape[0], ))
	
	return words

def similarity_set_words(set1, set2):
	model = gensim.models.doc2vec.Doc2Vec.load("doc2Vec.model")
	return model.n_similarity(set2, set1)

def compare_with_lexicon_positive(bow_mat, labels, vocab, lex_labels):	
	lab_values = [1, 2]
	for lab in lab_values:
		inds = np.where(labels == lab)[0]
		words = get_most_frequent_words(bow_mat, inds, vocab)

		# Get the most frequent words of the positive group lexicon-based
		lex_inds = np.where(lex_labels == 1)[0]
		lexicon_words = get_most_frequent_words(bow_mat, lex_inds, vocab)
		
		sim = similarity_set_words(words, lexicon_words)
		print(lab)
		print(sim)

def compare_with_best_words(bow_mat, labels, vocab, best_words):
	lab_values = [1, 2]
	for lab in lab_values:
		inds = np.where(labels == lab)[0]
		words = get_most_frequent_words(bow_mat, inds, vocab)
		
		sim = similarity_set_words(words, best_words)
		print(lab)
		print(sim)
	
if __name__ == "__main__":
	bow_mat = io.loadmat(sys.argv[1])['X']
	labels = pd.read_csv(sys.argv[2], index_col = 0)
	vocab = pd.read_csv(sys.argv[3], index_col = 0)

	print(bow_mat.shape)
	print(labels.shape)
	print(vocab.shape)	
	
	"""lexicon = pd.read_csv(sys.argv[4], index_col = 0)

	compare_with_lexicon_positive(bow_mat, labels, vocab, lexicon)"""
	
	"""inds_1 = np.where(labels == 1)[0]
	words = get_most_frequent_words(bow_mat, inds_1, vocab)
	print(words)
	
	inds_2 = np.where(labels == 2)[0]
	words = get_most_frequent_words(bow_mat, inds_2, vocab)
	print(words)"""
	
	#get_most_positive_words(sys.argv[1], sys.argv[2], sys.argv[3])
	
	best_words = pd.read_csv(sys.argv[4], index_col = 0)
	compare_with_best_words()
