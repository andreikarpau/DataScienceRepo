library(DAAG)
library(relaimpo)
library(glmnet)

mean_sq_error <- function(actual, predict) { sum((actual - predict)^2)/length(predict) }
calculate_R2 <- function(actual, predict){
  return(1 - (sum((actual-predict)^2)/sum((actual-mean(actual))^2)))
} 
calculate_R2_obj <- function(r2, n, p) {return(1 - (1-r2)*(n-1)/(n-p-1))}

trips_reg <- read.csv("./csv/output/car_trips_minmax.csv")
trips_reg$X <- NULL

co2_reg_formula <-  formula(co2_emission_per_dist ~ throttle_position_diff_avg + 
                              car_construction_year + speed_avg + 
                              rpm_avg + acceleration_avg + deceleration_avg + engine_load_diff_avg +
                              car_engine_displ + intake_pressure_avg +
                              car_manufacturer + distance + time_type + highway_val + time_diff + lit + rpm_diff_avg +  
                              throttle_position_avg + intake_temp_avg + engine_load_avg)

# simple linear regression estimation
lm_model <- lm(data=trips_reg, formula = co2_reg_formula)

#metrics <- calc.relimp(lm_model, type = c("lmg", "first", "last"), rela=TRUE)
#print(metrics)

run_cross_validation <- function(formula){
  # k-fold cross-validation
  regression_res <- cv.lm(data = trips_reg, m = 10, seed = 29, plotit = FALSE,
                        form.lm = formula)
  
  attr(regression_res, 'ms')
  attr(regression_res, 'df')
  print(mean_sq_error(regression_res$co2_emission_per_dist, regression_res$cvpred))
  r2 <- calculate_R2(regression_res$co2_emission_per_dist, regression_res$cvpred)
  print(r2)
  print(calculate_R2_obj(r2, length(regression_res$cvpred), length(lm_model$coefficients)-1))
}

co2_reg_formula_cv <- formula(co2_emission_per_dist ~ speed_avg + 
                             car_construction_year + throttle_position_diff_avg + 
                             rpm_avg + acceleration_avg + deceleration_avg + engine_load_diff_avg +
                             car_engine_displ + intake_pressure_avg +
                             car_manufacturer + #distance + time_type + highway_val + time_diff + lit + rpm_diff_avg +  
                             throttle_position_avg + intake_temp_avg + engine_load_avg)

run_cross_validation(co2_reg_formula_cv)

# simple linear regression summary
lm_model <- lm(data=trips_reg, formula = co2_reg_formula_cv)
summary(lm_model)
#-----------------------------------------------------
set.seed(29)

formula <- formula(co2_emission_per_dist ~ .)
data <- trips_reg[,c("co2_emission_per_dist","speed_avg","car_construction_year", "throttle_position_diff_avg",
                     "rpm_avg", "acceleration_avg", "deceleration_avg", "engine_load_diff_avg", "car_engine_displ",
                     "intake_pressure_avg", "car_manufacturer", "throttle_position_avg", "intake_temp_avg", "engine_load_avg")]
data <- cbind(data, model.matrix( ~ 0 + car_manufacturer, data))
data$car_manufacturer <- NULL

fit.lasso <- glmnet(x = as.matrix(data[-1]), y = as.matrix(data[1]), alpha=1, family="gaussian")
fit.ridge <- glmnet(x = as.matrix(data[-1]), y = as.matrix(data[1]), alpha=0, family="gaussian")

plot(fit.lasso, xvar="lambda")
plot(fit.ridge, xvar="lambda")

fit.lasso.cv <- cv.glmnet(x = as.matrix(data[-1]), y = as.matrix(data[1]), type.measure="mse", alpha=1, family="gaussian")
fit.ridge.cv <- cv.glmnet(x = as.matrix(data[-1]), y = as.matrix(data[1]), type.measure="mse", alpha=0, family="gaussian")

fit.lasso.cv$lambda.min.index <- which(fit.lasso.cv$lambda == fit.lasso.cv$lambda.min)
fit.lasso.cv$mse.min <- fit.lasso.cv$cvm[fit.lasso.cv$lambda.min.index]
fit.lasso.cv$coefs <- fit.lasso.cv$glmnet.fit$beta[, fit.lasso.cv$lambda.min.index]

fit.ridge.cv$lambda.min.index <- which(fit.ridge.cv$lambda == fit.ridge.cv$lambda.min)
fit.ridge.cv$mse.min <- fit.ridge.cv$cvm[fit.ridge.cv$lambda.min.index]
fit.ridge.cv$coefs <- fit.ridge.cv$glmnet.fit$beta[, fit.ridge.cv$lambda.min.index]


print(paste("LASSO Lambda:", fit.lasso.cv$lambda.min, " MSE:", fit.lasso.cv$mse.min,  sep = " "))
print(paste("Ridge Lambda:", fit.ridge.cv$lambda.min, " MSE:", fit.ridge.cv$mse.min,  sep = " "))

coef(fit.lasso.cv, s=fit.lasso.cv$lambda.min)

#-----------------------------------------------------
nrows <- nrow(data)
size <- floor(nrows * 0.3)
k <- 10;
set.seed(29)

for (i in 1:k){
  test_indexes <- sample(nrows, size = size)  

  train_sample <- data[-test_indexes,]
  test_sample <- data[test_indexes,] 
}






