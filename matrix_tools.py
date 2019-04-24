import sys
import scipy
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from math import log



csr_dot = scipy.sparse.csr_matrix.dot

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
	X = vectorizer.fit_transform(docs) # sparse data
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
	
"""
======= CONTEXT MATRIX with CO-OCCURENCE MATRIX =======
"""
def text_to_co_occurence_matrix(texts_file):
	texts_df = file_to_bow(texts_file)[1]
	
	texts_df[texts_df > 1] = 1
	
	co_occurence_matrix = csr_dot(texts_df.T, texts_df)
	
	print(co_occurence_matrix)
	print(co_occurence_matrix.shape)	
		
	return co_occurence_matrix
	
def compute_pmi(matrix, i, j, row_mat, col_mat, mat_sum, default = 0):
	cij = matrix[i,j]
	cid = row_mat[i]
	cdj = col_mat[j]
	cdd = mat_sum
		
	try:
		ret = log( (cij * cdd) / (cid * cdj) )
	except:
		ret = default
	return ret

def sppmi_context_matrix(matrix, N = 2):
	#sppmi_matrix = np.zeros(matrix.shape)
	sppmi_matrix = scipy.sparse.lil_matrix(matrix.shape)
	shape = matrix.shape[0]
	
	row_mat = matrix.sum(axis = 1)
	row_mat = row_mat.reshape([shape, 1])	
	
	col_mat = matrix.sum(axis = 0)
	col_mat = col_mat.reshape([shape, 1])
	
	mat_sum = matrix.sum()		

	cx = scipy.sparse.coo_matrix(matrix)
	for i,j,v in zip(cx.row, cx.col, cx.data):
		pmi = compute_pmi(matrix, i, j, row_mat, col_mat, mat_sum)
		#sppmi_matrix[i][j] = max(pmi - log(N), 0)
		sppmi_matrix[i,j] = max(pmi - log(N), 0)
	
	sppmi_matrix = scipy.sparse.csr_matrix(sppmi_matrix)
		
	return sppmi_matrix	

def text_to_sppmi_context_matrix(texts_file):
	co_occurence_matrix = text_to_co_occurence_matrix(texts_file)
	return sppmi_context_matrix(co_occurence_matrix)
	
	
	
"""
======= MAIN =======
"""	
if __name__ == '__main__':
	# BOW
	"""print("csv to bow...")
	df, X = file_to_bow(sys.argv[1])
	print("save mat file...")
	scipy.io.savemat(sys.argv[1]+"_bow.mat", {'X' : X})"""

	# TF-IDF L2
	"""print("csv to tf-idf...")
	df, X = file_to_tfidf_l2(sys.argv[1])
	print("save mat file...")
	scipy.io.savemat(sys.argv[1]+"_tf-idf-l2.mat", {'X' : X})"""

	# Context Matrix with Co-Occurence Matrix
	"""sppmi_context_matrix = text_to_sppmi_context_matrix(sys.argv[1])
	scipy.io.savemat(sys.argv[1]+"_sppmi_context_matrix.mat", {'X' : sppmi_context_matrix})"""
	
	# Get vocabulary
	df, X = file_to_bow(sys.argv[1])
	vocab = df.columns.values
	pd.DataFrame(vocab).to_csv(sys.argv[1]+"_vocabulary.csv")
