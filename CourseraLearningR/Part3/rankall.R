rankall <- function(outcome, num = "best") {
  data <- read.csv("data/outcome-of-care-measures.csv", colClasses = "character")
  
  data[which(data[11] == "Not Available"), 11] <- NA
  data[which(data[17] == "Not Available"), 17] <- NA
  data[which(data[23] == "Not Available"), 23] <- NA
  
  if (outcome != "heart attack" && outcome != "heart failure" && outcome != "pneumonia")
    stop("invalid outcome")

  names <- tapply(data$Hospital.Name, data$State, function(x) {x})
  
  if (outcome == "heart attack") {
    stateData <- tapply(as.numeric(data[[11]]), data$State, function(x) {x})
  }
  else if (outcome == "heart failure") {
    stateData <- tapply(as.numeric(data[[17]]), data$State, function(x) {x})
  }
  else if (outcome == "pneumonia") {
    stateData <- tapply(as.numeric(data[[23]]), data$State, function(x) {x})
  }
  
  matrix <- sapply(names(stateData), function(x) {
    nonNas <- which(!is.na(stateData[[x]]))
    stateData1 <- stateData[[x]][nonNas]
    names1 <- names[[x]][nonNas]
    
    namesO <- names1[order(stateData1, names1)]
    
    if (length(namesO) <= 0){
      c(NA, x)
    }
    else if (num == "best"){
      c(namesO[1], x)
    }
    else if (num == "worst"){
      c(namesO[length(namesO)], x)
    }
    else if (0 < num && num <= length(namesO)){
      c(namesO[num], x)
    }
    else {
      c(NA, x)
    }
    })
  
  matrix <- t(matrix)
  df <- data.frame(matrix)
  colnames(df) <- c("hospital", "state")
  df
}