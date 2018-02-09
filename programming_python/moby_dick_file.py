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

        print("Bag of words (moby dick text) size: {}".format(len(bag)))
        return bag


def most_frequent_words(bag, top_num=10):
    pass

bag_of_words()