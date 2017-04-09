library(ggplot2) 
library(data.table)

car_trips <- read.csv("./csv/output/all_trips.csv")
car_trips$time <- strptime(car_trips$time, "%Y-%m-%d %H:%M:%S", tz="UTC")
summary(car_trips)

trip_data <- car_trips[car_trips$trip_id == '52e2164ce4b0d8e8c222bfa1',]

plot_co2_points <- function(car_data) {
  ggplot(data=car_data, aes(x=highway)) + 
    geom_point(aes(y=CO2_value, colour="Emission CO2")) +
    geom_point(aes(y=Speed_value, colour="Speed"), alpha = 0.05, shape=3) 
}

#plot_co2_points(trip_data)

plot_speed_co2 <- function(car_data) {
  ggplot(data=car_data, aes(x=time)) + 
    geom_line(aes(y=Speed_value, colour="Speed")) +
    geom_line(aes(y=CO2_value, colour="Emission CO2")) + 
#    geom_point(aes(y=Speed_value, colour=highway)) +
    geom_line(aes(y=Rpm_value/100, colour="RPM/100")) +
    theme(legend.position="bottom",legend.direction="horizontal")
}

car_data = car_trips[car_trips$trip_id=="587907d4e4b04a0d72561e60",]
plot_speed_co2(car_data)

plot_osm_id <- function(car_data) {
  ggplot(data=car_data, aes(x=highway)) + 
  #  geom_point(aes(y=co2_mean)) +
    geom_point(aes(y=speed_mean, colour="Speed")) +
    geom_point(aes(y=speed_mean/co2_mean, colour="Coef"))
}

dt_trips <- data.table(car_trips)
dt_trips <-dt_trips[,list(co2_mean=mean(CO2_value), count=.N, speed_mean=mean(Speed_value)),by=highway]
plot_osm_id(dt_trips)

