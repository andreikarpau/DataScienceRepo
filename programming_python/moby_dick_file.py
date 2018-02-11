import re


def bag_of_words(filename="./data/moby_dick.txt"):
    with open(filename, "r", encoding="utf8") as f:
        bag = {}
        for line in f:
            words = re.findall("\w*", line)
            for w in words:
                if len(w) <= 0:
                    continue

                if w in bag:
                    bag[w] += 1
                else:
                    bag[w] = 1

        return bag


def bag_of_bigramms(filename="./data/moby_dick.txt"):
    with open(filename, "r", encoding="utf8") as f:
        bag = {}
        prev_word = None

        for line in f:
            words = re.findall("\w*", line)
            for w in words:
                if len(w) <= 0:
                    continue

                if prev_word is None or len(prev_word) <= 0:
                    prev_word = w
                    continue

                bigramm = "{} {}".format(prev_word, w)
                prev_word = w

                if bigramm in bag:
                    bag[bigramm] += 1
                else:
                    bag[bigramm] = 1

        return bag


def most_frequent_words(bag):
    values = list(bag.values())
    top_index = values.index(max(values))
    return list(bag.keys())[top_index]


def word_conditional_probability(bag_words, bag_bigramms, prev_word = "The", word = "Whale"):
    num_words = sum(bag_words.values())
    p_prev_word = bag_words[prev_word] / num_words

    num_bigramms = sum(bag_bigramms.values())
    p_bigramm = bag_bigramms["{} {}".format(prev_word, word)] / num_bigramms

    return p_bigramm / p_prev_word

bag_words = bag_of_words()
print("Bag of words (moby dick text) size: {}".format(len(bag_words)))

top_word = most_frequent_words(bag_words)
print("Most frequent word: {}; count: {}".format(top_word, bag_words[top_word]))

bag_bigramms = bag_of_bigramms()
print("Bag of bigramms (moby dick text) size: {}".format(len(bag_bigramms)))

p_prev_word = word_conditional_probability(bag_words, bag_bigramms, "with", "this")
print("Probability of word <{}> after word <{}> is: {}".format("this", "with", p_prev_word))
