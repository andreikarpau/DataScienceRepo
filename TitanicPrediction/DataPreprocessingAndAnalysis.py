import numpy as np
import csv as csv
import pandas as pd
import pylab as P
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Analyze data set
csv_file_reader = csv.reader(open('Data/train.csv', 'rb'))
header = csv_file_reader.next()

data = []

for line in csv_file_reader:
    data.append(line)

data = np.array(data)

number_passengers = np.size(data[0::,1].astype(np.float))
number_survived = np.sum(data[0::,1].astype(np.float))

women_only_stats = data[0::, 4] == "female"
men_only_stats = data[0::, 4] == "male"

woman_survived_stats = data[women_only_stats,1].astype(np.float)
man_survived_stats = data[men_only_stats,1].astype(np.float)

proportion_woman_survivors = sum(woman_survived_stats) / np.size(woman_survived_stats)
proportion_man_survivors = sum(man_survived_stats) / np.size(man_survived_stats)
proportion_survivors = number_survived / number_passengers

# Use pandas
df = pd.read_csv('Data/train.csv', header=0)

print df.head(3)
print df.dtypes
print df.info()
print df.describe()

print df.Age.mean()
print df.Age.median()

print  df[df['Age'] > 60][['Sex', 'Pclass', 'Age', 'Survived']]
print  df[df['Age'].isnull()][['Sex', 'Pclass', 'Age', 'Survived']]

df['Age'].hist()
P.show()

df['Age'].dropna().hist(bins=16, range=(0,80), alpha = .5)
P.show()

df['Gender'] = df['Sex'].map( {'female': 0, 'male': 1} ).astype(int)

median_ages = np.zeros((2,3))

for i in range(0, 2):
    for j in range(0, 3):
        median_ages[i,j] = df[(df['Gender'] == i) & (df['Pclass'] == j+1)]['Age'].dropna().median()

print median_ages

df['AgeFill'] = df['Age']

for i in range(0, 2):
    for j in range(0, 3):
        df.loc[ (df.Age.isnull()) & (df.Gender == i) & (df.Pclass == j+1), 'AgeFill'] = median_ages[i,j]

print df[ df['Age'].isnull() ][['Gender','Pclass','Age','AgeFill']].head(10)

df['AgeIsNull'] = pd.isnull(df.Age).astype(int)
df['FamilySize'] = df['SibSp'] + df['Parch']
df['AgeFill*Class'] = df.AgeFill * df.Pclass

print df.dtypes[df.dtypes.map(lambda x: x=='object')]

df = df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked'], axis=1)
df = df.drop(['Age'], axis=1)
df = df.drop(['PassengerId'], axis=1)

mask = np.random.rand(len(df)) < 0.8
df_train = df[mask]
df_test = df[~mask]

train_data = df_train.values
test_data_results = df_test['Survived'].values

df_test = df_test.drop(['Survived'], axis=1)
test_data = df_test.values

print train_data
print test_data
print test_data_results


#Create Random Forest Classifier
forest = RandomForestClassifier(n_estimators = 100)
forest = forest.fit(train_data[0::,1::],train_data[0::,0])

output = forest.predict(test_data)

true_positive = sum((output + test_data_results) == 2)
true_negative = sum((output + test_data_results) == 0)
false_positive = sum((test_data_results - output) == 1)
false_negative = sum((test_data_results - output) == -1)

print '                     Predicted positive    Predicted negative'
print 'Condition positive:   ' + str(true_positive) + '                    ' + str(false_negative)
print 'Condition negative:   ' + str(false_positive) + '                    ' + str(true_negative)

print 'accurancy'
print accuracy_score(output, test_data_results)