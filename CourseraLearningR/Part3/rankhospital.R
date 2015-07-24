rankhospital <- function(state, outcome, num = "best") {
  data <- read.csv("data/outcome-of-care-measures.csv", colClasses = "character")
  
  data[which(data[11] == "Not Available"), 11] <- NA
  data[which(data[17] == "Not Available"), 17] <- NA
  data[which(data[23] == "Not Available"), 23] <- NA
  
  if (sum(data$State == state) <= 0)
    stop("invalid state")
  
  if (outcome != "heart attack" && outcome != "heart failure" && outcome != "pneumonia")
    stop("invalid outcome")
  
  stateData <- data[data$State == state, ]
  
  ## Return hospital name in that state with lowest 30-day death
  if (outcome == "heart attack") {
    stateDataVals <- as.numeric(stateData[[11]])
  }
  else if (outcome == "heart failure") {
    stateDataVals <- as.numeric(stateData[[17]])
  }
  else if (outcome == "pneumonia") {
    stateDataVals <- as.numeric(stateData[[23]])
  }
  
  stateData <- stateData[-which(is.na(stateDataVals)), ]
  stateDataVals <- stateDataVals[-which(is.na(stateDataVals))]
  stateData <- stateData[order(stateDataVals, stateData$Hospital.Name), ]

  if (num == "best"){
    stateData$Hospital.Name[1]
  }
  else if (num == "worst"){
    stateData$Hospital.Name[length(stateData$Hospital.Name)]
  }
  else if (0 < num && num <= length(stateData$Hospital.Name)){
    stateData$Hospital.Name[num]
  }
  else {
    NA
  }
    
  ## Return hospital name in that state with the given rank
  ## 30-day death rate
}