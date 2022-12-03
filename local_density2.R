# Tue Oct  4 16:24:34 2022 ------------------------------
#'
#' estimate local density
#' 
#' @author Mauro Morais

#  para calcular a densidade local (3x3). 
# Este script depende da função kernsmooth que está no arquivo aux_functions.R
source('C:/R/R-4.2.1/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/distanceDensity/aux_functions.R')

library('pheatmap')
library(ggplot2)
# Load data
path = "C:/R/R-4.2.1/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/heatmapCsv/hipo2"
setwd(path)
filesName <- "C:/R/R-4.2.1/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/heatmapCsv/hipo2/matrix7.csv"
simFrame <- read.csv(filesName)
#Get cells clusters
matrix_skmel = simFrame == 1
matrix_hacat = simFrame == 2
matrix_both = simFrame != 0
# Estimate local (side x side) cell density
side = 3
local_density = kernelsmooth(matrix_both, matrix(rep(1,side**2), nrow=side))
local_density_hacat = abs(local_density - matrix_skmel)
local_density_skmel = abs(local_density - matrix_hacat)
# Plot hacat local density of hacat
p1 <- pheatmap((local_density_hacat > 0.9)*1, #local_density,
                color = colorRampPalette(c('blue','yellow'))(256),#gray(seq(0,1, length.out=256)),
                cluster_rows = F, cluster_cols = F,
                show_rownames = F, show_colnames = F,
                height= 200,
                width=height/1.618)
  
ggsave(filename=paste0("nghDensity_8_90_h2.png"),plot = p1)