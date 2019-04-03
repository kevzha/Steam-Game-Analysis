import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, label_binarize, LabelEncoder
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score, roc_curve, auc, f1_score, mean_squared_error, confusion_matrix, classification_report
from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus
from sklearn.decomposition import PCA
import xgboost as xgb
from sklearn.multiclass import OneVsRestClassifier
import warnings

warnings.filterwarnings('ignore')


def plot_feature_importances(model, title, X_train):
    n_features = X_train.shape[1]
    plt.figure(figsize=(8,8))
    plt.barh(range(n_features), model.feature_importances_, align='center') 
    plt.yticks(np.arange(n_features), pd.DataFrame(X_train).columns.values) 
    plt.xlabel("Feature importance")
    plt.ylabel("Feature")
    plt.title(title)

def run_reports(model, X_train, y_true, y_pred, y_type="train", plot=False):
    print(f"{y_type.title()} Report:")
    acc = accuracy_score(y_true, y_pred) * 100
    print(f"Our {y_type} accuracy is: {acc}")    
    print(f"{y_type.title()} Classification Report:")
    print(pd.DataFrame(classification_report(y_true, y_pred, output_dict=True)))
    if plot:
        plot_feature_importances(model, y_type + "'s Feature of Importance", X_train)
    
def decision_tree(Xtrain, Xtest, ytrain, ytest, criterion="gini", max_depth=None, viz=False):
    clf = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth)
    clf.fit(Xtrain, ytrain)
    y_pred_train = clf.predict(Xtrain)
    y_pred_test = clf.predict(Xtest)
    if viz:
        dot_data = StringIO()
        export_graphviz(clf, out_file=dot_data, filled=True, rounded=True,special_characters=True)
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
        Image(graph.create_png())
    return clf, y_pred_train, y_pred_test