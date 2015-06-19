import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import math
# import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

data = pd.read_csv('dataset.csv', index_col=0)

social_features = list(data.columns.values)[15:]
market_features = list(data.columns.values)[7:15]
degree_features = list(data.columns.values)[5:7]

# print(data.head(n=10))

y = data.SELLER
#  Logistic Regression for social features

x_s = data[social_features]
soc_lm = LogisticRegression()
soc_lm.fit(x_s, y)

#  Logistic Regression for Market Features

x_m = data[market_features]
mar_lm = LogisticRegression()
mar_lm.fit(x_m, y)

#  Logistic Regression for Degree Features

x_d = data[degree_features]
deg_lm = LogisticRegression()
deg_lm.fit(x_d, y)

#  Logistic Regression for All Features

x_a = data[degree_features + market_features + social_features]
all_lm = LogisticRegression()
all_lm.fit(x_a, y)

#  Random Testing

# lista_for_deg = [random.randint(1.0, 380) for i in range(2)]
# lista_for_sol_mar = [random.uniform(0, 1) for i in range(8)]
# lista_for_all = [random.randint(1.0, 380) if i < 2 else random.uniform(0, 1) for i in range(18)]
# pred = soc_lm.predict(lista_for_sol_mar)
# print(lista_for_all)
# print(deg_lm.intercept_)
# print(all_lm.coef_)
# print(sigmoid(pred))


features_sets = [x_s, x_m, x_d, x_a]
features_sets_names = ['C1 - Social features',
                       'C2 - Market features',
                       'C3 - Degrees features',
                       'C4 - Combined features']
scores_names = ['Precision', 'Recall', 'F-1', 'AUC']

# model evaluation for the model, logistic regression.

model = LogisticRegression()

precision = [cross_val_score(model, x, y, scoring='precision', cv=5) for x in features_sets]
recall = [cross_val_score(model, x, y, scoring='recall', cv=5) for x in features_sets]
f1 = [cross_val_score(model, x, y, scoring='f1', cv=5) for x in features_sets]
auc = [cross_val_score(model, x, y, scoring='roc_auc', cv=5) for x in features_sets]

scores = [precision, recall, f1, auc]

print('Model evaluation by features sets:')
print('----------------------------------')

for i in range(4):
    print('', features_sets_names[i] + ':')
    prom = []
    for j in range(4):
        print('  ' + scores_names[j] + ':', scores[j][i].mean())
        prom.append(scores[j][i].mean())
    print('  Average:', np.array(prom).mean(), '\n')

coefs = all_lm.coef_.tolist()[0]
exp_coefs = [math.exp(i) for i in coefs]

# features_list = degree_features + market_features + social_features
# pairs = [(i, j) for i, j in zip(features_list, exp_coefs)]
# for i in pairs:
#     print(i)


print('Coefficients relevance testing:')
print('-------------------------------')

pred = all_lm.predict_proba([12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
pred_next = all_lm.predict_proba([13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# print(all_lm.classes_)
# print(all_lm.coef_)
# print(sigmoid(all_lm.intercept_))
preds = pred.tolist()[0]
print(' Initial prediction:', preds, '[is not seller v/s is seller]')
odds = preds[1] / preds[0]
print(' Initial odds:', odds)

preds_next = pred_next.tolist()[0]
print(' 1-unit-increase prediction:', preds_next, '[is not seller v/s is seller]')
odds_next = preds_next[1] / preds_next[0]
print(' 1-unit-increase odds:', odds_next)

print(' Multiplying by coef odds:', odds * exp_coefs[0])
# The next inequality is only valid (due to float calculation issues) for some cases, so we round
# the values for it to be significant.
print(' Estimated odds == calculated odds:',
      round((odds * exp_coefs[0]), 5) == round((odds_next), 5))


# model evaluation for another model, the decission tree.
# Comparison Model  http://scikit-learn.org/stable/modules/tree.html
model = DecisionTreeClassifier()
precision = cross_val_score(model, x_a, y, scoring='precision', cv=5)
recall = cross_val_score(model, x_a, y, scoring='recall', cv=5)
f1 = cross_val_score(model, x_a, y, scoring='f1', cv=5)
auc = cross_val_score(model, x_a, y, scoring='roc_auc', cv=5)

decision_tree_classifier_scores = [precision.mean(), recall.mean(), f1.mean(), auc.mean()]
print('\nDecision Tree Classifier model evaluation:')
print('------------------------------------------')
print(' C4 - Combined features:')
for i in range(len(decision_tree_classifier_scores)):
    print('  ' + scores_names[i] + ':', decision_tree_classifier_scores[i])
print('  Average:', np.array(decision_tree_classifier_scores).mean())
