import sys
import scipy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer



# Process text file and return docs and meta_data
def file_to_data(file_name):
	df = pd.read_csv(file_name, header=0, index_col=0)	
	docs = df['Review']
	
	# TODO - Manage meta-data (is it useful?)
	meta_data = None
	
	return docs, meta_data

# TODO - adapt the function below to the project context
# Returns dataFrame from docs and meta_data
def data_to_dataFrame(docs, meta_data, vectorizer):
	X = vectorizer.fit_transform(docs) # non sparse data
	df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
	
	# TODO - Manage meta-data (is it useful?)
	if meta_data is not None:
		#df_meta = pd.DataFrame(meta_data, columns=['RATING', 'AUTHOR', 'DOC_ID'])
		df = pd.concat([df, df_meta], axis=1)
		
	return df, X

# Whole pipeline text to dataFrame
def file_to_dataFrame(file_name, vectorizer):
	docs, meta_data = file_to_data(file_name)
	df, X = data_to_dataFrame(docs, meta_data, vectorizer)
	return df, X
	
# Return basic bag of words
def file_to_bow(file_name):
	vectorizer = CountVectorizer()
	df, X = file_to_dataFrame(file_name, vectorizer)
	return df, X
	
# Return tf-idf bag of words
def file_to_tfidf(file_name):
	vectorizer = TfidfVectorizer(norm=None, sublinear_tf=True)
	df, X = file_to_dataFrame(file_name, vectorizer)
	return df, X	
	
# Return tf-idf with l2 norm bag of words	
def file_to_tfidf_l2(file_name):
	vectorizer = TfidfVectorizer(norm='l2', sublinear_tf=True)
	df, X = file_to_dataFrame(file_name, vectorizer)
	return df, X	
	
if __name__ == '__main__':
	print("csv to tf-idf...")
	df, X = file_to_tfidf_l2(sys.argv[1])
	print("save mat file...")
	scipy.io.savemat(sys.argv[1]+"_tf-idf-l2.mat", {'X' : X})
