rm(list = ls())

library('gmodels')
library('class')

# Text mining
library(tm)
library(wordcloud)
library(e1071)

#Loading And Analyzing Data 
sms_row <- read.csv('Data/sms_spam.csv', stringsAsFactors = FALSE)
str(sms_row)

sms_row$type <- factor(sms_row$type)
str(sms_row$type)
table(sms_row$type)

wordcloud(sms_row$text, min.freq = 50, random.order = FALSE)
wordcloud(subset(sms_row, type == "spam")$text, max.words = 40, scale = c(3, 0.5))
wordcloud(subset(sms_row, type == "ham")$text, max.words = 40, scale = c(3, 0.5))

#Data Preprocessing
corpus_clean <- Corpus(VectorSource(sms_row$text)) #not yet clean!!!

inspect(sms_corpus[1:3])
print(sms_corpus[[1]]$content)

corpus_clean <- tm_map(sms_corpus, content_transformer(tolower))
corpus_clean <- tm_map(corpus_clean, content_transformer(removeNumbers))
corpus_clean <- tm_map(corpus_clean, content_transformer(removePunctuation))
corpus_clean <- tm_map(corpus_clean, content_transformer(removeWords), stopwords())
corpus_clean <- tm_map(corpus_clean, content_transformer(stripWhitespace))

inspect(corpus_clean[1:3])
print(corpus_clean[[1]]$content)

sms_corpus_train <- corpus_clean[1:4169]
sms_corpus_test <- corpus_clean[4170:5559]

# Find frequent words in TrainSet
sms_dict <- findFreqTerms(DocumentTermMatrix(sms_corpus_train), 5)

sms_train_freq <- DocumentTermMatrix(sms_corpus_train, list(dictionary = sms_dict))
sms_test_freq <- DocumentTermMatrix(sms_corpus_test, list(dictionary = sms_dict))

convert_counts <- function(x) {
  ones <- ifelse(x > 0, 1, 0)
  ones <- factor(ones, levels = c(0, 1), labels = c("No", "Yes"))
  return(ones)
}

sms_train1 <- apply(sms_train_freq, MARGIN = 2, convert_counts)
sms_test1 <- apply(sms_test_freq, MARGIN = 2, convert_counts)

sms_train <- sms_row[1:4169,]
sms_test <- sms_row[4170:5559,] 

# Build classifier
sms_classifier <- naiveBayes(sms_train1, sms_train$type)

# Test classifier
sms_test_pred <- predict(sms_classifier, sms_test1)

head(sms_test_pred)
CrossTable(x = sms_test_pred, y = sms_test$type, dnn = c('Predicted', 'Actual'), prop.chisq = FALSE, prop.t = FALSE, prop.r = FALSE)

# Improve classifier
sms_classifier <- naiveBayes(sms_train1, sms_train$type, laplace = 1)

# Test classifier
sms_test_pred <- predict(sms_classifier, sms_test1)
CrossTable(x = sms_test_pred, y = sms_test$type, dnn = c('Predicted', 'Actual'), prop.chisq = FALSE, prop.t = FALSE, prop.r = FALSE)