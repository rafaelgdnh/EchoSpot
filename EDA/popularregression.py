import statsmodels.api as sm
import pandas as pd
from sklearn.preprocessing import StandardScaler


df = pd.read_csv('../DataFrames/dataset.csv')

# DATA PRE-PROCESSING ##

# Drops the first column by its position
df = df.drop(df.columns[0], axis=1)

# Normalization for numeric features of DataFrame
scaler = StandardScaler()
columns_to_scale = ['energy', 'loudness', 'speechiness', 'valence', 'liveness', 'tempo', 'danceability', 'acousticness', 'duration_ms', 'instrumentalness', 'popularity']
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# List of numeric features aside from 'popularity' feature
num_features_no_pop = ['energy', 'loudness', 'speechiness', 'valence', 'liveness', 'tempo', 'danceability', 'acousticness', 'duration_ms', 'instrumentalness']

X = df[num_features_no_pop]  # List of numeric feature columns
y = df['popularity']  # Popularity scores

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
with open('../EDA/regression_summary.txt', 'w') as f:
    f.write(summary.as_text())