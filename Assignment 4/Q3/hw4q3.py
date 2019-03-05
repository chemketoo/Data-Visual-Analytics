## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect seizure

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
data = pd.read_csv('seizure_dataset.csv')
# XXX

# XXX
# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]
# The random state to use while splitting the data.
random_state = 100
# XXX

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the paramater 'shuffle' set to true and the 'random_state' set to 100.
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state= random_state, shuffle = True)
# XXX

# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
lr_model1 = LinearRegression()
lr_time = time.time()
lr_model1.fit(x_train,y_train)
print("linear: --%s seconds --" %(time.time()-lr_time)) #0.07811522483825684
# XXX

# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
lr_model1trainpredict = [round(i) for i in lr_model1.predict(x_train)]
lr_model1_train = accuracy_score(lr_model1trainpredict, y_train)
print("lr_model1 Training Set Accuracy", lr_model1_train) #0.8607817303469477

# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
lr_model1testpredict = [round(i) for i in lr_model1.predict(x_test)]
lr_model1_test = accuracy_score(lr_model1testpredict, y_test)
print("lr_model1 Testing Set Accuracy", lr_model1_test) #0.8239508700102354
# Note: Use y_predict.round() to get 1 or 0 as the output.
# XXX

# ############################################### Multi Layer Perceptron #################################################
# XXX
# TODO: Create an MLPClassifier and train it.
mlp_model1 = MLPClassifier(random_state = random_state)
mlp_time = time.time()
mlp_model1.fit(x_train,y_train)
print("mlp: --%s seconds --" %(time.time()-mlp_time)) #2.37566876411438
# XXX


# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
mlp_model1trainpredict = [round(i) for i in mlp_model1.predict(x_train)]
mlp_model1_train = accuracy_score(mlp_model1trainpredict, y_train)
print("mlp_model1 Training Set Accuracy", mlp_model1_train) #0.9696969696969697


# TODO: Test its accuracy on the test set using the accuracy_score method.
mlp_model1testpredict = [round(i) for i in mlp_model1.predict(x_test)]
mlp_model1_test = accuracy_score(mlp_model1testpredict, y_test)
print("mlp_model1 Testing Set Accuracy", mlp_model1_test) #0.804503582395087
# XXX

# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
rfc_model1 = RandomForestClassifier()
rfc_time = time.time()
rfc_model1.fit(x_train, y_train)
print("rfc: --%s seconds --" %(time.time()-rfc_time)) #0.3125026226043701
# XXX

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
rfc_model1trainpredict = [round(i) for i in rfc_model1.predict(x_train)] 
rfc_model1_train = accuracy_score(rfc_model1trainpredict, y_train) 
print("rfc_model1 Training Set Accuracy", rfc_model1_train) #0.997364953886693

# TODO: Test its accuracy on the test set using the accuracy_score method.
rfc_model1testpredict = [round(i) for i in rfc_model1.predict(x_test)] 
rfc_model1_test = accuracy_score(rfc_model1testpredict, y_test) 
print("rfc_model1 Testing Set Accuracy", rfc_model1_test) #0.9641760491299898
# XXX

# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
hypersvmTunePram = {'n_estimators':[10,20,30], 'max_depth':[10,20,30]}
rfc_model2 = GridSearchCV(RandomForestClassifier(), hypersvmTunePram, cv=10)
rfc_model2.fit(x_train, y_train)

print(rfc_model2.best_params_) #{'max_depth': 20, 'n_estimators': 30}
print(rfc_model2.best_score_) #0.9657444005270093

# y_actual, y_predicted = y_test, rfc_model2.predict(x_test).round()
rfc_model2_test = accuracy_score(y_actual, y_predicted)
print(rfc_model2_test) #0.9631525076765609
# XXX

############################################ Support Vector Machine ###################################################
# XXX
TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
normxTrain = normalize(x_train, norm='l2')
normxTest = normalize(x_test, norm='l2')

# TODO: Create a SVC classifier and train it.
svm_model1 = SVC(gamma = 'scale') 
svctime = time.time()
svm_model1.fit(x_train, y_train) #before pre process
print("svc: --%s seconds --" %(time.time()-svctime)) #1.9588630199432373
# XXX

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
svm_model1trainpredict = [round(i) for i in svm_model1.predict(x_train)]
svm_model1_train = accuracy_score(svm_model1trainpredict, y_train)
print("svm_model1 Training Set Accuracy", svm_model1_train) #1.0

# TODO: Test its accuracy on the test set using the accuracy_score method.
svm_model1testpredict = [round(i) for i in svm_model1.predict(x_test)]
svm_model1_test = accuracy_score(svm_model1testpredict, y_test)
print("svm_model1 Testing Set Accuracy", svm_model1_test) #0.8024564994882293
# XXX

# XXX
TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
Print the best params, using .best_params_, and print the best score, using .best_score_.
svmTunePram = {'kernel':('linear', 'rbf'), 'C':[0.0001, 0.1, 10]}
svm_model2 = GridSearchCV(SVC(gamma = 'scale'), svmTunePram, cv=10)
svm_model2.fit(normxTrain, y_train)

print(svm_model2.best_params_) #{'C': 0.0001, 'kernel': 'linear'}
print(svm_model2.best_score_) #0.8054457619675011

norm_ytrue, norm_ypred = y_test, svm_model2.predict(normxTest).round()
svm_model2_test = accuracy_score(norm_ytrue, norm_ypred)
print("svm_model2 Testing Accuracy Score", svm_model2_test) #0.812691914022518
# XXX

# XXX
best_score = max(svm_model2.cv_results_['mean_test_score'])
index = svm_model2.cv_results_['mean_test_score'].tolist().index(best_score)
print(best_score) #0.8054457619675011
print(svm_model2.cv_results_['mean_train_score'][index]) #0.8124236688926187
print(svm_model2.cv_results_['mean_fit_time'][index]) #0.7793070554733277
# XXX

