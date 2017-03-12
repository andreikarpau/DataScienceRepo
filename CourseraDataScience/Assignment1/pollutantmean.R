pollutantmean <- function(directory, pollutant, id = 1:332) {
  if(!file.exists(directory)) {
    stop('directory does not exist')
  }
  
  if (pollutant != 'sulfate' && pollutant != 'nitrate'){
    stop('pollutant should be either "sulfate" or "nitrate"')
  }
  
  newTable <- TRUE
  
  for (i in id){
    fileName <- sprintf("%s/%s.csv", directory, formatC(i, width=3, flag="0"))
    table <- read.csv(fileName, stringsAsFactors = FALSE)
    
    if (newTable){
      wholeTable <- table
      newTable <- FALSE
    }
    else{
      wholeTable <- rbind(wholeTable, table)
    }
  }

  allValues <- wholeTable[pollutant]
  values <- allValues[!is.na(allValues)]
  mean(values)
}