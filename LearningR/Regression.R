rm(list = ls())

launch <- read.csv("Data/challenger.csv")

b <- cov(launch$temperature, launch$distress_ct) / var(launch$temperature)
a <- mean(launch$distress_ct) - b * mean(launch$temperature)

cat("distress_ct = ", a, " + ", b,  " * temperature")

#correlation
r <- cov(launch$temperature, launch$distress_ct) / (sd(launch$temperature) * sd(launch$distress_ct))

print("")
print(r)
print(cor(launch$temperature, launch$distress_ct))

simplePredictor <- function(temperature){
  result <- a + b * temperature
  return(result)
}

print(simplePredictor(40))
print(simplePredictor(60))
print("")

#regression
reg <- function(y, x) {
  x <- as.matrix(x)
  x <- cbind(Intercept = 1, x)
  solve(t(x) %*% x) %*% t(x) %*% y
}

print(reg(y = launch$distress_ct, x = launch$temperature))
print("")
print(reg(y = launch$distress_ct, x = launch[3:5]))

