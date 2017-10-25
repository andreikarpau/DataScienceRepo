from helper import FileHelper
from sklearn.feature_extraction.text import CountVectorizer

texts, _, rates = FileHelper.read_data_file("data/Short_Data.json")

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

vocabulary = vectorizer.vocabulary_

print(X)