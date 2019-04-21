import sys
import re
import pandas as pd
import numpy as np
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize
from collections import Counter
import emoji

# TODO adapt the function below to the project context
def countWordsOnReviews(df):
	wordCounter = Counter()
	for review in df['Review']:
		for word in word_tokenize(review):
			wordCounter[word] +=1
	
	return wordCounter

# TODO adapt the function below to the project context
def cleanseData(df, threshold, vocab_file_out, vocab):
	print('Vocabulary size: ' + str(len(vocab)))
	f = open(vocab_file_out, 'w' )
	f.write(repr(vocab))
	f.close()
	new_df_review = []
	for review in df['Review']:
		new_review = []
		for word in word_tokenize(review):
			if word in vocab:
				new_review.append(word)
		review = ' '.join(new_review)
		new_df_review.append(review)
	new_df_review = pd.DataFrame(new_df_review, columns=['Review'])
	df.drop(['Review'], 1, inplace=True)
	df.reset_index(inplace=True, drop=True)   
	df = pd.concat([df, new_df_review], axis=1)
	return df,vocab

def cleanseData_below_threshold(df, threshold, vocab_file_out):
	counter = countWordsOnReviews(df)	
	vocab = {x : counter[x] for x in counter if counter[x] >= threshold}
	return cleanseData(df, threshold, vocab_file_out, vocab)

def preprocessDataset(file_name):
	df = pd.read_csv(file_name, sep="\t", usecols = [0, 1, 2, 3, 4])
	
	frames = []
	found = {}
	
	#old_frame = None
	
	for i, row in df.iterrows():
		text = row["full_text"]
		if text != text: # test if NaN
			continue
		
		if not text in found:
			print("{} \n {}".format(i, text))
			found[text] = i
			text = emoji.demojize(text) # TODO - not working
			text = re.sub("^RT", "", text)
			text = preprocess(word_tokenize(text))
			frames.append(text)
		"""else:
			print(found[text])
			input()"""
			
	df = pd.DataFrame(frames)
	print(df.shape)	

	df.to_csv('tweets_without_clean.csv')

def preprocess(words):
	new_words = []
	lemmatizer = WordNetLemmatizer()   
	for word in words:
		
		# Remove from array punctuation words
		temp = re.sub(r'[^\w\s]', '', word)
		if temp == '':
			continue

		# To lowercase
		temp = temp.lower()

		# Remove line breaks
		temp = temp.replace('\n', ' ').replace('\r', '').replace('\t', ' ')

		# Remove numbers
		if temp.isdigit():
			continue

		# Remove stop words
		"""if temp in selected_stopwords:
			continue"""
			
		# Lemmatization
		#temp = lemmatizer.lemmatize(temp, get_wordnet_pos(temp)) # complete lemmatization but slow
		temp = lemmatizer.lemmatize(temp) # fast lemmatization but not perfect

		new_words.append(temp)
		# Return a single string with preprocessed text
	return ' '.join(str(x) for x in new_words)
	
if __name__ == '__main__':
	preprocessDataset(sys.argv[1])
