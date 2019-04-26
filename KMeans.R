setwd("/media/matthieu/Data/Matthieu/##Etude/#M1/S2/BD2/opinion-mining")

library(aricode)
library(R.matlab)
library(skmeans)

normalize <- function(x) {x / sqrt(rowSums(x^2))}
normalizeByCol <- function(df) { t( normalize( t(df) ) )}
sent_process <- function(x){ x[1] - x[2] + 1 }

# -------------- Dataset loading --------------

#X <- readMat("dataset/mat_files/tweets_clean10.csv_tf-idf-l2.mat")
#df <- X$X

df <- read.csv("dataset/tweets_clean10.csv_doc2Vec_50.csv", header = TRUE, row.names = 1)

dim(df)
mat_df <- as.matrix(df)
mat_df <- normalize(mat_df)
dim(mat_df)

#mat_df[(rowSums(mat_df) == 0), 1] = 1

# ----------------------------------------


#print("run PCA...")
#resPCA <- PCA(mat_df, scale.unit = FALSE, ncp = 50)

#write.csv(resPCA$ind$coord, "pca_coord.csv")
#write.csv(resPCA$eig, "pca_eig.csv")

#mat_df <- resPCA$ind$coord


# -------------- Run --------------

k <- 2

print("run kmeans...")
res_kmeans <- kmeans(mat_df, centers = k)
write.csv(res_kmeans$cluster, "doc2vec_kmeans_clusters.csv")

print("run spherical kmeans...")
res_skmeans <- skmeans(mat_df, k, control = list(verbose = TRUE), method = "pclust")
write.csv(res_skmeans$cluster, "doc2vec_skmeans_clusters.csv")

# ----------------------------------------
