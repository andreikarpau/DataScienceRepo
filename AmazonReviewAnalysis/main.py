from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from MeanEmbeddingVectorizer import MeanEmbeddingVectorizer
from PreprocessingEngine import PreprocessingEngine
from helper import FileHelper
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfVectorizer
from sklearn.model_selection import GroupShuffleSplit, StratifiedShuffleSplit
from nltk.stem.snowball import SnowballStemmer

texts, summaries, overalls = FileHelper.get_sample_data_rates()

rates = [3 < val for val in overalls]
#rates = overalls

preprocessingEngine = PreprocessingEngine()

#vectorizer = CountVectorizer(tokenizer=preprocessingEngine.tweet_tokenize_filter, ngram_range=(1, 2), min_df=3)
vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=3)
#vectorizer = HashingVectorizer(tokenizer=preprocessingEngine.tweet_tokenize_stemming_custom_stopwords, ngram_range=(1, 2), norm='l2', alternate_sign=False)
#vectorizer = TfidfVectorizer(sublinear_tf=True, tokenizer=preprocessingEngine.tweet_tokenize_filter, ngram_range=(1, 2))
# vectorizer = MeanEmbeddingVectorizer(FileHelper.read_word2vec())

# analyzer = vectorizer.build_analyzer()

#classifier = MultinomialNB()
#classifier = LinearSVC(dual=False)
#classifier = RandomForestClassifier(n_estimators=10)
classifier = LogisticRegression()
#classifier = LogisticRegression(solver='lbfgs')


k_folds = StratifiedShuffleSplit(n_splits=5, test_size=0.1, random_state=345)

accuracy = []
prf_array = []

clf = None

iteration = 0

for train_index, test_index in k_folds.split(texts, rates):
    iteration = iteration + 1

    x_train = [texts[i] for i in train_index]
    y_train = [rates[i] for i in train_index]

    x_test = [texts[i] for i in test_index]
    y_test = [rates[i] for i in test_index]

    x_train_vectorized = vectorizer.fit_transform(x_train)
    clf = classifier.fit(x_train_vectorized, y_train)

    x_test_vectorized = vectorizer.transform(x_test)
    predicted = clf.predict(x_test_vectorized)

    a_score = accuracy_score(y_pred=predicted, y_true=y_test)
    prf = precision_recall_fscore_support(y_pred=predicted, y_true=y_test, average='binary')

    accuracy.append(a_score)
    prf_array.append(prf)

    print("Accuracy iteration {0}: {1}; Precision, recall, F score: {2}".format(iteration, a_score, prf))
    print(a_score)

num_iterations = len(accuracy)
total_accuracy = sum(accuracy) / num_iterations

sum_precision = 0
sum_recall = 0
sum_f_score = 0

for item in prf_array:
    sum_precision = sum_precision + item[0]
    sum_recall = sum_recall + item[1]
    sum_f_score = sum_f_score + item[2]

print("-----------------------------------------")
print("Accuracy: {0}".format(total_accuracy))
print("Precision: {0}".format(sum_precision/num_iterations))
print("Recall: {0}".format(sum_recall/num_iterations))
print("F-score: {0}".format(sum_f_score/num_iterations))
FileHelper.print_top10(vectorizer, clf, ["Top Tokens"])
print("-----------------------------------------")
