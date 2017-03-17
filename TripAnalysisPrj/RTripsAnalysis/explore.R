library(ggplot2) 
library(data.table)

create_car_trips_dataframe <- function(csv_file_name){
  car_trips = read.csv(csv_file_name)
  car_trips$time <- strptime(car_trips$time, "%Y-%m-%dT%H:%M:%S", tz="UTC")
  car_trips <- car_trips[with(car_trips, order(time, trip_id)), ] 
  
  car_trips$measure_index <- NULL
  #car_trips$date <- as.Date(as.POSIXct(car_trips$time, 'GMT'))
  
  car_trips$Acceleration = 0
  
  for (i in 1:(length(car_trips$Speed_value) - 1)){
    next_i = i + 1

    if (car_trips$trip_id[next_i] == car_trips$trip_id[i]){
      speed_diff = car_trips$Speed_value[next_i] - car_trips$Speed_value[i]
      time_diff = as.numeric(car_trips$time[next_i] - car_trips$time[i], units="hours")
      car_trips$Acceleration[i] = speed_diff/time_diff * 1000/3600
    }
  }
  
  return(car_trips)
} 

csv_files = list.files(path = "./csv/", pattern="*.csv", full.names=TRUE)
car_trips = create_car_trips_dataframe(csv_files[6])
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

