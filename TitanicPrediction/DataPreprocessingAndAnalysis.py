import numpy as np
import csv as csv
import pandas as pd
import pylab as P
from sklearn.ensemble import RandomForestClassifier

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

train_data = df.values
print train_data

#Create Random Forest Classifier
forest = RandomForestClassifier(n_estimators = 100)
forest = forest.fit(train_data[0::,1::],train_data[0::,0])

#output = forest.predict(test_data)
