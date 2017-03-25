replace_na_by_value <- function(list, value){
  if (class(list) == "character") {
    list[nchar(list)==0] <- value
    return(list)
  }
  
  list <- value
  return(list)
}

create_car_trips_dataframe <- function(csv_file_name){
  car_trips = read.csv(csv_file_name, stringsAsFactors=FALSE)
  car_trips$time <- strptime(car_trips$time, "%Y-%m-%dT%H:%M:%S", tz="UTC")
  car_trips <- car_trips[with(car_trips, order(time, trip_id)), ] 
  
  car_trips$measure_index <- NULL
  #car_trips$date <- as.Date(as.POSIXct(car_trips$time, 'GMT'))
  
  car_trips$Acceleration = 0
  car_trips$Throttle.Position_unit <- NULL
  car_trips$Speed_unit <- NULL
  car_trips$Rpm_unit <- NULL
  car_trips$Voltage_unit <- NULL
  car_trips$ER_unit <- NULL
  car_trips$MAF_unit <- NULL
  car_trips$Intake.Temperature_unit <- NULL
  car_trips$Intake.Pressure_unit <- NULL
  car_trips$GPS.VDOP_value <- NULL
  car_trips$GPS.VDOP_unit <- NULL
  car_trips$GPS.Speed_unit <- NULL
  car_trips$GPS.PDOP_value <- NULL
  car_trips$GPS.PDOP_unit <- NULL
  car_trips$GPS.HDOP_value <- NULL
  car_trips$GPS.HDOP_unit <- NULL
  car_trips$GPS.Bearing_value <- NULL
  car_trips$GPS.Bearing_unit <- NULL
  car_trips$GPS.Altitude_value <- NULL
  car_trips$GPS.Altitude_unit <- NULL
  car_trips$GPS.Accuracy_value <- NULL
  car_trips$GPS.Accuracy_unit <- NULL
  car_trips$O2.Lambda.Voltage_unit <- NULL
  car_trips$O2.Lambda.Voltage.ER_unit <- NULL
  car_trips$Engine.Load_unit <- NULL
  car_trips$Calculated.MAF_unit <- NULL
  car_trips$Consumption_unit <- NULL

  car_trips$CO2_unit <- NULL
  car_trips$FIXME <- NULL
  car_trips$access.lanes <- NULL
  car_trips$access.lanes.forward <- NULL
  car_trips$alt_name <- NULL
  car_trips$area <- NULL
  car_trips$bridge.structure <- NULL
  car_trips$bus <- NULL
  car_trips$bus.lanes <- NULL
  car_trips$bus.lanes.forward <- NULL
  car_trips$cycleway.both <- NULL
  car_trips$fixed <- NULL
  car_trips$frequency <- NULL
  car_trips$gauge <- NULL
  car_trips$lit_by_gaslight <- NULL
  car_trips$loc_name <- NULL
  car_trips$local_ref <- NULL
  car_trips$maxaxleload <- NULL
  car_trips$maxspeed.conditional <- NULL
  car_trips$name.de <- NULL
  car_trips$old_name <- NULL
  car_trips$psv.lanes <- NULL
  car_trips$psv.lanes.forward <- NULL
  car_trips$public_transport <- NULL
  car_trips$ref.IFOPT <- NULL
  car_trips$ref_old <- NULL
  car_trips$wheelchair <- NULL
  car_trips$width <- NULL

  car_trips$cycleway <- replace_na_by_value(car_trips$cycleway, "no")
  car_trips$oneway <- replace_na_by_value(car_trips$oneway, "no")
  car_trips$lit <- replace_na_by_value(car_trips$lit, "no")
  car_trips$surface <- replace_na_by_value(car_trips$surface, "asphalt")
  
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
car_trips = create_car_trips_dataframe(csv_files[4])
summary(car_trips)