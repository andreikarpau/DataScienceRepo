library(ggplot2) 

create_car_trips_dataframe <- function(csv_file_name){
  car_trips = read.csv(csv_file_name)
  car_trips$time <- strptime(car_trips$time, "%Y-%m-%dT%H:%M:%S", tz="UTC")
  return(car_trips)
} 

csv_files = list.files(path = "./csv/", pattern="*.csv", full.names=TRUE)
car_trips = create_car_trips_dataframe(csv_files[8])
