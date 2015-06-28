rm(list = ls())

library(psych)

insurance <- read.csv("Data/insurance.csv", stringsAsFactors = TRUE)

print(str(insurance))
print(summary(insurance$charges))

hist(insurance$charges)

#print the correlation matrix
print(cor(insurance[c("age", "bmi", "children", "charges")]))

#scatter plots matrix
pairs(insurance[c("age", "bmi", "children", "charges")])

#psych scatter plots matrix
pairs.panels(insurance[c("age", "bmi", "children", "charges")])