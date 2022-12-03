# Tue Oct  4 18:17:47 2022 ------------------------------

library('pheatmap')

# Plot hacat cells
pheatmap(matrix_hacat * 1,
         color = c('white', 'red'),
         cluster_rows = F, cluster_cols = F,
         show_rownames = F, show_colnames = F,
         legend = F
         # legend_breaks = 0:2, legend_labels = 0:2
)

# Plot skmel cells
pheatmap(matrix_skmel * 1,
         color = c('white', 'blue'),
         cluster_rows = F, cluster_cols = F,
         show_rownames = F, show_colnames = F,
         legend = F
         # legend_breaks = 0:2, legend_labels = 0:2
)

# Plot both cells
pheatmap(matrix_both * 1,
         color = c('white', 'orange'),
         cluster_rows = F, cluster_cols = F,
         show_rownames = F, show_colnames = F,
         legend = F
         # legend_breaks = 0:2, legend_labels = 0:2
)

# Plot hacat local density of hacat
pheatmap(local_density_hacat, #local_density,
         color = colorRampPalette(c('blue','yellow'))(256),#gray(seq(0,1, length.out=256)),
         cluster_rows = F, cluster_cols = F,
         show_rownames = F, show_colnames = F
         # legend = F
         # legend_breaks = 0:2, legend_labels = 0:2
)

# # Plot hacat local density of hacat
# pheatmap((local_density_hacat > 0.4)*1, #local_density,
#          color = colorRampPalette(c('white','orange','red'))(256),#gray(seq(0,1, length.out=256)),
#          cluster_rows = F, cluster_cols = F,
#          show_rownames = F, show_colnames = F
#          # legend = F
#          # legend_breaks = 0:2, legend_labels = 0:2
# )


# just checking the contours...
image(local_density_hacat, 
      col=colorRampPalette(c('black', 'red'))(256)
)

lines(min_max_norm(contours[,1]), min_max_norm(contours[,2])-0.02, lwd=2, col='cyan')
