library(ggplot2) 
library(data.table)
library(corrplot)

car_trips <- read.csv("./csv/output/all_aggregated_trips.csv")
car_trips$X <- NULL
str(car_trips)
summary(car_trips)

car_trips <- car_trips[0 < car_trips$distance,]
car_trips$co2_emission_per_dist <- car_trips$co2_emission / car_trips$time_diff 
summary(car_trips)

numeric_car_trips <- car_trips[,-c(3, 4, 8, 9, 10, 21)]

numeric_cor_matrix <- cor(numeric_car_trips)

corrplot(numeric_cor_matrix, method="number")

