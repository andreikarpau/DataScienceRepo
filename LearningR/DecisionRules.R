rm(list = ls())

library(RWeka)



mushrooms <- read.csv("Data/mushrooms.csv", stringsAsFactors = TRUE)

print(table(mushrooms$veil_type))
#drop this table since it has only the same values
mushrooms$veil_type <- NULL

#predict using oneR
mushroom_1R <- OneR(type ~ ., data = mushrooms)

print(summary(mushroom_1R))
print(mushroom_1R)

#predict using RIPPER
mushroom_JRip <- JRip(type ~ ., data = mushrooms)

print(summary(mushroom_JRip))
print(mushroom_JRip)
