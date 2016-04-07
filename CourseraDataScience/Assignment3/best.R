best <- function(state, outcome) {
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
    vals <- which(as.numeric(stateData[[11]]) == min(as.numeric(stateData[[11]]), na.rm = TRUE))
  }
  else if (outcome == "heart failure") {
    vals <- which(as.numeric(stateData[[17]]) == min(as.numeric(stateData[[17]]), na.rm = TRUE))
  }
  else if (outcome == "pneumonia") {
    vals <- which(as.numeric(stateData[[23]]) == min(as.numeric(stateData[[23]]), na.rm = TRUE))
  }
  
  if (0 < length(vals)) {
    hospitals <- sort(stateData$Hospital.Name[vals])
    hospitals[1]
  } 
  else{
    NA  
  } 
}