# Fri Feb  3 11:32:43 2023 ------------------------------
library(dplyr)
library(tidyr)

# params
#setwd('projects/Exp16_TXT/') # data from co-culture
setwd("C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/exp16_txt")
files = dir()

# read files
data = list()
for(file in files){
  data[[file]] = read.table(
    file, header = T, sep='\t')
}

# set the timepoint and replicate number
repli = rep(c(rep.int(1, 10), rep.int(2, 10), rep.int(3, 10)), 8)
for(i in 1:240){
  day = ceiling(i / 30)
  data[[i]]$timepoint = day
  data[[i]]$repli = repli[i]
}

# combine the dataset
df = do.call(rbind, data)

df_hacat = filter(df, Type == 1) %>%
  select(Type, timepoint, repli) %>%
  group_by(timepoint) %>%
  count(repli) %>% 
  spread(timepoint, n)


df_sk147 = filter(df, Type == 2) %>%
  select(Type, timepoint, repli) %>%
  group_by(timepoint) %>%
  count(repli) %>%
  spread(timepoint, n)



# Plot for checking...
plot(1:8, df_hacat[1,2:9], pch=16, col='red',
     ylim=c(0,6000))
for(i in 1:3){
  points(1:8, df_sk147[i, 2:9], pch=16, col='blue')
  lines(1:8, df_sk147[i, 2:9], lwd=2, col='blue')

  points(1:8, df_hacat[i, 2:9], pch=16, col='red')
  lines(1:8, df_hacat[i, 2:9], lwd=2, col='red')
}
#dev.off()

df_hacat$repli <- NULL
df_sk147$repli <- NULL
K1 = as.numeric(df_hacat[1,ncol(df_hacat)]) + as.numeric(df_sk147[1,ncol(df_sk147)])
K2 = as.numeric(df_hacat[2,ncol(df_hacat)]) + as.numeric(df_sk147[2,ncol(df_sk147)])
K3 = as.numeric(df_hacat[3,ncol(df_hacat)]) + as.numeric(df_sk147[3,ncol(df_sk147)])

E1 = as.numeric(K1 - (df_hacat[1,] + df_sk147[1,]))
E2 = as.numeric(K2 - (df_hacat[2,] + df_sk147[2,]))
E3 = as.numeric(K3 - (df_hacat[3,] + df_sk147[3,]))

df_E <- tibble(E1,E2,E3)  
colnames(df_E) = colnames(df_hacat)                
#colnames(df_E) <- NULL

df_coc = cbind(t(df_hacat),t(df_sk147),df_E)
colnames(df_coc) <- c("hacat1","hacat2","hacat3",
                      "skmel1","skmel2","skmel3",
                      "E1","E2","E3") 

write.csv(df_coc,
          "C:/R-4.2.2/dataAnalysis_UFRN/BooleanNetworkBioME/booleanKinetics/popTimeSerie.csv",
          row.names=FALSE)

