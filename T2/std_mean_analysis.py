import pandas as pd

data = pd.read_csv('dataset.csv', index_col=0)

labels = data.columns.values[5:]

print('Standard deviation for each column/feature:')
print('-------------------------------------------')
for label in labels:
    print(label + ' std:', data[label].std())

print('\nMeans for each column/feature:')
print('--------------------------------')
for label in labels:
    print(label + ' mean:', data[label].mean())
