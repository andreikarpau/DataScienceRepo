rm(list=ls())

library("stats")
source('GetAndPrepareData.R')
#dev.off() Reset graphics to plot properly

trainData$QuoteNumber <- NULL

#model <- lm(QuoteConversion_Flag ~ SSlogis(I(a*Year + b*Month + c*GeographicField63), 1, 0.5, 0.05), data = trainData, start = list(a = 1, b = 0, c = 2))
#model <- glm(QuoteConversion_Flag ~ ., data=trainData)

corr <- cor(trainData$QuoteConversion_Flag, trainData[3:520])
corr[is.na(corr)] <- 0
plot(seq(1, 518), corr, ylim=c(-1,1), xlim=c(0,518))