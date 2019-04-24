import emoji
import numpy as np
import pandas as pd
import sys
import re
from nltk.tokenize import word_tokenize


def emoji_to_sentiment(emojis_file, emoji_sentiment_dict_file, text_column=0):
    texts_df = pd.read_csv(emojis_file, header=0)
    emoji_sentiment_df = pd.read_csv(emoji_sentiment_dict_file, index_col=0)
    doc_emoji_sentiment_matrix = []
    dict_emoji_sentiment_matrix = {}

    # Iterate through all sentiment words in the dictionnary
    for _, sent_vec in emoji_sentiment_df.iterrows():
        sent_emoji = sent_vec[6]
        sent_emoji = sent_emoji.lower()
        sent_emoji = re.sub(" ","_",sent_emoji)
        sent_emoji = sent_emoji
        total = sent_vec[5]+sent_vec[3]+sent_vec[4]

        pos = float(sent_vec[5]/total)
        neg = float(sent_vec[3]/total)
        neu = float(sent_vec[4]/total)

        # print("sent_emoji",sent_emoji)
        # print("pos",pos)
        # print("neg",neg)
        # print("neu",neu)
        # TODO - save this dict to avoid to compute it every time
        dict_emoji_sentiment_matrix[sent_emoji] = (pos, neg, neu)

    # Iterate through all the text
    for _, row in texts_df.iterrows():
        temp = [0., 0., 0.]
        text = row[text_column]
        text = emoji.demojize(text)
        text = re.sub(":","", text)
        # print("text: " ,text)
        for emot in word_tokenize(text):
            print("emot",emot)
            if emot in dict_emoji_sentiment_matrix:
                sent_vec = dict_emoji_sentiment_matrix[emot]
                print("sent_vec en bas", sent_vec)
                temp = np.add(temp, sent_vec)
        doc_emoji_sentiment_matrix.append(temp)
    return doc_emoji_sentiment_matrix


if __name__ == "__main__":
    text_column = 4
    emoji_to_sentiment(sys.argv[1], sys.argv[2], text_column)
