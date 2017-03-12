
#outcome <- read.csv("data/outcome-of-care-measures.csv", colClasses = "character")
#print(head(outcome))

#outcome[, 11] <- as.numeric(outcome[, 11])
## You may get a warning about NAs being introduced; that is okay
#hist(outcome[, 11])