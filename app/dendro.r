# usage:
#     rscript dendro.r <linkage_method> <url> <output_file>
# e.g.:
#     rscript dendro.r complete "https://docs.google.com/spreadsheets/d/1IeN0K6LpULcYiqetBl4koNZA1PkKx-NftKgBr0PNxzc/gviz/tq?tqx=out:csv"
# outputs an SVG to stdout.

library('GGally')
library('ggdendro')
library('ggplot2')
library('igraph')
library('network')
library('sna')
library('svglite')
library('textshape')

args = commandArgs(trailingOnly=TRUE)
output_filename <- args[3]

my_matrix <- as.matrix(read.table(args[2], header=TRUE, row.names=1, sep=","))

# copy upper triangle of matrix to lower triangle. 
for (i in 1:nrow(my_matrix)) {
    for (j in 1:i) {
        my_matrix[j,i]=my_matrix[i,j] 
    }
}

hc <- hclust(as.dist(my_matrix), method = args[1])
image <- ggdendrogram(hc, rotate = TRUE, theme_dendro = FALSE)
ggsave(file=output_filename, device='svg', plot=image, width=10, height=8)
