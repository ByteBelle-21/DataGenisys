import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

def predictive_model(df, target,  X_input):
    Y = df[target].to_numpy()
    X = df.drop(target, axis=1)
    transform = preprocessing.StandardScaler()
    X=transform.fit_transform(X) 
    X_input = transform.fit_transform(X_input)
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.3, random_state=2) 
    """
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
    highest_accuracy = 0
    best_model = None
    best_model_name = None
    trained_model = {}
    for model_name in ml_models.keys():
        model_object = GridSearchCV(estimator=ml_models[model_name]['model'],param_grid=ml_models[model_name]['params'], cv=5)                                  
        model_object.fit(X_train,Y_train)
        accuracy = model_object.fit(X_test,Y_test).best_score_
        parameters = model_object.best_params_
        trained_model[model_name] = [accuracy, parameters]
        if accuracy > highest_accuracy:
            highest_accuracy = accuracy
            best_model = model_object
            best_model_name = model_name

        print(f"tuned hpyerparameters for {model_name} = ",parameters)
        print(f"accuracy for {model_name} :",accuracy)
    
    Y_output = best_model.predict(X_input) 
    print(f"prediction  is = ",Y_output)
    return trained_model, Y_output,best_model_name
