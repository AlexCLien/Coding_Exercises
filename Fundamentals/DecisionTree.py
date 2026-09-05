from sklearn import tree

# grade scores
X = [[49], [50], [79], [80], [99], [100], [12],[18],[59],[60]]
# pass or fail
Y = ['fail', 'fail', 'pass', 'pass', 'pass', 'pass', 'fail','fail','fail','pass']

# Creates a decision tree classifier and fits the model to the data
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

prediction_pass = clf.predict([[70]])
prediction_fail = clf.predict([[30]])

print(prediction_pass)  # Output: ['pass']
print(prediction_fail)  # Output: ['fail']

#boundary numbers
Z = [[48], [49], [50], [51], [58], [59], [60], [61]]
print(clf.predict(Z))
