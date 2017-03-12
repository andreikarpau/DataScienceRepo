__author__ = 'askofen'
from sklearn import neighbors
from sklearn.cross_validation import KFold
from sklearn.metrics import precision_recall_curve

knn = neighbors.KNeighborsClassifier(n_neighbors = 3)
knn.fit([[1], [2], [3], [4], [5], [6], [7]], [0,0,0,1,1,2,2])

knn.predict(1)
knn.predict(1.6)
knn.predict(4.1)

#prediction probabilities
knn.predict_proba(3.5)
knn.predict_proba(1.5)



cv = KFold(n = 5, n_folds = 3)

for trainI, testI in cv:
    print(trainI)
    print(testI)


precision, recall, thresholds = precision_recall_curve([0,1,1,1,0,0,0,0,1,1], [0,1,1,1,1,0,0,0,1,1])