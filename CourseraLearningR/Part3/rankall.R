rankall <- function(outcome, num = "best") {
  data <- read.csv("data/outcome-of-care-measures.csv", colClasses = "character")
  
  data[which(data[11] == "Not Available"), 11] <- NA
  data[which(data[17] == "Not Available"), 17] <- NA
  data[which(data[23] == "Not Available"), 23] <- NA
  
  if (outcome != "heart attack" && outcome != "heart failure" && outcome != "pneumonia")
    stop("invalid outcome")
  
  ## Check that state and outcome are valid
  ## For each state, find the hospital of the given rank
  ## Return a data frame with the hospital names and the
  ## (abbreviated) state name
}