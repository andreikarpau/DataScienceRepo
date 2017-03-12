range01 <- function(x){(x-min(x))/(max(x)-min(x))}

source('ConstructCompData.R')

tubesData <- read.csv("../Data/competition_data/train_set.csv")
tubesInfo <- read.csv("../Data/competition_data/tube.csv")
billOfMaterials <- read.csv("../Data/competition_data/bill_of_materials.csv")

mergeBillFunc <- function(bill, mergeTable, cols, prefix){
  mergeItem <- function(componentIndex){
    
    changeName <- function(index, prefix, postfix){
      namesTable <- names(merged) 
      namesTable[index] <- paste(prefix, namesTable[index], postfix, sep="_")
      namesTable
    }

    component_id_index <- paste("component_id_", componentIndex, sep="")
    quantity_index <- paste("quantity_", componentIndex, sep="")
    
    merged <- merge(x = mergeTable, y = bill[c(component_id_index, "tube_assembly_id", quantity_index)], by.x = c("component_id"), by.y = c(component_id_index))[-1]

    for (i in 1:length(cols)){
      colName = cols[i]
      merged[colName] <- merged[colName] * merged[quantity_index]
    }
  
    for (i in 1:(length(merged)-2)){
      names(merged) <- changeName(i, prefix, componentIndex)
    }
    
    merged[-length(merged)]
  }

  itemCounts <- rep(0, nrow(bill))
  newColsCount = 0;
  
  for (i in 1:8){
    m <- mergeItem(i)
    
    if (nrow(m) <= 0)
      next 
    
    newColsCount <- newColsCount + 1
    
    temp <- merge(x = bill["tube_assembly_id"], y = m, by = "tube_assembly_id", all.x = TRUE)

    itemCounts[!is.na(temp[2])] <- itemCounts[!is.na(temp[2])] + 1
    
    for (i in 2:length(temp)){
      temp[is.na(temp[i]), i] <- 0
    }
    
    if (newColsCount == 1){
      resultTable <- temp
    }
    else {
      for (i in 2:length(temp)){
        resultTable[i] = resultTable[i] + temp[i]
      }
    }
  }
  
  colsNum <- length(cols)
  resultTable[paste(prefix, "count", sep="_")] <- itemCounts
  resultTable
} 

## First cleaning the data

# 1 Try to analyse only tubes where the quantity is 1. 
print(length(unique(tubesData$tube_assembly_id)))
print(sum(tubesData$quantity == 1))
# (Number of such tubes == 7061; Totla number of unique tubes == 8855)

tubesOneOnly <- tubesData[tubesData$quantity == 1, ]

# Very probably that min_order_quantity can also hardly influence the price. Probably it needs 
# to get rid of extra large values here (number of items where min order quantity is bigger than 2
# is 651)
print(sum(2 < tubesOneOnly$min_order_quantity))
tubesQuantityMinOrder <- tubesOneOnly[tubesOneOnly$min_order_quantity <= 2 ,]
# Also possible to get rid from two high cost items and to high min order quantity items
#...

adaptors <- mergeBillFunc(billOfMaterials, adaptorInfo, c("overall_length", "weight"), "adaptor")
bosses <- mergeBillFunc(billOfMaterials, bossInfo, c("height_over_tube", "weight"), "boss")
elbows <- mergeBillFunc(billOfMaterials, elbowInfo, c("overall_length", "weight"), "elbow")
floats <- mergeBillFunc(billOfMaterials, floatInfo, c("bolt_pattern_long", "bolt_pattern_wide", "thickness", "weight"), "float")
hfls <- mergeBillFunc(billOfMaterials, hflInfo, c("hose_diameter", "weight"), "hfl")
nuts <- mergeBillFunc(billOfMaterials, nutInfo, c("length", "thread_pitch", "weight"), "nut")

tubesWithInfo <- merge(x = tubesQuantityMinOrder, y = tubesInfo, by = "tube_assembly_id", all.x = TRUE)
tubesWithInfo <- merge(x = tubesWithInfo, y = adaptors, by = "tube_assembly_id", all.x = TRUE)
tubesWithInfo <- merge(x = tubesWithInfo, y = bosses, by = "tube_assembly_id", all.x = TRUE)
tubesWithInfo <- merge(x = tubesWithInfo, y = elbows, by = "tube_assembly_id", all.x = TRUE)
tubesWithInfo <- merge(x = tubesWithInfo, y = floats, by = "tube_assembly_id", all.x = TRUE)
tubesWithInfo <- merge(x = tubesWithInfo, y = hfls, by = "tube_assembly_id", all.x = TRUE)
tubesWithInfo <- merge(x = tubesWithInfo, y = nuts, by = "tube_assembly_id", all.x = TRUE)

tubesWithInfo$supplier <- NULL
tubesWithInfo$quote_date <- NULL
tubesWithInfo$min_order_quantity <- NULL
tubesWithInfo$bracket_pricing <- NULL
tubesWithInfo$quantity <- NULL
tubesWithInfo$annual_usage <- NULL
tubesWithInfo$end_a_1x <- NULL
tubesWithInfo$end_a_2x  <- NULL
tubesWithInfo$end_x_1x <- NULL
tubesWithInfo$end_x_2x <- NULL

tubesWithInfo$diameter <- range01(tubesWithInfo$diameter)
tubesWithInfo$wall <- range01(tubesWithInfo$wall)
tubesWithInfo$length <- range01(tubesWithInfo$length)
tubesWithInfo$num_bends <- range01(tubesWithInfo$num_bends)
tubesWithInfo$bend_radius <- range01(tubesWithInfo$bend_radius)
tubesWithInfo$num_boss <- range01(tubesWithInfo$num_boss)
tubesWithInfo$num_bracket <- range01(tubesWithInfo$num_bracket)
tubesWithInfo$other <- range01(tubesWithInfo$other)
tubesWithInfo$adaptor_overall_length_1 <- range01(tubesWithInfo$adaptor_overall_length_1)
tubesWithInfo$adaptor_weight_1 <- range01(tubesWithInfo$adaptor_weight_1)
tubesWithInfo$boss_height_over_tube_1 <- range01(tubesWithInfo$boss_height_over_tube_1)
tubesWithInfo$boss_weight_1 <- range01(tubesWithInfo$boss_weight_1)
tubesWithInfo$elbow_overall_length_1 <- range01(tubesWithInfo$elbow_overall_length_1)
tubesWithInfo$elbow_weight_1 <- range01(tubesWithInfo$elbow_weight_1)
tubesWithInfo$float_bolt_pattern_long_1 <- range01(tubesWithInfo$float_bolt_pattern_long_1)
tubesWithInfo$float_bolt_pattern_wide_1 <- range01(tubesWithInfo$float_bolt_pattern_wide_1)
tubesWithInfo$float_thickness_1 <- range01(tubesWithInfo$float_thickness_1)
tubesWithInfo$float_weight_1 <- range01(tubesWithInfo$float_weight_1)
tubesWithInfo$hfl_hose_diameter_3 <- range01(tubesWithInfo$hfl_hose_diameter_3)
tubesWithInfo$hfl_weight_3 <- range01(tubesWithInfo$hfl_weight_3)
tubesWithInfo$nut_length_1 <- range01(tubesWithInfo$nut_length_1)
tubesWithInfo$nut_thread_pitch_1 <- range01(tubesWithInfo$nut_thread_pitch_1)
tubesWithInfo$nut_weight_1 <- range01(tubesWithInfo$nut_weight_1)


tubesWithInfo$adaptor_count <- range01(tubesWithInfo$adaptor_count)
tubesWithInfo$boss_count <- range01(tubesWithInfo$boss_count)
tubesWithInfo$elbow_count <- range01(tubesWithInfo$elbow_count)
tubesWithInfo$float_count <- range01(tubesWithInfo$float_count)
tubesWithInfo$hfl_count <- range01(tubesWithInfo$hfl_count)
tubesWithInfo$nut_count <- range01(tubesWithInfo$nut_count)

print(summary(tubesWithInfo))

set.seed(100)
testNums <- sample(6410, size = 1923)

tubesTestSet <- tubesWithInfo[testNums, ]
tubesTrainSet <- tubesWithInfo[-testNums, ]

#rm(list = c("tubesWithInfo", "tubesQuantityMinOrder", "tubesOneOnly", "tubesData", "tubesInfo", "testNums", "adaptorInfo", "bosses"))