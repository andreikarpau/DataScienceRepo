import nltk
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from MeanEmbeddingVectorizer import MeanEmbeddingVectorizer
from helper import FileHelper
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfVectorizer
from sklearn.model_selection import GroupShuffleSplit, StratifiedShuffleSplit
from nltk.stem.snowball import SnowballStemmer


#########################################################
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


stemmer = SnowballStemmer("english")


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


#########################################################

# texts, _, rates = FileHelper.read_data_file("data/Short_Data.json")
texts, _, rates = FileHelper.read_data_file("data/Grocery_Gourmet_Food.json", max_num=1000)

rates = [3 < val for val in rates]

# vectorizer = CountVectorizer(tokenizer=tokenize)
vectorizer = CountVectorizer(stop_words='english')
# vectorizer = HashingVectorizer(stop_words='english', alternate_sign=False)
# vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words='english')
# vectorizer = MeanEmbeddingVectorizer(FileHelper.read_word2vec())

# analyzer = vectorizer.build_analyzer()

classifier = MultinomialNB()
# classifier = LinearSVC()
# classifier = RandomForestClassifier(n_estimators=10)
# classifier = LogisticRegression()
# classifier = LogisticRegression(multi_class='multinomial', solver='lbfgs')


k_folds = StratifiedShuffleSplit(n_splits=5, test_size=0.3, random_state=345)

accuracy = []
prf_array = []

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

total_accuracy = sum(accuracy) / len(accuracy)
print("Accuracy: ")
print(total_accuracy)
