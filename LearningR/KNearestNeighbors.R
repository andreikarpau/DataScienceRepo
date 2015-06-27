rm(list = ls())

library('gmodels')
library('class')

normalize <- function(x){
  return ((x - min(x)) / (max(x) - min(x)))
}

wbcd <- read.csv("/home/askofen/Documents/LearningR/Data/wisc_bc_data.csv", stringsAsFactors = FALSE)

wbcd$diagnosis <- factor(wbcd$diagnosis, levels = c("B", "M"), labels = c("Benign", "Malignant"))
wbcd = wbcd[2:32]
#wbcd_n <- as.data.frame(lapply(wbcd[2:31], normalize))
wbcd_n <- as.data.frame(lapply(wbcd[2:31], normalize))
wbcd_train <- wbcd_n[1:469, ]
wbcd_test <- wbcd_n[470:569, ]
wbcd_train_label <- wbcd[1:469, 1]
wbcd_test_label <- wbcd[470:569, 1]
wbcd_test_pred <- knn(train = wbcd_train, test = wbcd_test, cl = wbcd_train_label, k=21)
CrossTable(x = wbcd_test_label, y = wbcd_test_pred, prop.chisq=FALSE)


wbcd_z = as.data.frame(scale(wbcd[-1]))

wbcd_train <- wbcd_z[1:469, ]
wbcd_test <- wbcd_z[470:569, ]
wbcd_test_pred <- knn(train = wbcd_train, test = wbcd_test, cl = wbcd_train_label, k=21)
CrossTable(x = wbcd_test_label, y = wbcd_test_pred, prop.chisq=FALSE)
