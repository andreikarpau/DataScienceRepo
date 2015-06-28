rm(list = ls())

insurance <- read.csv("Data/insurance.csv", stringsAsFactors = TRUE)

print(str(insurance))
print(summary(insurance$charges))

hist(insurance$charges)