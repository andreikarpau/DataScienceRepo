rm(list = ls())

#source('pollutantmean.R')
#print(pollutantmean('Data', "sulfate", id = 1:10))
#print(pollutantmean('Data', "nitrate", 70:72))
#print(pollutantmean('Data', "nitrate", 23))

source('complete.R')
print(complete('Data', 1))
print(complete('Data', c(2, 4, 8, 10, 12)))
print(complete('Data', 30:25))
print(complete('Data', 3))

      

