rm(list = ls())

source('pollutantmean.R')
print(pollutantmean('Data', "sulfate", id = 1:10))
print(pollutantmean('Data', "nitrate", 70:72))
print(pollutantmean('Data', "nitrate", 23))

      

