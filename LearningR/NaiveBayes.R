rm(list = ls())

library('gmodels')
library('class')
library(tm)
library(wordcloud)
library(e1071)

sms_row <- read.csv('Data/sms_spam.csv', stringsAsFactors = FALSE)
str(sms_row)

sms_row$type <- factor(sms_row$type)
str(sms_row$type)
table(sms_row$type)
sms_corpus <- Corpus(VectorSource(sms_row$text))

print(sms_corpus)
inspect(sms_corpus[1:3])

corpus_clean <- tm_map(sms_corpus, content_transformer(tolower))
corpus_clean <- tm_map(corpus_clean, content_transformer(removeNumbers))
corpus_clean <- tm_map(corpus_clean, content_transformer(removePunctuation))
corpus_clean <- tm_map(corpus_clean, content_transformer(removeWords), stopwords())
corpus_clean <- tm_map(corpus_clean, content_transformer(stripWhitespace))

inspect(corpus_clean[1:3])

sms_dtm <- DocumentTermMatrix(corpus_clean)

sms_train <- sms_row[1:4169,]
sms_test <- sms_row[4170:5559,]

sms_dtm_train <- sms_dtm[1:4169, ]
sms_dtm_test <- sms_dtm[4170:5559, ]

sms_corpus_train <- corpus_clean[1:4169]
sms_corpus_test <- corpus_clean[4170:5559]

prop.table(table(sms_train$type))
prop.table(table(sms_test$type))

wordcloud(sms_corpus_train, min.freq = 50, random.order = FALSE)

spam <- subset(sms_train, type == "spam")
ham <- subset(sms_train, type == "ham")

wordcloud(spam$text, max.words = 40, scale = c(3, 0.5))
wordcloud(ham$text, max.words = 40, scale = c(3, 0.5))

sms_dict <- findFreqTerms(sms_dtm_train, 5)
sms_train_freq <- DocumentTermMatrix(sms_corpus_train, list(dictionary = sms_dict))
sms_test_freq <- DocumentTermMatrix(sms_corpus_test, list(dictionary = sms_dict))

convert_counts <- function(x) {
  ones <- ifelse(x > 0, 1, 0)
  ones <- factor(ones, levels = c(0, 1), labels = c("No", "Yes"))
  return(ones)
}

sms_train1 <- apply(sms_train_freq, MARGIN = 2, convert_counts)
sms_test1 <- apply(sms_test_freq, MARGIN = 2, convert_counts)

sms_classifier <- naiveBayes(sms_train1, sms_train$type)
sms_test_pred <- predict(sms_classifier, sms_test1)
CrossTable(x = sms_test_pred, y = sms_test$type, dnn = c('Predicted', 'Actual'), prop.chisq = FALSE, prop.t = FALSE)


sms_classifier <- naiveBayes(sms_train1, sms_train$type, laplace = 1)
sms_test_pred <- predict(sms_classifier, sms_test1)
CrossTable(x = sms_test_pred, y = sms_test$type, dnn = c('Predicted', 'Actual'), prop.chisq = FALSE, prop.t = FALSE)

