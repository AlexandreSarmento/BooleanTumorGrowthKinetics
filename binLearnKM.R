# Here we binarize the cell count data, calculate the consenssus of samples 
# binarized and plot the heatmaps

# call libraries
library(igraph)
library(BoolNet)
library(Binarize)

# call modules
source("C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/iterativeKM.R")
source("C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/setData.R")
source("C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/conssensus.R")
source("C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/conssensus2.R")

# Iterative k-mean binarization and consennsus
binRepliIKM <- readBinDataIKM(inputFileName,
                              outputFileName,
                              numberOfInputFiles)
consIKM <- conssensusBin(binRepliIKM$S1)

# k-mean binarization and consennsus
binRepliKM1 <- binarizeTimeSeries(popDensity2bin, 
                                  method="kmeans")$binarizedMeasurements 
consKM1 <- conssensusBin2(binRepliKM1)
rownames(consKM1) <- c("HaCat","Skmel-147","E")

# BASCA binarization and consennsus
binRepliBASCA <- binarizeMatrix(popDensity2bin, 
                                method="BASCA", 
                                tau = tauA)
consBASCA <- conssensusBin2(binRepliBASCA)
rownames(consBASCA) <- c("HaCat","Skmel-147","E")

# BASCB binarization and consennsus
binRepliBASCB <- binarizeMatrix(popDensity2bin,
                                method = "BASCB", 
                                tau = tauB,
                                sigma = sigma)
consBASCB <- conssensusBin2(binRepliBASCB)
rownames(consBASCB) <- c("HaCat","Skmel-147","E")

# Plot the binarized state heatmap and the consenssus of the binarization 
# iterative k-means
plotBinIKM  <- plotHeatMap(binRepliIKM$S1,
                           "binRepliIKM",
                           allTimePoints)
plotConsIKM  <- plotHeatMap(consIKM,
                            "consIKM",
                            allTimePoints)

# k-means
plotBinKM1  <- plotHeatMap(t(binRepliKM1),
                           "binRepliKM1",
                           allTimePoints)
plotConsKM1  <- plotHeatMap(consKM1,
                            "consKM1",
                            allTimePoints)

# BASC-A
plotBinBASCA  <- plotHeatMap(t(binRepliBASCA),
                             paste("binRepliBASCA_","tau_",tauB),
                             allTimePoints)
plotConsBASCA  <- plotHeatMap(consBASCA,
                              "consBASCA",
                              allTimePoints)

# BASC-B
plotBinBASCB  <- plotHeatMap(t(binRepliBASCB),
                             paste("binRepliBASCB_","tau_",tauB,"_sig_",sigma),
                             allTimePoints)
plotConsBASCB  <- plotHeatMap(consBASCB,
                              "consBASCB",
                              allTimePoints)

# inferring probabilistic boolean network (ibn)
ibn <- reconstructNetwork(consIKM,
                          method="bestfit",
                          maxK=1,
                          readableFunctions=TRUE,
                          returnPBN=TRUE)
ibn

# Set a boolean network in a file with extension bn
path2bn <- "C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/popNet.bn" 
# generate the file with bn extension cotaining the boolean network
try({
  sink(path2bn)
  cat("targets, factors\n")
  cat("HaCat, Skmel \n")
  cat("Skmel, Skmel \n")
  cat("E, !Skmel \n")
  sink()}, 
  silent = T)

# Load and print the boolean network 
net <- loadNetwork(path2bn)
print(net)

# search for attractor and plot a heatmap
attr <- getAttractors(net,type="synchronous")
plotAttractors(attr,
               drawLegend = FALSE,
               onColor = "#ffff00",
               offColor = "#0000ff",
               allInOnePlot=TRUE)
# check state transition table
getTransitionTable(attr)
# plot the State Graph just in case
plotStateGraph(attr,highlightAttractors = TRUE, 
               colorBasins = TRUE, 
               drawLegend = TRUE, drawLabels = TRUE, 
               layout = layout.kamada.kawai,
               piecewise = FALSE,
               basin.lty = 2, attractor.lty = 1,
               plotIt = TRUE, 
               colorsAlpha = c(colorBasinsNodeAlpha    = .2,
                               colorBasinsEdgeAlpha    = .2,
                               colorAttractorNodeAlpha = 1,
                               colorAttractorEdgeAlpha = 1))
# # Set a probabilistic boolean network in a file with extension bn
# setwd("C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics")
# path2probn <- "C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/probPopNet.bn" 
# 
# # probabilities
# try({
#   sink(path2probn)
#   cat("targets, factors \n")
#   cat("HaCat, Skmel \n")
#   cat("Skmel, Skmel \n")
#   cat("E, !Skmel | !HaCat \n")
# sink()}, silent = T)
# 
# # Load and Check the boolean network 
# probNet <- loadNetwork(path2probn)
# print(probNet)
# search for attractor
# probAttr <- markovSimulation(probNet)
# probAttr