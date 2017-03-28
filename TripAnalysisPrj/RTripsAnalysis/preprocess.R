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
    if (is.na(one_way) || nchar(one_way)==0) {
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
  
  car_trips <- car_trips[, !(names(car_trips) %in% c("Throttle.Position_unit", "Speed_unit", "Rpm_unit",
    "Voltage_unit", "ER_unit", "MAF_unit", "Intake.Temperature_unit", "Intake.Pressure_unit", "GPS.VDOP_value", 
    "GPS.VDOP_unit", "GPS.Speed_unit", "GPS.PDOP_value", "GPS.PDOP_unit", "GPS.HDOP_value", "GPS.HDOP_unit", 
    "GPS.Bearing_value", "GPS.Bearing_unit", "GPS.Altitude_value", "GPS.Altitude_unit", "GPS.Accuracy_value", "GPS.Accuracy_unit",
    "O2.Lambda.Voltage_unit", "O2.Lambda.Voltage.ER_unit", "Engine.Load_unit", "Calculated.MAF_unit", "Consumption_unit",
    "CO2_unit", "FIXME", "access.lanes", "access.lanes.forward", "alt_name", "bridge.structure", "area", "bus",
    "bus.lanes", "bus.lanes.forward", "cycleway.both", "fixed", "frequency", "gauge", "lit_by_gaslight", "loc_name",
    "local_ref", "maxaxleload", "maxspeed.conditional", "name.de", "old_name", "psv.lanes", "psv.lanes.forward", "public_transport",
    "ref.IFOPT", "ref_old", "wheelchair", "width", "road_name", "tmc", "right.sloped_curb", "proposed",
    "placement.backward", "parking.lane.right", "wikidata", "wikipedia", "traffic_calming", "parking.lane.both",
    "parking.lane.left", "parking.condition.both.1", "parking.condition.both.1.residents", "parking.condition.both.2",
    "parking.condition.both.2.ticket", "parking.condition.left.1", "parking.condition.left.1.maxstay", "parking.condition.left.1.residents",
    "parking.condition.left.1.ticket", "parking.condition.left.1.time_interval", "parking.condition.left.2", "parking.condition.left.2.ticket",
    "parking.condition.left.2.time_interval", "parking.condition.left.3", "parking.condition.left.3.time_interval",
    "parking.condition.left.3.residents", "footway", "footway.left.sloped_curb.end", "footway.left.sloped_curb.start",
    "footway.left.wheelchair", "footway.left.wheelchair.end", "footway.left.wheelchair.start", "footway.left.incline",
    "footway.left.smoothness", "footway.left.surface", "footway.left.width", "footway.right.sloped_curb.end",
    "footway.right.sloped_curb.start", "footway.right.incline", "footway.right.smoothness", "footway.right.surface", 
    "history", "left.sloped_curb", "maxspeed.wet", "destination.lanes.forward", "destination.ref", "destination.ref.lanes",
    "destination.symbol.lanes", "fixme", "class.bicycle", "bicycle.left", "bdouble"))]
  
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
