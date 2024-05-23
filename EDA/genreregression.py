import statsmodels.api as sm
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder


df = pd.read_csv('../DataFrames/dataset.csv')

# DATA PRE-PROCESSING ##

# Drops first column by its position
df = df.drop(df.columns[0], axis=1)

# Normalization for numeric features of DataFrame
scaler = StandardScaler()
columns_to_scale = ['energy', 'loudness', 'speechiness', 'valence', 'liveness', 'tempo', 'danceability', 'acousticness', 'duration_ms', 'instrumentalness', 'popularity']
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# Creating labelEncoder
le = LabelEncoder()

# Converting string labels into numbers
df['labeled_genre'] = le.fit_transform(df['track_genre'])

X = df[columns_to_scale]  # List of numeric feature columns
y = df['labeled_genre']  # Numerical values of genres

# Adds constant to the model (intercept term)
X = sm.add_constant(X)

# Creates OLS model
model = sm.OLS(y, X)

# Fits model
results = model.fit()

# Gets summary of regression
summary = results.summary()

# Prints out summary to the console
print(summary)

# Exports summary to a .txt
with open('../EDA/genre_regression_summary.txt', 'w') as f:
    f.write(summary.as_text())


