corr <- function(directory, threshold = 0) {
  if(!file.exists(directory)) {
    stop('directory does not exist')
  }
  
  cases <- complete(directory)
  ids <- cases$id[cases$nobs > threshold]
  
  idsCount <- length(ids)
  correlations <- numeric(idsCount)
  
  if (idsCount <= 0){
    return(correlations)
  }
  
  for (i in 1:idsCount){
    fileName <- sprintf("%s/%s.csv", "Data", formatC(ids[i], width=3, flag="0"))
    table <- read.csv(fileName, stringsAsFactors = FALSE)
    naSulfate <- is.na(table$sulfate)
    naNitrate <- is.na(table$nitrate)
    nonNa <- naSulfate == FALSE & naNitrate == FALSE
    sulfate <- table$sulfate[nonNa]
    nitrate <- table$nitrate[nonNa]
    correlations[i] <- cor(sulfate, nitrate)
  }
  
  return(correlations)
}