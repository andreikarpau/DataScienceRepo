car_trips <- read.csv("./csv/output/all_trips.csv", stringsAsFactors=FALSE)
car_trips$time <- strptime(car_trips$time, "%Y-%m-%d %H:%M:%S", tz="UTC")

get_non_na_value <- function (value, default_value){
  if (!is.na(value)){
    return(value)
  }else{
    return(default_value)
  }
}

prev_tripid <- car_trips[1,]$trip_id
prev_highway_val <- car_trips[1,]$highway_val
car_trips_length <- length(car_trips[,1])
list_index <- 0

throttle_position_sum <- 0
throttle_position_diff_sum <- 0
time_diff <- 0
trip_items <- 0
speed_sum <- 0
rmp_sum <- 0
rmp_diff_sum <- 0
acc_sum <- 0
decc_sum <- 0
distance_sum <- 0
co2_sum <- 0
intake_temp_sum <- 0
engine_load_sum <- 0

index_v = c()
trip_id_v = c()
highway_v = c()
highway_val_v = c()
car_construction_year_v = c()
car_engine_displ_v = c()
car_fuel_v = c()
car_manufacturer_v = c()
time_type_v = c()
time_light_type_num_v = c()
time_diff_v = c()
throttle_position_avg_v = c()
throttle_position_diff_avg_v = c()
speed_avg_v = c()
rpm_avg_v = c()
rpm_diff_avg_v = c()
acceleration_avg_v = c()
decceleration_avg_v = c()
distance_v = c()
co2_emission_v = c()
cycleway_v = c()
intake_temp_avg_v = c()
engine_load_avg_v = c()

for (i in 2:car_trips_length){
  tr <- car_trips[i,]
  
  if (prev_tripid != tr$trip_id || prev_highway_val != tr$highway_val || i == car_trips_length){
    prev_tr = car_trips[i-1,]
    list_index <- list_index + 1
    
    index_v = c(index_v, list_index)
    trip_id_v = c(trip_id_v, prev_tripid)
    highway_v = c(highway_v, prev_tr$highway)
    highway_val_v = c(highway_val_v, prev_highway_val)
    car_construction_year_v = c(car_construction_year_v, prev_tr$car_construction_year)
    car_engine_displ_v = c(car_engine_displ_v, prev_tr$car_engine_displacement)
    car_fuel_v = c(car_fuel_v, prev_tr$car_fuel_type)
    car_manufacturer_v = c(car_manufacturer_v, prev_tr$car_manufacturer)
    time_type_v = c(time_type_v, prev_tr$time_type)
    time_light_type_num_v = c(time_light_type_num_v, prev_tr$time_light_type_num)
    time_diff_v = c(time_diff_v, time_diff)
    throttle_position_avg_v = c(throttle_position_avg_v, throttle_position_sum/trip_items)
    throttle_position_diff_avg_v = c(throttle_position_diff_avg_v, throttle_position_diff_sum/trip_items)
    speed_avg_v = c(speed_avg_v, speed_sum/trip_items)
    rpm_avg_v = c(rpm_avg_v, rmp_sum/trip_items)
    rpm_diff_avg_v = c(rpm_diff_avg_v, rmp_diff_sum/trip_items)
    acceleration_avg_v = c(acceleration_avg_v, acc_sum/trip_items)
    decceleration_avg_v = c(decceleration_avg_v, decc_sum/trip_items)
    distance_v = c(distance_v, distance_sum)
    co2_emission_v = c(co2_emission_v, co2_sum)
    cycleway_v = c(cycleway_v, prev_tr$cycleway)
    intake_temp_avg_v = c(intake_temp_avg_v, intake_temp_sum/trip_items)
    engine_load_avg_v = c(engine_load_avg_v, engine_load_sum/trip_items)
    
    prev_tripid <- tr$trip_id
    prev_highway_val <- tr$highway_val
    time_diff <- 0
    trip_items <- 0
    throttle_position_sum <- 0
    throttle_position_diff_sum <- 0
    speed_sum <- 0
    rmp_sum <- 0
    rmp_diff_sum <- 0
    acc_sum <- 0
    decc_sum <- 0
    distance_sum <- 0
    co2_sum <- 0
    intake_temp_sum <- 0
    engine_load_sum <- 0
  }
  
  trip_items <- trip_items + 1
  time_diff <- time_diff + tr$time_diff
  
  throttle_position_sum <- throttle_position_sum + get_non_na_value(tr$Throttle.Position_value, 20)
  throttle_position_diff_sum <- throttle_position_diff_sum + abs(get_non_na_value(tr$throttle_diff, 0))
  speed_sum <- speed_sum + get_non_na_value(tr$Speed_value, 40)
  rmp_sum <- rmp_sum + get_non_na_value(tr$Rpm_value, 1600)
  rmp_diff_sum <- rmp_diff_sum + get_non_na_value(abs(tr$rpm_diff), 0)
  distance_sum <- distance_sum + get_non_na_value(tr$distance, 0)
  co2_sum <- co2_sum + tr$co2_emission
  intake_temp_sum <- intake_temp_sum + get_non_na_value(tr$Intake.Temperature_value, 12)
  engine_load_sum <- engine_load_sum + get_non_na_value(tr$Engine.Load_value, 32)
    
  if (0 < tr$acceleration){
    acc_sum <- acc_sum + get_non_na_value(tr$acceleration,0)
  }else{
    decc_sum <- decc_sum + abs(get_non_na_value(tr$acceleration,0))    
  }
}

trips_aggregated <- data.frame(
  index = index_v,
  trip_id = trip_id_v,
  highway = highway_v,
  highway_val = highway_val_v,
  car_construction_year = car_construction_year_v,
  car_engine_displ = car_engine_displ_v,
  car_fuel = car_fuel_v,
  car_manufacturer = car_manufacturer_v,
  time_type = time_type_v,
  time_light_type_num = time_light_type_num_v,
  time_diff = time_diff_v,
  throttle_position_avg = throttle_position_avg_v,
  throttle_position_diff_avg = throttle_position_diff_avg_v,
  speed_avg = speed_avg_v,
  rpm_avg = rpm_avg_v,
  rpm_diff_avg = rpm_diff_avg_v,
  acceleration_avg = acceleration_avg_v,
  decceleration_avg = decceleration_avg_v,
  distance = distance_v,
  cycleway = cycleway_v,
  intake_temp_avg = intake_temp_avg_v,
  engine_load_avg = engine_load_avg_v,
  co2_emission = co2_emission_v
)
write.csv(file="./csv/output/all_aggregated_trips.csv", x=trips_aggregated)

str(trips_aggregated)
summary(trips_aggregated)
