setwd("/media/matthieu/Data/Matthieu/##Etude/#M1/S2/BD2/opinion-mining")

library(aricode)
library(R.matlab)

normalize <- function(x) {x / sqrt(rowSums(x^2))}
normalizeByCol <- function(df) { t( normalize( t(df) ) )}
sent_process <- function(x){ x[1] - x[2] + 1 }

# -------------- Dataset loading --------------

#X <- readMat("dataset/mat_files/tweets_clean10.csv_tf-idf-l2.mat")

#df <- read.csv("dataset/tweets_clean10.csv_doc2Vec.csv", header = TRUE, row.names = 1)

#df <- X$X
#dim(df)
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

# ----------------------------------------


# -------------- Analysis --------------

# --- Lexicon based

lexicon_cluster <- read.csv("results/tweets_clean10.csv_lexicon_sentiment_pos_neg.csv", row.names = 1)

length(lexicon_cluster[lexicon_cluster == 1])
length(lexicon_cluster[lexicon_cluster == 0])



# --- K-Means

kmeans_cluster = read.csv("results/doc2vec_kmeans_clusters.csv", row.names = 1)

kmeans_ind1 = which(kmeans_cluster == 1)
kmeans_ind2 = which(kmeans_cluster == 2)

length(kmeans_cluster[kmeans_ind1,])
length(kmeans_cluster[kmeans_ind2,])



# --- Spherical K-Means

skmeans_cluster = read.csv("results/doc2vec_skmeans_clusters.csv", row.names = 1)

skmeans_ind1 = which(skmeans_cluster == 1)
skmeans_ind2 = which(skmeans_cluster == 2)

length(skmeans_cluster[skmeans_ind1,])
length(skmeans_cluster[skmeans_ind2,])


NMI(skmeans_cluster, lexicon_cluster)
ARI(skmeans_cluster, lexicon_cluster)



# --- WC-NMTF / NTMTF

wcnmtf_cluster = read.csv("results/doc2vec_wc_nmtf_clusters.csv", row.names = 1)

wcnmtf_ind1 = which(wcnmtf_cluster == 1)
wcnmtf_ind2 = which(wcnmtf_cluster == 2)

length(wcnmtf_cluster[wcnmtf_ind1,])
length(wcnmtf_cluster[wcnmtf_ind2,])

# ----------------------------------------

wc_nmtf <- read.csv("results/wc-nmtf_Z_l0.0.csv")
wc_nmtf <- apply(wc_nmtf, MARGIN = 1, FUN = which.max)
write.csv(wc_nmtf, "results/doc2vec_wc_nmtf_clusters.csv")
