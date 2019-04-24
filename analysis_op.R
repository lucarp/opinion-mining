setwd("/media/matthieu/Data/Matthieu/##Etude/#M1/S2/BD2/opinion-mining")

library(aricode)
library(R.matlab)
library(cluster)

normalize <- function(x) {x / sqrt(rowSums(x^2))}
normalizeByCol <- function(df) { t( normalize( t(df) ) )}
sent_process <- function(x){ x[1] - x[2] + 1 }

# -------------- Dataset loading --------------

X <- readMat("dataset/mat_files/tweets_clean10.csv_tf-idf-l2.mat")

#df <- read.csv("dataset/tweets_clean10.csv_doc2Vec.csv", header = TRUE, row.names = 1)

df <- X$X
dim(df)
#mat_df <- as.matrix(df)
#mat_df <- normalize(mat_df)
#dim(mat_df)

# ----------------------------------------

k <- 2

lexicon_sent <- read.csv("results/tweets_clean10.csv_lexicon_sentiment.csv")
lexicon_sent <- read.csv("results/tweets_clean10.csv_lexicon_sentiment_pos_neg.csv", row.names = 1)

n_pos <- length(lexicon_sent[lexicon_sent == 1])
n_neg <- length(lexicon_sent[lexicon_sent == 0])
n_neu <- length(lexicon_sent[lexicon_sent == 0.5])
dim(lexicon_sent)[1]

silhouette(list(lexicon_sent))
