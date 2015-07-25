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
    nas <- which(is.na(stateData[[x]]))
    stateData1 <- stateData[[x]][-nas]
    names1 <- names[[x]][-nas]
    namesO <- names1[order(stateData1, names1)]

    if (num == "best"){
      c(namesO[1], x)
    }
    else if (num == "worst"){
      c(namesO[length(namesO)], x)
    }
    else if (0 < num && num <= length(namesO)){
      c(namesO[num], x)
    }
    else {
      NA
    }
    })
  
  matrix <- t(matrix)
  df <- data.frame(matrix)
  names(df) <- c("hospital", "state")
  df
  ## For each state, find the hospital of the given rank
  ## Return a data frame with the hospital names and the
  ## (abbreviated) state name
}