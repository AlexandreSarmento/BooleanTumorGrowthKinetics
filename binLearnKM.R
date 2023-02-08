library(igraph)
library(BoolNet)
library(Binarize)

source("C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/iterativeKM.R")
source("C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/setData.R")
source("C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/conssensus.R")


binIKM <- readBinDataIKM(inputFileName,outputFileName,numberOfInputFiles)
binIKM <- conssensusBin(binIKM$S1)

binKM1 <- binarizeTimeSeries(popDensity2bin, method="kmeans")$binarizedMeasurements

binBASCA <- binarizeMatrix(popDensity2bin, 
                           method="BASCA", 
                           tau = tauA)


binBASCB <- binarizeMatrix(popDensity2bin, 
                           method = "BASCB",
                           tau = tauB,
                           sigma = sigma)


plotBinIKM  <- plotHeatMap(binIKM,"binPop_iKM",allTimePoints)
plotBinKM  <- plotHeatMap(t(binKM1),"binPop_KM",allTimePoints)

plotBinBASCA  <- plotHeatMap(t(binBASCA),
                             paste("BASCA_","tau_",
                             tauB),allTimePoints)

plotBinBASCB  <- plotHeatMap(t(binBASCB),
                             paste("BASCB_","tau_",
                             tauB,"_sig_",sigma),allTimePoints)



  





