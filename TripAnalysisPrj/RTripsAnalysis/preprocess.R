replace_na_by_value <- function(list, value){
  if (class(list) == "character") {
    list[nchar(list)==0] <- value
    return(list)
  }
  
  list <- value
  return(list)
}

get_highway_info <- function(car_trips){
  highway_info <- lapply(1:nrow(car_trips), function(i) {
    tr <- car_trips[i,]
    highway_val <- 0
    one_way_def <- "no"
    lanes_def <- 2
    max_speed_def <- 50
    highway <- tr$highway
    
    if (grepl("motorway", tr$highway)){
      highway_val <- 9
      one_way_def <- "yes"
      max_speed_def <- 300
      highway <- "motorway"
    }else if (grepl("trunk", tr$highway)) {
      highway_val <- 8  
      one_way_def <- "yes"
      max_speed_def <- 300
      highway <- "trunk"
    }else if (grepl("primary", tr$highway)) {
      highway_val <- 7  
      max_speed_def <- 100
      highway <- "primary"
    }else if (grepl("secondary", tr$highway)) {
      highway_val <- 6  
      max_speed_def <- 100
      highway <- "secondary"
    }else if (grepl("tertiary", tr$highway)) {
      highway_val <- 5  
      max_speed_def <- 100
      highway <- "tertiary"
    }else if (grepl("unclassified", tr$highway)) {
      highway_val <- 4    
      max_speed_def <- 100
      highway <- "unclassified"
    }else if (grepl("residential", tr$highway)) {
      highway_val <- 3
      highway <- "residential"
    }else if (grepl("service", tr$highway)) {
      highway_val <- 2
      highway <- "service"
    } else {
      highway_val <- 1
      max_speed_def <- 30
      highway <- "small_street"
    }
    
    one_way <- tr$oneway
    if (nchar(one_way)==0) {
      one_way <- one_way_def
    }
    if (grepl("-1", one_way)){
      one_way <- "yes"
    }
    
    lanes <- tr$lanes
    if (is.na(lanes)){
      lanes <- lanes_def
    }
    
    maxspeed <- tr$maxspeed
    if (nchar(maxspeed)==0 || is.na(maxspeed)){
      maxspeed <- max_speed_def
    }
    if (grepl("none", maxspeed)){
      maxspeed <- 300
    }
    
    road_overview <- tr$time_light_type_num
    if (road_overview < 1 && grepl("yes", tr$lit)) {
      road_overview = 1
    }
    
    return(list(index=i, highway_val=highway_val, lanes=lanes, one_way=one_way, maxspeed=maxspeed, 
                road_overview=road_overview, highway=highway))
  })
  highway_info <- do.call(rbind, highway_info)
  return(highway_info)
}

create_car_trips_dataframe <- function(csv_file_name){
  car_trips = read.csv(csv_file_name, stringsAsFactors=FALSE)
  
  trip_time <- strptime(car_trips$time, "%Y-%m-%dT%H:%M:%S", tz="UTC")
  if (is.na(trip_time[1])){
    trip_time <- strptime(car_trips$time, "%Y-%m-%d %H:%M:%S", tz="UTC")
  }
  car_trips$time <- trip_time
  
  car_trips <- car_trips[with(car_trips, order(trip_id, time)), ] 
  
  car_trips$measure_index <- NULL
  #car_trips$date <- as.Date(as.POSIXct(car_trips$time, 'GMT'))
  
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
  car_trips$road_name <- NULL
  
  car_trips$cycleway <- replace_na_by_value(car_trips$cycleway, "no")
  car_trips$lit <- replace_na_by_value(car_trips$lit, "no")
  car_trips$surface <- replace_na_by_value(car_trips$surface, "asphalt")
  
  car_trips$acceleration = 0
  car_trips$throttle_diff = 0
  car_trips$distance = 0
  car_trips$time_diff = 0
  car_trips$rpm_diff = 0
  
  for (i in 1:(length(car_trips$Speed_value) - 1)){
    next_i = i + 1
    
    if (car_trips$trip_id[next_i] == car_trips$trip_id[i]){
      time_diff = as.numeric(car_trips$time[next_i] - car_trips$time[i], units="hours")

      if (0 < time_diff){
        speed_diff = car_trips$Speed_value[next_i] - car_trips$Speed_value[i]
        acceleration = speed_diff/time_diff
        
        car_trips$time_diff[i] = time_diff
        car_trips$acceleration[i] = acceleration
        car_trips$distance[i] = car_trips$Speed_value[i] * time_diff + acceleration * time_diff * time_diff / 2 
        car_trips$throttle_diff[i] = car_trips$Throttle.Position_value[next_i] - car_trips$Throttle.Position_value[i]
        car_trips$rpm_diff[i] = car_trips$Rpm_value[next_i] - car_trips$Rpm_value[i]
      }
    }
  }
  
  hi <- get_highway_info(car_trips)
  car_trips$maxspeed <- rapply(hi[,"maxspeed"],c)
  car_trips$lanes <- rapply(hi[,"lanes"],c)
  car_trips$oneway <- rapply(hi[,"one_way"],c)
  car_trips$highway_val <- rapply(hi[,"highway_val"],c)
  car_trips$road_overview <- rapply(hi[,"road_overview"],c)
  car_trips$highway <- rapply(hi[,"highway"],c)
  
  car_trips$co2_emission <- car_trips$time_diff * car_trips$CO2_value
    
  return(car_trips)
} 

csv_files <- list.files(path = "./csv/", pattern="*.csv", full.names=TRUE)
all_trips <- create_car_trips_dataframe(csv_files[1])
for (i in 2:length(csv_files)){
  car_trips <- create_car_trips_dataframe(csv_files[i])
  if (0 < sum(is.na(car_trips$CO2_value))){
    print(paste("No CO2 Values: ", car_trips$car_manufacturer[1], car_trips$car_model[1], " "))
  }else{
    all_trips <- rbind(all_trips, car_trips)
  }
}
write.csv(file="./csv/output/all_trips.csv", x=all_trips)

summary(all_trips)
