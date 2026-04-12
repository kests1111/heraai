import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

df = pd.read_csv(r"C:\Users\soldierofgabe\Downloads\Heart.csv")

pd.DataFrame(df)

df['AHD'] = df['AHD'].map({'No':0, 'Yes':1})
df['ChestPain'] = df['ChestPain'].map({'typical':0, 'nontypical':1, 'asymptomatic':2, 'nontypical':3, 'nonanginal':4})
df['Thal'] = df['Thal'].map({'fixed':0, 'normal':1, 'reversable':2})
df = df.dropna()
print(df)

X = df.iloc[:, :-1]
Y = df['AHD']
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=33)
clf = LogisticRegression(max_iter=5000, random_state = 0)
clf.fit(X_train, y_train)
acc = accuracy_score(y_test,clf.predict(X_test)) * 100 
print(f"logistic accuracy: {acc:.2f}%")
model = GaussianNB()
model.fit(X_train, y_train)
acc = accuracy_score(y_test,model.predict(X_test)) * 100 
print(f"naive bias accuracy: {acc:.2f}%")


# df = df.drop(columns=['PassengerId','Ticket', 'Cabin', 'Name', 'Embarked'])
# df['Age'] = df['Age'].fillna(df['Age'].median())
# df['Fare'] = df['Fare'].fillna(df['Age'].median())
# #df = df.dropna()
# df['Sex'] = df['Sex'].map({'male':0, 'female':1})
# #df.drop(df[df['Fare'] == 0].index)

# print(type(df))
# print(df.shape)
# print(df.iloc[:, 1:])

# X = df.iloc[:, 1:]
# Y = df['Survived']
# scaler = StandardScaler()
# X = scaler.fit_transform(X)

# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=33)

# clf = LogisticRegression(max_iter=5000, random_state = 0)
# clf.fit(X_train, y_train)
# acc = accuracy_score(y_test,clf.predict(X_test)) * 100 
# print(f"accuracy: {acc:.2f}%")