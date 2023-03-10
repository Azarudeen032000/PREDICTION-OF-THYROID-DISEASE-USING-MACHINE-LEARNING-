# -*- coding: utf-8 -*-
"""thyroid.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fPLlRv5rkvuNPKUMflISm_xHyt9qWkwu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings 
warnings.simplefilter('ignore')

data = pd.read_csv("/content/thyroid dataset.csv")

"""# New Section"""

data.head()

data.shape

data.info()

data.columns

# Checking the target feature
data['class'].value_counts()

# increased binding protein clearly a positive sign of Thyroid
# *decreased binding protein can be considered as negative class itself

# Adjusting the target feature

data['class'].replace(to_replace = ['decreased binding protein','increased binding protein' ], value =['negative', 'positive'], inplace = True)

data['class'].value_counts()

plt.figure(figsize = (7,5))
data['class'].value_counts().plot(kind = 'pie')

# Checking duplicates in dataset

data.duplicated().sum()

#see which are the rows are duplicated in a dataset
data.loc[data.duplicated()]

# Removing Duplicated data from dataset
data.drop_duplicates(inplace = True)

data.shape

data.isnull().sum()

#Droping unnecessary feature
data.drop('referralSource', axis = 1, inplace = True)

data.info()

# Data Analysis

data.describe()

import seaborn as sns
#get correlations of each features in dataset
corrmat = data.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(7,7))
# plot heat map
g=sns.heatmap(data[top_corr_features].corr(),annot=True,cmap="RdYlGn")

plt.figure(figsize = (20,4))
sns.histplot(x = 'age', hue = 'class', data = data)

# * Thyroid emergers at an early age of 19 and can show symoptoms till the age of 76
# * Although thyroid is not very commom in elder age group, people in the late 20s and late 70s shows positive sign of thyroid.
# * People in their 30s & 70s have significant chanches of getting thyroid.

plt.figure(figsize = (6,4))
sns.countplot(x = 'gender', hue = 'class', data = data)

# * Females are prone to have thyriod more as compared to Males.

data['class'] = data['class'].map({"positive":1,"negative":0})

data.select_dtypes(include = np.number).columns

data['gender'].value_counts().plot(kind = 'pie')

# * Our data is having majority of Females candidates

fig, ax = plt.subplots(2,3, figsize =(20,10))

sns.histplot(x= 'TSH', hue = 'class', data=data, ax = ax[0][0])
sns.histplot(x= 'T3', hue = 'class', data=data, ax = ax[0][1])
sns.histplot(x= 'TT4', hue = 'class', data=data, ax = ax[0][2])
sns.histplot(x= 'T4U', hue = 'class', data=data, ax = ax[1][0])
sns.histplot(x= 'FTI', hue = 'class', data=data, ax = ax[1][1])

# * All these specific presence of substances in blood does not much contribute to Thyroid.
# * However, presence of "T4U" above 1.3 units in blood leads to positive signs for Thyroid.

sns.jointplot(x='class', y='TT4', data=data, kind='scatter', height=5,  hue = 'gender')
sns.jointplot(x='class', y='TSH', data=data, kind='scatter', height=5,  hue = 'gender')
sns.jointplot(x='class', y='T3', data=data, kind='scatter', height=5,  hue = 'gender')
sns.jointplot(x='class', y='T4U', data=data, kind='scatter', height=5,  hue = 'gender')
sns.jointplot(x='class', y='FTI', data=data, kind='scatter', height=5,  hue = 'gender')

# * From the above observation on 'TSH', 'T3', 'TT4', 'T4U', 'FTI' in blood w.r.t Age we conclude that :
# * Level of TT4 that results in Positive cases for tyroid is having in range of (70-270) and majorly in Females.
# * Level of THS that results in Positive cases for tyroid is having in range of (0-25) and majorly in Females.
# * Level of T3 in blood results in Positive cases for tyroid is having in range of (1.5-5.5).
# * Level of T4U in blood results in Positive cases for tyroid is having in range of (0.8-2) and contributing to both genders.
# * Level of FTI in blood results in Positive cases for tyroid is having in range of (60-230).

data['pregnant'] = data['pregnant'].map({"t":1,"f":0})

pregnant_class =data.pivot_table(values= 'class', columns ='pregnant')
pregnant_class.loc['class',:].plot(kind='bar', width=0.4,color=['b','r'])

# * Almost 68% changes of having Thyroid during Pregnancy

data['I131treatment'] = data['I131treatment'].map({"t":1,"f":0})

I131treatment_class =data.pivot_table(values= 'class', index ='I131treatment' )
I131treatment_class.loc[:,'class'].plot(kind= 'bar', color =['cyan','green'])

# * Data shows that people which are not undergoing 'I131treatment' are prone to have Thyroid 2X times.

# Feature Engineering

# Handling missing values

data.isnull().sum()

data['TSH'] = data['TSH'].fillna(data['TSH'].mean())
data['T3'] = data['T3'].fillna(data['T3'].mean())
data['TT4'] = data['TT4'].fillna(data['TT4'].mean())
data['T4U'] = data['T4U'].fillna(data['T4U'].mean())
data['FTI'] = data['FTI'].fillna(data['FTI'].mean())

data['age'] = data['age'].fillna(data['age'].mode()[0])

data['tumor'] = data['tumor'].fillna(data['tumor'].mode()[0])

data.isnull().sum()

# Outliers Handeling

fig, ax = plt.subplots(2,3, figsize =(20,10))

sns.boxplot(data['age'], ax = ax[0][0])
sns.boxplot(data['TSH'], ax = ax[0][1])
sns.boxplot(data['T3'], ax = ax[0][2])
sns.boxplot(data['TT4'], ax = ax[1][0])
sns.boxplot(data['T4U'], ax = ax[1][1])
sns.boxplot(data['FTI'], ax = ax[1][2])

# Age
Q1 = data.age.quantile(0.25)
Q3 = data.age.quantile(0.75)

IQR = Q3 -Q1
data = data[(data.age >= Q1-1.5*IQR) & (data.age <= Q3+1.5*IQR)]

# TSH
Q1 = data.TSH.quantile(0.25)
Q3 = data.TSH.quantile(0.75)

IQR = Q3 -Q1
data = data[(data.TSH >= Q1-1.5*IQR) & (data.TSH <= Q3+1.5*IQR)]

# T3
Q1 = data.T3.quantile(0.25)
Q3 = data.T3.quantile(0.75)

IQR = Q3 -Q1
data = data[(data.T3 >= Q1-1.5*IQR) & (data.T3 <= Q3+1.5*IQR)]

# TT4
Q1 = data.TT4.quantile(0.25)
Q3 = data.TT4.quantile(0.75)

IQR = Q3 -Q1
data = data[(data.TT4 >= Q1-1.5*IQR) & (data.TT4 <= Q3+1.5*IQR)]

# T4U
Q1 = data.T4U.quantile(0.25)
Q3 = data.T4U.quantile(0.75)

IQR = Q3 -Q1
data = data[(data.T4U >= Q1-1.5*IQR) & (data.T4U <= Q3+1.5*IQR)]

# FTI
Q1 = data.FTI.quantile(0.25)
Q3 = data.FTI.quantile(0.75)

IQR = Q3 -Q1
data = data[(data.FTI >= Q1-1.5*IQR) & (data.FTI <= Q3+1.5*IQR)]

fig, ax = plt.subplots(2,3, figsize =(20,10))

sns.boxplot(data['age'], ax = ax[0][0])
sns.boxplot(data['TSH'], ax = ax[0][1])
sns.boxplot(data['T3'], ax = ax[0][2])
sns.boxplot(data['TT4'], ax = ax[1][0])
sns.boxplot(data['T4U'], ax = ax[1][1])
sns.boxplot(data['FTI'], ax = ax[1][2])

fig, ax = plt.subplots(2,3, figsize =(20,10))

sns.distplot(data['age'], ax = ax[0][0])
sns.distplot(data['TSH'], ax = ax[0][1])
sns.distplot(data['T3'], ax = ax[0][2])
sns.distplot(data['TT4'], ax = ax[1][0])
sns.distplot(data['T4U'], ax = ax[1][1])
sns.distplot(data['FTI'], ax = ax[1][2])

import scipy.stats as s
import pylab

def plot_data(data, feature):
  plt.figure(figsize = (8, 4))
  plt.subplot(1,2,1)
  data[feature].hist()
  plt.subplot(1,2,2)
  s.probplot(data[feature], dist = 'norm', plot = pylab)
  plt.show()

plot_data(data, 'age')

## Lograthemic transformation

data['Age_log'] = np.log(data['age'])
plot_data(data,'Age_log' )

## Exponential Transformation

data['Age_exp'] = data.age**(1/1.2)
plot_data(data, 'Age_exp')

## Reciprocal Transformation
data['Age_rec'] = 1/ data.age
plot_data(data, 'Age_rec')

## Square Root Transformation
data['Age_square'] = data.age ** (1/2)
plot_data(data, 'Age_square')

## Box cox transformation

import scipy
data['Age_boxcox'], parameter = s.boxcox(data['age'])
plot_data(data,'Age_boxcox')

#  we observe that 'Lograthemic transformation', 'Reciprocal Transformation', 'Square Root Transformation' are not giving us the good results
data.drop(['Age_log','Age_rec','Age_square'], axis =1 , inplace = True)

fig, ax = plt.subplots(1,3, figsize =(20,5))

sns.distplot(data['age'], ax = ax[0])
sns.distplot(data['Age_exp'], ax = ax[1])
sns.distplot(data['Age_boxcox'], ax = ax[2])

data.drop(['age','Age_boxcox'], axis =1 , inplace = True)

plot_data(data, 'TSH')

## Lograthemic transformation

data['TSH_log'] = np.log(data['TSH'])
plot_data(data,'TSH_log' )

## Exponential Transformation

data['TSH_exp'] = data.TSH**(1/1.2)
plot_data(data, 'TSH_exp')

## Reciprocal Transformation
data['TSH_rec'] = 1/ data.TSH
plot_data(data, 'TSH_rec')

## Square Root Transformation
data['TSH_square'] = data.TSH ** (1/2)
plot_data(data, 'TSH_square')

## Box cox transformation
data['TSH_boxcox'], parameter = s.boxcox(data['TSH'])
plot_data(data,'TSH_boxcox')

# we observe that 'Lograthemic transformation', 'Reciprocal Transformation', 'Exponential Transformation' are not giving us the good results
data.drop(['TSH_rec','TSH_log','TSH_exp'], axis =1 , inplace = True)

fig, ax = plt.subplots(1,3, figsize =(20,5))

sns.distplot(data['TSH'], ax = ax[0])
sns.distplot(data['TSH_square'], ax = ax[1])
sns.distplot(data['TSH_boxcox'], ax = ax[2])

data.drop(['TSH','TSH_square'], axis =1 , inplace = True)

data.head()

cat_col = data.select_dtypes(include = 'object').columns

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

for i in cat_col:
    data[i] = le.fit_transform(data[i])

data.head()

data.drop('hypopituitary', axis = 1, inplace = True)

# Feature Selection

plt.figure(figsize =(20,14))
sns.heatmap(data.corr(), annot = True , cmap ='CMRmap_r')

# we observe that 'FTI' and 'TT4' are having high correlation among each other

# with the following function we can select highly correlated features
# it will remove the first feature that is correlated with anything other feature

def correlation(data, threshold):
    col_corr = set()  # Set of all the names of correlated columns
    corr_matrix = data.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value
                colname = corr_matrix.columns[i]  # getting the name of column
                col_corr.add(colname)
    return col_corr

corr_features = correlation(data, 0.6)
corr_features

# Dropping correlated feature 'FIT'
data.drop('FTI', axis = 1, inplace = True)

data.drop('TSH_boxcox', axis = 1, inplace = True)

## Chi square test

from sklearn.feature_selection import chi2

x1 = data[['gender','Thyroxine','queryThyroxine','antithyroid','sick','pregnant','I131treatment','hypothyroid','hyperthyroid','lithium','tumor']]
y1 = data['class']

f_score =chi2(x1,y1)

p_value = pd.Series(f_score[1],index = x1.columns)
p_value = p_value.sort_values(ascending = True)
p_value

cols = []

for i in p_value.index:
    if p_value[i] <=0.05:
        print(i, '------------', 'Reject Null Hypothesis')
    else:
        print(i, '------------', 'Accept Null Hypothesis')
        cols.append(i)

# droping features that will not add any value to my model 

data.drop(labels = cols, axis = 1, inplace = True)

data.head()

# Splitting

X = data.drop(['class'], axis  =1)
y = data['class']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42)
X_train.shape, X_test.shape

# Model Building

# Logistic Regression
from sklearn.linear_model import LogisticRegression

# create the instance of logistic regression model
lr = LogisticRegression()

# fit the model
lr.fit(X_train, y_train)

# Make a prediction for the testing set
y_pred_lr = lr.predict(X_test)

from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, classification_report

# print accuracy on  test data

print('Accuracy Score on testing data:', accuracy_score(y_test, y_pred_lr))

print(classification_report(y_test, y_pred_lr))

# f1 score 

print('f1_score :', f1_score(y_test, y_pred_lr) )

# precision score

print('Precision Score :', precision_score(y_test, y_pred_lr) )

# Recall Score

print('Recall Score :', recall_score(y_test, y_pred_lr) )

# Confusion matrics

plt.figure(figsize =(10,5))
cm = confusion_matrix(y_test, y_pred_lr)

sns.heatmap(cm, annot = True)

#let's first visualize the decisiontree on the data without doing any pre processing
from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier()
dt.fit(X_train,y_train)

y_pred_dt = dt.predict(X_test)

# print accuracy on  test data

print('Accuracy Score on testing data:', accuracy_score(y_test, y_pred_dt))

# precision score

print('Precision Score :', precision_score(y_test, y_pred_dt) )

# Recall Score

print('Recall Score :', recall_score(y_test, y_pred_dt) )

# f1 score 

print('f1_score :', f1_score(y_test, y_pred_dt) )

# Balance the dataset using SMOTE

from imblearn.over_sampling import SMOTE

sm = SMOTE(random_state =23)
X_sm , y_sm = sm.fit_resample(X,y)

X_train, X_test, y_train, y_test = train_test_split(X_sm , y_sm, test_size = 0.20, random_state = 42)

# create the instance of logistic regression model
clf1 = LogisticRegression()

# fit the model
clf1.fit(X_train, y_train)

#let's first visualize the tree on the data without doing any pre processing
clf2 = DecisionTreeClassifier()
clf2.fit(X_train,y_train)

## Naive Bayes Classifier
from sklearn.naive_bayes import GaussianNB
clf3 = GaussianNB()

# fit the model
clf3.fit(X_train, y_train)

# Support Vector Machine


from sklearn import svm
clf4 = svm.SVC(kernel = 'linear')

#fit the model
clf4.fit(X_train, y_train)

# prediction on testing data
y_pred_lr1 = clf1.predict(X_test)
y_pred_dt2 = clf2.predict(X_test)
y_pred_nb = clf3.predict(X_test)
y_pred_svm = clf4.predict(X_test)

# print accuracy on  test data

print('Accuracy Score on testing data LR:', accuracy_score(y_test, y_pred_lr1))
print('Accuracy Score on testing data DT:', accuracy_score(y_test, y_pred_dt2))
print('Accuracy Score on testing data NB:', accuracy_score(y_test, y_pred_nb))
print('Accuracy Score on testing data SVM:', accuracy_score(y_test, y_pred_svm))

# f1 score 

print('f1_score : LR', f1_score(y_test, y_pred_lr1) )
print('f1_score : DT', f1_score(y_test, y_pred_dt2) )
print('f1_score : NB', f1_score(y_test, y_pred_nb) )
print('f1_score : SVM', f1_score(y_test, y_pred_svm) )

# Confusion matrics on DT

plt.figure(figsize =(7,4))
cm = confusion_matrix(y_test, y_pred_dt2)

sns.heatmap(cm, annot = True)

# Confusion matrics on Logistic Regression

plt.figure(figsize =(7,4))
cm = confusion_matrix(y_test, y_pred_lr1)

sns.heatmap(cm, annot = True)

# Confusion matrics on Naive Bayes

plt.figure(figsize =(7,4))
cm = confusion_matrix(y_test, y_pred_nb)

sns.heatmap(cm, annot = True)

# Confusion matrics on SVM

plt.figure(figsize =(7,4))
cm = confusion_matrix(y_test, y_pred_svm)

sns.heatmap(cm, annot = True)

# Comparision

Models = pd.DataFrame({'Models':['LogisticRegression', 'DecisionTree','Naive Bayes','SVM'], 'Accuracy': [accuracy_score(y_test, y_pred_lr1)*100,accuracy_score(y_test, y_pred_dt2)*100,accuracy_score(y_test, y_pred_nb)*100,accuracy_score(y_test, y_pred_svm)*100]})

plt.figure(figsize=(10,5))
sns.set()
sns.barplot(Models['Models'], Models['Accuracy'],palette="Spectral_r")

"""Decision tree gives highest accuracy"""

F1_Score = pd.DataFrame({'Models':['LogisticRegression', 'DecisionTree','Naive Bayes','SVM'], 'f1_score': [f1_score(y_test, y_pred_lr1),f1_score(y_test, y_pred_dt2),f1_score(y_test, y_pred_nb), f1_score(y_test, y_pred_svm)]})

plt.figure(figsize=(10,5))
sns.set()
sns.barplot(F1_Score['Models'], F1_Score['f1_score'],palette="cubehelix")

