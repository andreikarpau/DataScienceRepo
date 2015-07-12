complete <- function(directory, id = 1:332) {
  if(!file.exists(directory)) {
    stop('directory does not exist')
  }
  
  idsCount <- length(id)
  dataFrame <- data.frame(id=numeric(idsCount), nobs=numeric(idsCount))

  for (i in 1:idsCount){
    fileName <- sprintf("%s/%s.csv", directory, formatC(id[i], width=3, flag="0"))
    table <- read.csv(fileName, stringsAsFactors = FALSE)
    naSuldate <- is.na(table$sulfate)
    naNitrate <- is.na(table$nitrate)
    nonNaIDs <- table$ID[naSuldate == FALSE & naNitrate == FALSE]
    dataFrame[i, ] <- list(id[i], length(nonNaIDs))
  }
  
  dataFrame
  ## 'id' is an integer vector indicating the monitor ID numbers
  ## to be used
  
  ## Return a data frame of the form:
  ## id nobs
  ## 1  117
  ## 2  1041
  ## ...
  ## where 'id' is the monitor ID number and 'nobs' is the
  ## number of complete cases
}
