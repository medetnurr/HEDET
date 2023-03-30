import numpy as np
import pandas as pd
import copy
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import joblib

warnings.simplefilter(action="ignore", category=FutureWarning)

# Importing the dataset
dataset = pd.read_csv('db/heart.csv')
df = pd.DataFrame(dataset)

# Create deep copy from original dataset
deep_copy_df = copy.deepcopy(df)

# Encoding categorical Data
df['Sex'].replace({'M': 1, 'F': 2}, inplace=True)
df['ChestPainType'].replace({'ATA': 1, 'NAP': 2, 'ASY': 3, 'TA': 4}, inplace=True)
df['FastingBS'].replace({0: 1, 1: 2}, inplace=True)
df['RestingECG'].replace({'Normal': 1, 'ST': 2, 'LVH': 3}, inplace=True)
df['ExerciseAngina'].replace({'N': 1, 'Y': 2}, inplace=True)
df['ST_Slope'].replace({'Up': 1, 'Flat': 2, 'Down': 3}, inplace=True)
df['HeartDisease'].replace({1: 1, 0: 2}, inplace=True)

# separate categorical data/numerical data
df_num = df[['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']]
df_cat = df[['Sex', 'ChestPainType', 'FastingBS', 'RestingECG', 'ExerciseAngina', 'ST_Slope', 'HeartDisease']]
df_num_name = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']
df_cat_name = ['Sex', 'ChestPainType', 'FastingBS', 'RestingECG', 'ExerciseAngina', 'ST_Slope', 'HeartDisease']

# Converting Zero Value of Cholesterol to NaN Value
df.loc[df['Cholesterol'] == 0, 'Cholesterol'] = np.nan

# NaN value of Cholesterol is filled with median value
df["Cholesterol"] = df["Cholesterol"].fillna(df["Cholesterol"].median())

# According to Blood Pressure picture we haven`t ziro value , but in this case we have 1 sample
ziro_RestingBP = df[df['RestingBP'] == 0]

# We should remove this column
df = df.drop(df[(df['RestingBP'] == 0)].index)

pd.DataFrame(abs(df.corr()['HeartDisease'])).T.round(2)

df.agg(
    {
        "Age": ["min", "max", "median", "mean", "skew", 'std'],
        "RestingBP": ["min", "max", "median", "mean", "skew", 'std'],
        "Cholesterol": ["min", "max", "median", "mean", "skew", 'std'],
        "Oldpeak": ["min", "max", "median", "mean", "skew", 'std'],
        "MaxHR": ["min", "max", "median", "mean", "skew", 'std']
    }
)

"""Data Train and Test"""

x = df.drop('HeartDisease', axis=1)
y = df.HeartDisease

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=20, random_state=21)
for i in range(21, 31):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=i, random_state=21)

scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.fit_transform(x_test)

x_train = pd.DataFrame(x_train, columns=x.columns)
x_test = pd.DataFrame(x_test, columns=x.columns)

""" Random Forest"""

# Commented out IPython magic to ensure Python compatibility.


df_rf = pd.DataFrame()
nums_estimator = list(range(10, 100, 5))
max_depth = list(range(4, 13))
criterion = ['gini', 'entropy']

for t in range(20, 31):
    for ns in nums_estimator:
        for c in criterion:
            for md in max_depth:
                x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=t, random_state=125)
                rf = RandomForestClassifier(n_estimators=ns, criterion=c, max_depth=md)
                rf.fit(x_train, y_train.ravel())
                y_pred_rf = rf.predict(x_test)
                dict5 = {"Test Size": t, 'n-estimator': ns, 'Criterion': c, 'Max_Depth': md,
                         "Score": rf.score(x, y), "Accuracy_score": metrics.accuracy_score(y_test, y_pred_rf)}
                df_rf = df_rf.append(dict5, ignore_index=True)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=23, random_state=125)

# Random Forest
model = RandomForestClassifier(n_estimators=85, min_samples_split=8, min_samples_leaf=3, max_features='auto',
                               max_depth=50, bootstrap=True, random_state=125)
model.fit(x_train.values, y_train)

joblib.dump(model, 'db/randomforest.pkl')
