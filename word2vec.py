import sys
import gensim
import pandas as pd

def train_dataset(reviews):
	list_of_lists = []
	for item in reviews['Review']:
		list_of_lists.append(item.split(' '))
	return list_of_lists


def word2Vec(file_name, vec_size = 100):
	texts_df = pd.read_csv(file_name, header=0, index_col=0)

	print("make corpus...")
	train_corpus = train_dataset(texts_df)

	model = gensim.models.Word2Vec(size=vec_size, iter = 1)
	model.build_vocab(train_corpus)
	print("training...")
	model.train(train_corpus, total_examples=len(train_corpus), epochs=model.epochs)
	
	return model

def word2vec_to_embeddings(word2vec, vocabulary):
	df = pd.read_csv(vocabulary, index_col = 0)
	vecs = []
	for _, word in df.iterrows():
		word = word['0']
		if word != word:
			continue
		vec = word2vec.wv.get_vector(word)
		vecs.append(vec)
		
	return vecs

if __name__ == "__main__":
	word2vec = word2Vec(sys.argv[1])
	vecs = word2vec_to_embeddings(word2vec, sys.argv[2])
	print("save...")
	pd.DataFrame(vecs).to_csv(sys.argv[1]+"_word2Vec.csv")
