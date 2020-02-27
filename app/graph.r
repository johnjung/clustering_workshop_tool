# usage:
#     rscript graph.r <cutoff> <url> <output_file>
# e.g. (complete, single)
#     rscript graph.r 1 "https://docs.google.com/spreadsheets/d/1IeN0K6LpULcYiqetBl4koNZA1PkKx-NftKgBr0PNxzc/gviz/tq?tqx=out:csv" out.svg
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
cutoff <- args[1]
url <- args[2]
output_filename <- args[3]

my_matrix <- as.matrix(read.table(url, header=TRUE, row.names=1, sep=","))
for (i in 1:nrow(my_matrix)) {
    for (j in 1:i) {
        my_matrix[j,i]=my_matrix[i,j] 
    }
}

# build a dataframe from label pairs. 
column_a <- c() 
column_b <- c() 
for (n in which(my_matrix <= cutoff)) {
    i <- ((n - 1) %/% nrow(my_matrix) + 1)
    j <- ((n - 1) %% nrow(my_matrix) + 1)
    if (i != j) {
        column_a <- c(column_a, rownames(my_matrix)[i])
        column_b <- c(column_b, rownames(my_matrix)[j])
    }   
}
my_df = data.frame(column_a, column_b)

adjacency_matrix = get.adjacency(graph.edgelist(as.matrix(my_df), directed=FALSE))
image <- ggnet2(adjacency_matrix, label=TRUE) + theme(text = element_text(family = "Helvetica, sans-serif"))
ggsave(file=output_filename, device='svg', plot=image, width=17, height=11)
