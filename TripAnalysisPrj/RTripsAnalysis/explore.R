library(ggplot2) 
library(data.table)

car_trips <- read.csv("./csv/output/all_trips.csv")
summary(car_trips)

plot_co2_points <- function(car_data) {
  ggplot(data=car_data, aes(x=highway)) + 
    geom_point(aes(y=CO2_value, colour="Emission CO2")) +
    geom_point(aes(y=Speed_value, colour="Speed"), alpha = 0.05, shape=3) 
}

#plot_co2_points(car_trips)

plot_speed_co2 <- function(car_data) {
  ggplot(data=car_data, aes(x=time)) + geom_line(aes(y=Speed_value, colour="Speed")) +
    geom_line(aes(y=CO2_value, colour="Emission CO2")) + 
    geom_point(aes(y=Speed_value, colour=highway)) +
    geom_line(aes(y=Consumption_value, colour="Temp"))
}

car_data = car_trips[car_trips$trip_id=="586ba71de4b04a0d718a7437",]
#plot_speed_co2(car_data)

plot_osm_id <- function(car_data) {
  ggplot(data=car_data, aes(x=highway)) + 
  #  geom_point(aes(y=co2_mean)) +
    geom_point(aes(y=speed_mean, colour="Speed")) +
    geom_point(aes(y=speed_mean/co2_mean, colour="Coef"))
}

dt_trips <- data.table(car_trips)
dt_trips <-dt_trips[,list(co2_mean=mean(CO2_value), count=.N, speed_mean=mean(Speed_value)),by=highway]
plot_osm_id(dt_trips)

