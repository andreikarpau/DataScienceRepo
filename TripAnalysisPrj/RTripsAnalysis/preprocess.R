library(ggplot2) 

create_car_trips_dataframe <- function(csv_file_name){
  car_trips = read.csv(csv_file_name)
  car_trips$time <- strptime(car_trips$time, "%Y-%m-%dT%H:%M:%S", tz="UTC")
  car_trips <- car_trips[with(car_trips, order(time)), ] 
  car_trips$date <- as.Date(as.POSIXct(car_trips$time, 'GMT'))
  return(car_trips)
} 

plot_co2_points <- function(car_data) {
  ggplot(data=car_data, aes(x=highway)) + 
    geom_point(aes(y=CO2_value, colour="Emission CO2")) +
    geom_point(aes(y=Speed_value, colour="Speed"), alpha = 0.05, shape=3) 
}

csv_files = list.files(path = "./csv/", pattern="*.csv", full.names=TRUE)
car_trips = create_car_trips_dataframe(csv_files[8])


car_data = car_trips[car_trips$trip_id=="5850443ae4b0a979d5501cb3",]
plot_co2_points(car_trips)

plot_speed_co2 <- function(car_data) {
  ggplot(data=car_data, aes(x=time)) + geom_line(aes(y=Speed_value, colour="Speed")) +
    geom_line(aes(y=CO2_value, colour="Emission CO2")) + 
    geom_point(aes(y=Speed_value, colour=highway)) +
    geom_line(aes(y=Intake.Pressure_value, colour="Temp"))
}

plot_speed_co2(car_data)


