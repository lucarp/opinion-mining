from gensim import corpora, models
import pyLDAvis
import pyLDAvis.gensim
import pandas as pd 

data = pd.read_csv("dataset/tweets_clean10.csv")

list_of_list_of_tokens = []
for item in data["Review"]:
    list_of_list_of_tokens.append(item.split(' '))


dictionary_LDA = corpora.Dictionary(list_of_list_of_tokens)
dictionary_LDA.filter_extremes(no_below=3)
corpus = [dictionary_LDA.doc2bow(list_of_tokens) for list_of_tokens in list_of_list_of_tokens]

num_topics = 3
lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary_LDA, passes=4, alpha=[0.01]*num_topics, eta=[0.01]*len(dictionary_LDA.keys()))

for i,topic in lda_model.show_topics(formatted=True, num_topics=num_topics, num_words=50):
    print(str(i)+": "+ topic)
    print()



lda_model[corpus[0]] # corpus[0] means the first document.


vis = pyLDAvis.gensim.prepare(topic_model=lda_model, corpus=corpus, dictionary=dictionary_LDA)
pyLDAvis.enable_notebook()
pyLDAvis.display(vis)
#creates webserver
pyLDAvis.show(vis)
