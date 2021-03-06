# usage:
#     rscript matrix.r <linkage_method> <url> <output_file>
# e.g.:
#     rscript matrix.r complete "https://docs.google.com/spreadsheets/d/1IeN0K6LpULcYiqetBl4koNZA1PkKx-NftKgBr0PNxzc/gviz/tq?tqx=out:csv" out.svg
# outputs an SVG to stdout.

library('GGally')
library('ggdendro')
library('ggplot2')
library('igraph')
library('network')
library('sna')
library('svglite')
library('textshape')

# get command line arguments.
args = commandArgs(trailingOnly=TRUE)

url <- args[2]
output_filename <- args[3]

my_matrix <- as.matrix(read.table(url, header=TRUE, row.names=1, sep=","))

# fill in the matrix. 
for (i in 1:nrow(my_matrix)) { 
    for (j in 1:i) {
        my_matrix[j,i]=my_matrix[i,j] 
    }
}

# reorder matrix.
my_matrix <- cluster_matrix(my_matrix, dim="both", method=args[1])

data <- expand.grid(X=rownames(my_matrix), Y=rownames(my_matrix))
data$Z <- as.vector(my_matrix)
image <- ggplot(data, aes(X, Y, fill= Z)) + geom_tile() + theme(axis.text.x = element_text(angle=90, hjust=1), text = element_text(family = "Helvetica, sans-serif"))
ggsave(file=output_filename, device='svg', plot=image, width=10, height=8)
