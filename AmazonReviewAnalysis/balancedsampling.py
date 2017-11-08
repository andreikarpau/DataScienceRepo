import json

from helper import FileHelper
import random

texts, titles, rates = FileHelper.read_data_file("data/Grocery_Gourmet_Food.json")

def save_random_sampe(rate_indexes, sample_length, file):
    indexes = random.sample(rate_indexes, sample_length)

    for i in indexes:
        json.dump({'reviewText': texts[i], 'summary': titles[i], 'overall': rates[i]}, file, ensure_ascii=False)
        file.write('\n')

rate1 = []
rate2 = []
rate3 = []
rate4 = []
rate5 = []

for index, item in enumerate(rates):
    if item == 1:
        rate1.append(index)
    elif item == 2:
        rate2.append(index)
    elif item == 3:
        rate3.append(index)
    elif item == 4:
        rate4.append(index)
    elif item == 5:
        rate5.append(index)


with open('data/balanced_sample.json', 'w') as f:
    save_random_sampe(rate1, 500, f)
    save_random_sampe(rate2, 500, f)
    save_random_sampe(rate3, 500, f)
    save_random_sampe(rate4, 500, f)
    save_random_sampe(rate5, 500, f)
