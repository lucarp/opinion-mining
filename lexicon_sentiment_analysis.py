import numpy as np
import pandas as pd
import sys
import re
from nltk.tokenize import word_tokenize 

def texts_to_sentiment(texts_file, sentiment_dict_file, emoji_sentiment_dict_file, text_column = 0):
	texts_df = pd.read_csv(texts_file, header=0, index_col=0)
	sentiment_df = pd.read_csv(sentiment_dict_file, index_col=0)
	emoji_sentiment_df = pd.read_csv(emoji_sentiment_dict_file, index_col=0)
	
	doc_sentiment_matrix = []
	dict_term_sentiment_matrix = {}
	dict_emoji_sentiment_matrix = {}

	print("make term dictionary...")
	# TERM DICTIONARY - Iterate through all sentiment words in the dictionary	
	for _, sent_vec in sentiment_df.iterrows():
		sent_word = re.sub("#.*", "", sent_vec[0])
		pos = float(sent_vec[1])
		neg = float(sent_vec[2])
		
		if sent_word in dict_term_sentiment_matrix:
			pos = max(pos, dict_term_sentiment_matrix[sent_word][0])
			neg = max(neg, dict_term_sentiment_matrix[sent_word][1])
		
		neu = 1 if pos == 0 and neg == 0 else 0

		# TODO - save this dict to avoid to compute it every time
		dict_term_sentiment_matrix[sent_word] = (pos, neg, neu)
		
	print("make emoji dictionary...")
	# EMOJI DICTIONARY - Iterate through all sentiment emojis in the dictionary
	for _, sent_vec in emoji_sentiment_df.iterrows():
		sent_emoji = sent_vec[6]
		sent_emoji = sent_emoji.lower()
		sent_emoji = re.sub(" ","_",sent_emoji)
		sent_emoji = sent_emoji
		
		total = sent_vec[5]+sent_vec[3]+sent_vec[4]
		pos = float(sent_vec[5]/total)
		neg = float(sent_vec[3]/total)
		neu = float(sent_vec[4]/total)

		# TODO - save this dict to avoid to compute it every time
		dict_emoji_sentiment_matrix[sent_emoji] = (pos, neg, neu)		
	
	print("iterate through all the texts...")
	# Iterate through all the texts
	found = {}
	for _, row in texts_df.iterrows():
		temp = [0.,0.,0.]
		text = row[text_column]
		for word in word_tokenize(text):
			# Search in TERM dictionary
			if word in dict_term_sentiment_matrix:
				sent_vec = dict_term_sentiment_matrix[word]
				temp = np.add(temp, sent_vec)
			# Search in EMOJI dictionary				
			if word in dict_emoji_sentiment_matrix:
				sent_vec = dict_emoji_sentiment_matrix[word]
				temp = np.add(temp, sent_vec)
			if word in dict_term_sentiment_matrix and word in dict_emoji_sentiment_matrix:
				temp /= 2
			if word in dict_term_sentiment_matrix or word in dict_emoji_sentiment_matrix:
				found[word] = 1
				
		doc_sentiment_matrix.append(temp)	
	
	print(len(found))
	
	return doc_sentiment_matrix
		
if __name__ == "__main__":
	#text_column = 4
	doc_sentiment_matrix = texts_to_sentiment(sys.argv[1], sys.argv[2], sys.argv[3]) #, text_column)
	pd.DataFrame(doc_sentiment_matrix).to_csv(sys.argv[1]+"_doc_sentiment.csv")
	doc_label = []
	doc_label_neu = []
	for row in doc_sentiment_matrix:
		label = 1. if row[0] >= row[1] else 0.		
		doc_label.append(label)
		label = 1. if row[0] > row[1] else 0. if row[0] > row[1] else 0.5
		doc_label_neu.append(label)
	pd.DataFrame(doc_label).to_csv(sys.argv[1]+"_lexicon_sentiment_pos_neg.csv")
	pd.DataFrame(doc_label_neu).to_csv(sys.argv[1]+"_lexicon_sentiment.csv")	
