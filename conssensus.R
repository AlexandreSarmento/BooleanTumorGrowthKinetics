conssensusBin <- function(bin_data){
  
  df_bin <- list() #create an empty list

  deltaC1 = 1
  deltaC2 = 3
  binData <- t(bin_data)
  for (cols in 1:3) {
    
    vec <- numeric(8) #preallocate a numeric vector
  
    for (rows in 1:8) {
      
      if((sum(binData[rows,deltaC1:deltaC2])/3) > 0.5){
        
        vec[rows] <- 1
        
      } else {
        
        vec[rows] <- 0
          
        
      }
    
    }
    deltaC1 = deltaC1 + 3
    deltaC2 = deltaC2 + 3
    df_bin[[cols]] <- t(vec) #put all vectors in the list
  }
  df_bin <- do.call("rbind",df_bin) #combine all vectors into a matrix
  rownames(df_bin) <- c("HaCat","Skmel-147","E")
  return(df_bin) 
}