rm(list=ls())

#data = read.csv("../data/train.csv", header = TRUE)
data = read.csv("../data/temp_train_data.csv", header = TRUE)

# Verify if NaN or Empty factor values exist and write Column names to console
# Gets rid of Empty factors and changes them to most common
for(colName in names(data)){
  isNanCount <- sum(is.na(data[[colName]]))
  
  if (0 < isNanCount){
    print(paste("Column ", colName, "has ", isNanCount, " NaN values."))
  }
  
  if (is.factor(data[[colName]])){
    emptyCount <- sum(as.character(data[[colName]]) == "")
    
    if (0 < emptyCount){
      print(paste("Factor column ", colName, "has ", emptyCount, " empty values."))
      mostCommonFactor <- names(which.max(table(data[[colName]])));
      data[, colName] <- sapply(data[[colName]], function(x){ 
          val <- as.character(x)
          
          if (val == "")
            val <- mostCommonFactor
          
          val
        })
      
      data[, colName] <- as.factor(data[, colName])
    }
  }
  else {
    mostCommonVal <- as.numeric(names(which.max(table(data[[colName]]))))
    
    data[, colName] <- sapply(data[[colName]], function(x){ 
      val <- x
      
      if (is.na(x))
        val <- mostCommonVal
      
      val
    })
  }
}

# Made as Factor from Numeric
data$SalesField5 <- as.factor(data$SalesField5)


# Date conversion. Year, Month, Weekday columns instead of Data
date <- lapply(data$Original_Quote_Date, function(x) { as.Date(as.character(x), format='%Y-%m-%d') })
data <- data[-which(colnames(data)=="Original_Quote_Date")]
data$Weekday <- sapply(date, function(x) { as.POSIXlt(x)$wday })
data$Month <- sapply(date, function(x) { as.integer(format(x, '%m')) })
data$Year <- sapply(date, function(x) { as.integer(format(x, '%Y')) })

# Get rid of two values factors
oneTwoValuesFactorColumns <- sapply(data, function(x) { is.factor(x) && length(table(x)) <= 2 })
for(colName in names(data)[oneTwoValuesFactorColumns]){
  data[, colName] <- as.integer(data[[colName]]) - 1
}

# Investigate all factors 
print(summary(data[sapply(data, function(x) { is.factor(x) })]))

# Get rid of factors by adding columns
factorsCols <- sapply(data, function(x) { is.factor(x) }) 

for(colName in names(data)[factorsCols]){
    for (level in levels(data[[colName]]))
    {
      data[, paste(colName, "_", level, sep = "")] <- as.integer(data[[colName]] == level)
    }
  
    data[, colName] <- NULL
}

# Normalize all columns
range01 <- function(x)
{
  if (min(x) == max(x)){
    return (x - min(x))
  }

  return ((x - min(x)) / (max(x) - min(x)))
}

for(colName in names(data)){
   data[, colName] <- range01(data[, colName])
}

rm("colName")
rm("date")
rm("emptyCount")
rm("isNanCount")
rm("mostCommonFactor")
rm("oneTwoValuesFactorColumns")
rm("factorsCols")
rm("level")

print(names(data))

set.seed(100)
testNums <- sample(nrow(data), size = nrow(data) * 0.33) 

testData <- data[testNums, ]
trainData <- data[-testNums, ]