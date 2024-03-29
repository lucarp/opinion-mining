import sys
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import emoji

from nltk.corpus import wordnet



def countWordsOnReviews(df):
	wordCounter = Counter()
	for i, row in df.iterrows():
		review = row["0"]
		for word in word_tokenize(review):
			wordCounter[word] +=1

	return wordCounter

def cleanseData(df, threshold, vocab_file_out, vocab):
	print('Vocabulary size: ' + str(len(vocab)))
	f = open(vocab_file_out, 'w' )
	f.write(repr(vocab))
	f.close()
	new_df_review = []
	for i, row in df.iterrows():
		review = row["0"]
		new_review = []
		for word in word_tokenize(review):
			if word in vocab:
				new_review.append(word)
		review = ' '.join(new_review)
		if text != text or text == '':
				continue
		new_df_review.append(review)
		
	df = pd.DataFrame(new_df_review, columns=['Review'])	
	return df,vocab

def cleanseData_below_threshold(df, threshold, vocab_file_out):
	counter = countWordsOnReviews(df)
	vocab = {x : counter[x] for x in counter if counter[x] >= threshold}
	return cleanseData(df, threshold, vocab_file_out, vocab)
	
def cleanAndSaveData(fileNameIn, fileNameOut, threshold, vocab_file_out):
    df = pd.read_csv(fileNameIn, header=0, index_col=0)
    df,vocab = cleanseData_below_threshold(df, threshold, vocab_file_out)
    df.to_csv(fileNameOut)

def preprocessDataset(file_name):
	df = pd.read_csv(file_name, sep="\t", usecols = [0, 1, 2, 3, 4])
	
	frames = []
	found = {}
	found_full = {}
	
	for i, row in df.iterrows():
		text = row["full_text"]
		if text != text: # test if NaN
			continue

		if not text in found_full:
			found_full[text] = i
			text = emoji.demojize(text)
			text = re.sub("^RT", "", text)
			text = re.sub("http.*", "", text)			
			text = preprocess(word_tokenize(text))
			
			if text != text or text == '':
				continue
		
			if not text in found:		
				print(i)	
				#print(text)	
				found[text] = i
				frames.append(text)
			
	df = pd.DataFrame(frames)
	print(df.shape)	

	df.to_csv('tweets_no_clean.csv')

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
		if temp in stopwords.words('english'):
			continue
			
		# Lemmatization
		#temp = lemmatizer.lemmatize(temp, get_wordnet_pos(temp)) # complete lemmatization but slow
		temp = lemmatizer.lemmatize(temp) # fast lemmatization but not perfect

		new_words.append(temp)
		# Return a single string with preprocessed text
	return ' '.join(str(x) for x in new_words)
	
if __name__ == '__main__':
	preprocessDataset(sys.argv[1])

	#cleanAndSaveData(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])	
