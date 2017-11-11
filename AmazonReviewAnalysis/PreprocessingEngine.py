import nltk
from nltk.corpus import stopwords


class PreprocessingEngine(object):
    def __init__(self):
        self.tweet_tokenizer = nltk.TweetTokenizer(preserve_case=False)
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = nltk.SnowballStemmer("english")

    def stem_tokens(self, tokens, stemmer):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed

    def tweet_tokenize(self, sentence):
        tokens = self.tweet_tokenizer.tokenize(sentence)
        return tokens

    def tweet_tokenize_filter(self, sentence):
        tokens = self.tweet_tokenize(sentence)
        return [element for element in tokens if 1 < len(element)]

    def tweet_tokenize_filter_stopwords(self, sentence):
        tokens = self.tweet_tokenize_filter(sentence)
        return [element for element in tokens if not element in self.stop_words]

    def tweet_tokenize_stemming(self, sentence):
        tokens = self.tweet_tokenize_filter_stopwords(sentence)
        stems = self.stem_tokens(tokens, self.stemmer)
        return stems
