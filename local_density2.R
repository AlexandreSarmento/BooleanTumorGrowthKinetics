# Tue Oct  4 16:24:34 2022 ------------------------------
#'
#' estimate local density
#' 
#' @author Mauro Morais

#  para calcular a densidade local (3x3). 
# Este script depende da função kernsmooth que está no arquivo aux_functions.R
source('C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/distanceDensity/aux_functions.R')
library('pheatmap')
library('ggplot2')
# Load data
path = "C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/heatmapCsv"
setwd(path)
filesName <- "C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/heatmapCsv/matrix12.csv"
simFrame <- read.csv(filesName)
#Get cells clusters
matrix_skmel = simFrame == 1
matrix_hacat = simFrame == 2
matrix_both = simFrame != 0
# Estimate local (side x side) cell density
side = 5
local_density = kernelsmooth(matrix_both, matrix(rep(1,side**2), nrow=side))
local_density_hacat = abs(local_density - matrix_skmel)
local_density_skmel = abs(local_density - matrix_hacat)

png("ngh0fig13.png", width = 6, height = 6, units = 'in', res = 300)
pheatmap(
         local_density_hacat, #local_density,
         color = colorRampPalette(c('blue','yellow'))(256),#gray(seq(0,1, length.out=256)),
         cluster_rows = F, cluster_cols = F,
         show_rownames = F, show_colnames = F
         )
dev.off()