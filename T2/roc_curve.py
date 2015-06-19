import numpy as np
from scipy import interp
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import StratifiedKFold
import pandas as pd
from sklearn.linear_model import LogisticRegression
import random

data = pd.read_csv('dataset.csv', index_col=0)

social_features = list(data.columns.values)[15:]
market_features = list(data.columns.values)[7:15]
degree_features = list(data.columns.values)[5:7]
all_features = social_features + market_features + degree_features

features = [social_features, market_features, degree_features, all_features]
names = ['Social', 'Market', 'Degree', 'All']
for feature in features:
    X = data[feature]
    y = data.SELLER
    n_samples, n_features = X.shape
    random_state = np.random.RandomState(0)
    X = np.c_[X, random_state.randn(n_samples, 50 * n_features)]
    cv = StratifiedKFold(y, n_folds=5)
    classifier = LogisticRegression()
    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)
    all_tpr = []
    for i, (train, test) in enumerate(cv):
        probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
        fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)

    mean_tpr /= len(cv)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, 'k--', color=(random.randint(0,1), random.randint(0,1), random.randint(0,1)),
             label=names[features.index(feature)] + ' Mean ROC (area = %0.2f)' % mean_auc, lw=1)

plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic for sellers prediction with Logistic Regression')
plt.legend(loc="lower right")
plt.show()
