rm(list = ls())

library(RWeka)

source('~/Documents/CaterpillarTubePricing/Project/AnalyseData.R')

meanSquareError <- function(x, y){
  sqrt(sum((x - y) ^ 2)) / length(x)
}

meanLogError <- function(x, y){
  n <- length(x)
  x0 <- x
  x0[x < 0] <- 0 
  sqrt(sum((log(x0 + 1) - log(y + 1)) ^ 2) / n) 
}

trainSet <- tubesTrainSet
trainSet$tube_assembly_id <- NULL

testSet <- tubesTestSet
testSet$tube_assembly_id <- NULL


lr <- LinearRegression(cost ~ ., data = trainSet)

cat("\n\nPredictor\n")
print(summary(lr))

testCosts <- predict(lr, newdata = testSet[-1])

cat("\n\nPrediction on test set\n\n")
#print(summary(testCosts))

print(head(tubesTestSet$tube_assembly_id))
print(head(tubesTestSet$cost))
print(head(testCosts))
print(meanSquareError(testCosts, tubesTestSet$cost))
print(meanLogError(testCosts, tubesTestSet$cost))