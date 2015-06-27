rm(list = ls())
library(C50)
library(gmodels)
library (ROCR)

credit <- read.csv("/home/askofen/Documents/LearningR/Data/credit.csv", stringsAsFactors = TRUE)
credit$default <- factor(credit$default)

str(credit)
table(credit$checking_balance)
table(credit$savings_balance)
summary(credit$months_loan_duration)
summary(credit$amount)
table(credit$default)

#randomly shuffle the sequence
set.seed(12345)
credit_rand <- credit[order(runif(1000)), ]

head(credit$amount)
head(credit_rand$amount)

credit_train <- credit_rand[1:900, ]
credit_test <- credit_rand[901:1000, ]

prop.table(table(credit_train$default))
prop.table(table(credit_test$default))

credit_model <- C5.0(credit_train[-21], credit_train$default)
summary(credit_model)

credit_pred <- predict(credit_model, credit_test)

CrossTable(credit_test$default, credit_pred,
           prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE,
           dnn = c('actual default', 'predicted default'))

#-------------------------------
#ROCR Analizis
pred1 <- prediction(as.numeric(as.character(credit_test$default)), as.numeric(as.character(credit_pred)));
# Recall-Precision curve             
RP.perf <- performance(pred1, "prec", "rec")
plot (RP.perf)
# ROC curve
ROC.perf <- performance(pred1, "tpr", "fpr")
plot (ROC.perf)
#-------------------------------

credit_boost10 <- C5.0(credit_train[-21], credit_train$default, trials = 10)
credit_boost10
summary(credit_boost10)

credit_boost_pred10 <- predict(credit_boost10, credit_test)
CrossTable(credit_test$default, credit_boost_pred10,
           prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE,
           dnn = c('actual default', 'predicted default'))


# Cost matrix use
#-------------------------------------------
error_cost = matrix(c(0,1,4,0), nrow = 2)
credit_cost <- C5.0(credit_train[-21], credit_train$default, costs = error_cost)
credit_cost_pred <- predict(credit_cost, credit_test)
CrossTable(credit_test$default, credit_cost_pred,
           prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE,
           dnn = c('actual default', 'predicted default'))