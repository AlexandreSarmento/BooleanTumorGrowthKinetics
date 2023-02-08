working_dir <- "C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics" 
setwd(working_dir)

path2inputFile <- "/IKM/popTimeSerie_"
path2outputFile <- "/IKM/binAvg"
inputFileName = paste0(working_dir,path2inputFile)
outputFileName = paste0(working_dir,path2inputFile)
numberOfInputFiles = 100
allTimePoints = list(1,2,3,4,5,6,7,8)


mainCsv <- "/popTimeSerie.csv"
popDensity2bin <- read.csv(paste0(working_dir,mainCsv),
                           header=TRUE, 
                           stringsAsFactors=FALSE)


tauA = 0.01
tauB = 0.01
sigma = 4.0