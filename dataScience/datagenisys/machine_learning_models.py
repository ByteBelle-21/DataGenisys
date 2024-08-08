import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.experimental import enable_halving_search_cv  
from sklearn.model_selection import HalvingRandomSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score, f1_score

def predictive_model(df, target, X_input):
    Y = df[target].to_numpy()
    X = df.drop(target, axis=1)
    transform = preprocessing.StandardScaler()
    X=transform.fit_transform(X) 
    X_input = transform.fit_transform(X_input)
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.3, random_state=2) 
   
    ml_models = {
        'Logistic Regression': {
            'model' : LogisticRegression(),
            'params' : {'C':[0.01, 0.1, 1, 10, 100],
                        'penalty':['l2'],
                        'solver':['lbfgs', 'liblinear']} 
            },
        'Support vector machine': {
            'model' : SVC(),
            'params' : {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
                        'C': np.logspace(-3, 3, 5),
                        'gamma':np.logspace(-3, 3, 5)}
            },
        'Decision tree classifier': {
            'model' : DecisionTreeClassifier(),
            'params' : {'criterion': ['gini', 'entropy'],
                        'splitter': ['best', 'random'],
                        'max_depth': [2*n for n in range(1,10)],
                        'max_features': ['auto', 'sqrt'],
                        'min_samples_leaf': [1, 2, 4],
                        'min_samples_split': [2, 5, 10]} 
            },
        'K-nearest neighbors': {
            'model' : KNeighborsClassifier(),
            'params' :{'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                       'p': [1,2]} 
            }    
    }   
    """
    ml_models = {
        'Logistic Regression': {
            'model': LogisticRegression(),
            'params': {'C': [0.1, 1, 10], 'penalty': ['l2'], 'solver': ['lbfgs']}
        },
        'Support Vector Machine': {
            'model': SVC(),
            'params': {'kernel': ['linear', 'rbf'], 'C': [0.1, 1, 10], 'gamma': [0.1, 1, 10]}
        },
        'Decision Tree Classifier': {
            'model': DecisionTreeClassifier(),
            'params': {'criterion': ['gini'], 'max_depth': [10, 20], 'min_samples_split': [2, 5]}
        },
        'K-Nearest Neighbors': {
            'model': KNeighborsClassifier(),
            'params': {'n_neighbors': [5, 10], 'algorithm': ['auto']}
        }
    }
    """

    highest_accuracy = 0
    best_model = None
    best_f1_score = 0
    for model_name in ml_models.keys():
        #model_object = GridSearchCV(estimator=ml_models[model_name]['model'],param_grid=ml_models[model_name]['params'], cv=5, n_jobs=-1)                                  
        model_object = HalvingRandomSearchCV(
        estimator=ml_models[model_name]['model'],
        param_distributions=ml_models[model_name]['params'],
        factor=3,  # Controls the aggressiveness of the search
        random_state=2,
        n_jobs=-1
        )
        model_object.fit(X_train,Y_train)
        Y_predict = model_object.predict(X_test)
        accuracy = accuracy_score(Y_test, Y_predict)
        F1_score = f1_score(Y_test, Y_predict, average='weighted')
        if accuracy > highest_accuracy:
            highest_accuracy = accuracy
            best_f1_score = F1_score
            best_model = model_object
        elif accuracy == highest_accuracy:
            if F1_score > best_f1_score:
                highest_accuracy = accuracy
                best_f1_score = F1_score
                best_model = model_object

    Y_output = best_model.predict(X_input)
    return Y_output