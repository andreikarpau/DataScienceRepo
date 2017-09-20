library(DAAG)

mean_sq_error <- function(actual, predict) { sum((actual - predict)^2)/length(predict) }
calculate_R2 <- function(actual, predict){
  return(1 - (sum((actual-predict)^2)/sum((actual-mean(actual))^2)))
} 
calculate_R2_obj <- function(r2, n, p) {return(1 - (1-r2)*(n-1)/(n-p-1))}

trips_reg <- read.csv("./csv/output/car_trips_minmax.csv")
trips_reg$X <- NULL

co2_reg_formula <- formula(co2_emission_per_dist ~ throttle_position_diff_avg + 
  car_construction_year + speed_avg +
  rpm_avg + rpm_diff_avg + acceleration_avg + decceleration_avg +
  car_engine_displ + time_light_type_num +
  car_manufacturer + highway_val + #highway + time_type
  throttle_position_avg + intake_temp_avg + engine_load_avg)

# simple linear regression estimation
lm_model <- lm(data=trips_reg, formula = co2_reg_formula)

# k-fold cross-validation
regression_res <- cv.lm(data = trips_reg, m = 10, seed = 29, plotit = FALSE,
                        form.lm = co2_reg_formula)

attr(regression_res, 'ms')
attr(regression_res, 'df')
print(mean_sq_error(regression_res$co2_emission_per_dist, regression_res$cvpred))
r2 <- calculate_R2(regression_res$co2_emission_per_dist, regression_res$cvpred)
print(r2)
print(calculate_R2_obj(r2, length(regression_res$cvpred), length(lm_model$coefficients)-1))

# simple linear regression summary
summary(lm_model)
