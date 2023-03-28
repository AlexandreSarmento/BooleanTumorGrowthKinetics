library(gplots)
library(RColorBrewer)
library(reshape2)
library(ggplot2)
library(png)

plotHeatMap <- function(sample,titleDescripter,timePoints){
  
  my_palette <- colorRampPalette(c("blue", "gray", "yellow"))(n = 299)
  col_breaks = c(seq(0,.1,length=100),  # for green
                 seq(.11,0.9,length=100),              # for yellow
                 seq(0.91,1,length=100))
  
  rnames <- rownames(sample)          # assign labels in column 1 to "rnames"                           
  mat_data <- data.matrix(sample[,1:ncol(sample)])  # transform column 2- # of timepts into a matrix
  rownames(mat_data) <- rnames                  # assign row names 
  colnames(mat_data) <- timePoints
  # creates a 5 x 5 inch image
  outputName =paste(titleDescripter,".png",sep="") 
  png(outputName,   # create PNG for the heat map        
      width = 4*500,        # 5 x 300 pixels
      height = 3*500,
      res = 500,            # 300 pixels per inch
      pointsize = 6)      # smaller font size
  par(cex.main=0.8,cex.lab = 1)
  heatmap.2(mat_data,
            offsetCol = 2,
            offsetRow = 0,
            srtCol=270,
            notecol="black",      # change font color of cell labels to black
            density.info="none",  # turns off density plot inside color legend
            trace="none",         # turns off trace lines inside the heat map
            margins =c(9,12),     # widens margins around plot
            col=my_palette,       # use on color palette defined earlier 
            breaks=col_breaks,    # enable color transition at specified limits
            dendrogram="none",    # don't draw dendrograms
            Colv="NA",            # turn off column clustering
            Rowv="NA",            # turn off row clustering
            #srtCol=0,
            adjCol= c(.5,.5),
            adjRow= c(0,.5),
            sepwidth=c(0.001,0.001),
            sepcolor="black",
            colsep=1:ncol(mat_data),
            rowsep=1:nrow(mat_data),
            cexRow = 1.0,
            cexCol=.8,
            keysize = 1,
            #density.info=c("histogram","density","none"),
            key.title = NA,
            key.ylab = NA,
            key.xlab = "Binarized Abundance",
            key.ytickfun = NA
  )
  dev.off()               # close the PNG device  
}

readBinDataIKM <- function(inputFileName,outpuFileName,numberOfInputFiles) {
  
  mergedSampleList = list()
  for(i in 1:numberOfInputFiles){
    sampleName = paste(inputFileName,toString(i),".csv",sep="")
    mergedSample <- read.csv(sampleName, comment.char = "#", header=FALSE, check.names=FALSE,row.names=1)
    mergedSampleList[[i]] = mergedSample
  }
  
  s1 = mergedSampleList[[1]]
  noRows = length(s1[,1])
  noColumns = length(s1[1,])
  rowList = c(1:noRows)
  colList = c(1:noColumns)
  exprAverage = data.frame(row.names = rownames(data.frame(s1)))
  exprCumulative = data.frame(row.names = rownames(data.frame(s1)))
  rownames(exprAverage) = rownames(data.frame(s1))
  
  for(rowVal in rowList){
    for(colVal in colList){
      cumulativeVal = 0
      for(sample in mergedSampleList){
        tmpVal = sample[rowVal,colVal]
        cumulativeVal = tmpVal + cumulativeVal 
      }
      exprCumulative[rowVal,colVal]= cumulativeVal
      exprAverage[rowVal,colVal]= round(cumulativeVal/length(mergedSampleList),1)
    }
  }
  
  avgSampleList = list('S1' = exprAverage)
  binAvgSampleList = avgSampleList
  name = 'S1'
  
  for(name in names(avgSampleList)){
    
    tmpSample = avgSampleList[[name]]
    noRows = length(tmpSample[,1])
    noColumns = length(tmpSample[1,])
    rowList = c(1:noRows)
    colList = c(1:noColumns)
    for(rowVal in rowList){
      for(colVal in colList){
        tmpVal = tmpSample[rowVal,colVal]
        if(tmpVal > 0.5){
          tmpSample[rowVal,colVal] = 1
        }
        if(tmpVal < 0.5){
          tmpSample[rowVal,colVal] = 0
        }
        # the binarized version of avg sample list
        binAvgSampleList[[name]] = tmpSample
      }
    }
  }
  
  for(name in names(binAvgSampleList)){
    fileBinName =paste(outpuFileName,name,".csv",sep="")
    write.table(binAvgSampleList[[name]], file = fileBinName, sep= ',',quote=FALSE, row.names = 
                  rownames(binAvgSampleList[[name]]))
    
  }
  
  return(binAvgSampleList) 
}


