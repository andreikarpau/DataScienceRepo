import nltk
from nltk.corpus import stopwords


class PreprocessingEngine(object):
    def __init__(self):
        self.tweet_tokenizer = nltk.TweetTokenizer(preserve_case=False)
        self.stop_words = set(stopwords.words('english'))
        #self.stemmer = nltk.SnowballStemmer('english')
        self.stemmer = nltk.PorterStemmer()

        self.custom_stopwords = ['that', 'for', 'in', 'this', 'is', 'of', 'to', 'it', 'and', 'the']
            # ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
            #                      'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
            #                      'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
            #                      'itself', 'they', 'them', 'their', 'theirs', 'themselves',
            #                      'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
            #                      'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            #                      'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
            #                      'if', 'or', 'because', 'as', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
            #                      'between', 'into', 'through', 'during', 'before', 'after', 'to', 'from',
            #                      'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how'
            #                      ]

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

    def tweet_tokenize_custom_stopwords(self, sentence):
        tokens = self.tweet_tokenize_filter(sentence)
        return [element for element in tokens if not element in self.custom_stopwords]

    def tweet_tokenize_stemming_custom_stopwords(self, sentence):
        tokens = self.tweet_tokenize_custom_stopwords(sentence)
        stems = self.stem_tokens(tokens, self.stemmer)
        return stems

    def tweet_tokenize_filter_stopwords(self, sentence):
        tokens = self.tweet_tokenize_filter(sentence)
        return [element for element in tokens if not element in self.stop_words]

    def tweet_tokenize_stemming(self, sentence):
        tokens = self.tweet_tokenize_filter(sentence)
        stems = self.stem_tokens(tokens, self.stemmer)
        return stems

    def tweet_tokenize_stemming_stopwords(self, sentence):
        tokens = self.tweet_tokenize_filter_stopwords(sentence)
        stems = self.stem_tokens(tokens, self.stemmer)
        return stems