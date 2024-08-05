import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

def predictive_model(df, target):
    Y = df[target].to_numpy()
    X = df.drop(target, axis=1)
    transform = preprocessing.StandardScaler()
    X=transform.fit_transform(X) 
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
   
    for model_name in ml_models.keys():
        model_object = RandomizedSearchCV(estimator=ml_models[model_name]['model'],param_distributions=ml_models[model_name]['params'], cv=5,n_iter=10,n_jobs=-1,random_state=2)
                                          
                                          
        model_object.fit(X_train,Y_train)
        print(f"tuned hpyerparameters for {model_name} = ",model_object.best_params_)
        print(f"accuracy for {model_name} :",model_object.fit(X_test,Y_test).best_score_)
    
