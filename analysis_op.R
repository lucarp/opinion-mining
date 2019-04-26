setwd("/media/matthieu/Data/Matthieu/##Etude/#M1/S2/BD2/opinion-mining")

library(aricode)
#library(NMI)
library(R.matlab)

normalize <- function(x) {x / sqrt(rowSums(x^2))}
normalizeByCol <- function(df) { t( normalize( t(df) ) )}
sent_process <- function(x){ x[1] - x[2] + 1 }

# -------------- Dataset loading --------------

#X <- readMat("dataset/mat_files/tweets_clean10.csv_tf-idf-l2.mat")

#df <- read.csv("dataset/tweets_clean10.csv_doc2Vec_50.csv", header = TRUE, row.names = 1)

#df <- X$X
#dim(df)
#mat_df <- as.matrix(df)
#mat_df <- normalize(mat_df)
#dim(mat_df)

# ----------------------------------------

k <- 2

lexicon_sent <- read.csv("result/tweets_clean10.csv_lexicon_sentiment.csv")
lexicon_sent <- read.csv("result/tweets_clean10.csv_lexicon_sentiment_pos_neg.csv", row.names = 1)

n_pos <- length(lexicon_sent[lexicon_sent == 1])
n_neg <- length(lexicon_sent[lexicon_sent == 0])
n_neu <- length(lexicon_sent[lexicon_sent == 0.5])
dim(lexicon_sent)[1]

# ----------------------------------------


# -------------- Analysis --------------

# --- Lexicon based

lexicon_cluster <- read.csv("result/tweets_clean10.csv_lexicon_sentiment_pos_neg.csv", row.names = 1)

length(lexicon_cluster[lexicon_cluster == 1])
length(lexicon_cluster[lexicon_cluster == 0])

l_c <- unlist(lexicon_cluster, use.names=FALSE)
#t_c <- 1:length(l_c)
#l_c <- cbind(t_c, l_c)


# --- K-Means

kmeans_cluster = read.csv("result/doc2vec_kmeans_clusters_50.csv", row.names = 1)
kmeans_cluster = read.csv("result/tf_idf_kmeans_clusters.csv", row.names = 1)
kmeans_cluster = read.csv("result/dm_kmeans_clusters.csv", row.names = 1)

kmeans_ind1 = which(kmeans_cluster == 1)
kmeans_ind2 = which(kmeans_cluster == 2)

length(kmeans_cluster[kmeans_ind1,])
length(kmeans_cluster[kmeans_ind2,])

k_c <- unlist(kmeans_cluster, use.names=FALSE)
#k_c <- cbind(t_c, k_c)

NMI(k_c, l_c)
ARI(k_c, l_c)



# --- Spherical K-Means

skmeans_cluster = read.csv("result/doc2vec_skmeans_clusters_50.csv", row.names = 1)
skmeans_cluster = read.csv("result/tf_idf_skmeans_clusters.csv", row.names = 1)
skmeans_cluster = read.csv("result/dm_skmeans_clusters.csv", row.names = 1)

skmeans_ind1 = which(skmeans_cluster == 1)
skmeans_ind2 = which(skmeans_cluster == 2)

length(skmeans_cluster[skmeans_ind1,])
length(skmeans_cluster[skmeans_ind2,])


sk_c <- unlist(skmeans_cluster, use.names=FALSE)
#sk_c <- cbind(t_c, sk_c)

NMI(sk_c, l_c)
ARI(sk_c, l_c)



# --- WC-NMTF / NTMTF

#wcnmtf_res = read.csv("result/doc2vec_wc-nmtf_Z_l1.0.csv")
#wcnmtf_cluster = apply(wcnmtf_res, MARGIN = 1, FUN = which.max)
#write.csv(wcnmtf_cluster, "result/doc2vec_wc_nmtf_clusters.csv")

#wcnmtf_res = read.csv("result/tf_idf_wc-nmtf_Z_l1.0.csv")
#wcnmtf_cluster = apply(wcnmtf_res, MARGIN = 1, FUN = which.max)
#write.csv(wcnmtf_cluster, "result/tf_idf_wc_nmtf_clusters.csv")

#wcnmtf_cluster = read.csv("result/doc2vec_wc_nmtf_clusters.csv", row.names = 1)
wcnmtf_cluster = read.csv("result/tf_idf_wc_nmtf_clusters.csv", row.names = 1)

wcnmtf_ind1 = which(wcnmtf_cluster == 1)
wcnmtf_ind2 = which(wcnmtf_cluster == 2)

length(wcnmtf_cluster[wcnmtf_ind1,])
length(wcnmtf_cluster[wcnmtf_ind2,])


nmtf_c <- unlist(wcnmtf_cluster, use.names=FALSE)
#nmtf_c <- cbind(t_c, nmtf_c)

NMI(nmtf_c, l_c)
ARI(nmtf_c, l_c)

# ----------------------------------------

wc_nmtf <- read.csv("results/wc-nmtf_Z_l0.0.csv")
wc_nmtf <- apply(wc_nmtf, MARGIN = 1, FUN = which.max)
write.csv(wc_nmtf, "results/doc2vec_wc_nmtf_clusters.csv")
