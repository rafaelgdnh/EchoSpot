import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier  # or DecisionTreeRegressor for regression tasks
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report


df = pd.read_csv('../DataFrames/dataset.csv')

# DATA PRE-PROCESSING ##

# Drops the first column by its position
df = df.drop(df.columns[0], axis=1)

bins = [0, 33, 66, 100]  # Defining custom bin edges
labels = ['Low', 'Medium', 'High']
df['popularity_bin'] = pd.cut(df['popularity'], bins=bins, labels=labels, include_lowest=True)


# Normalization for numeric features of DataFrame
scaler = StandardScaler()
columns_to_scale = ['energy', 'loudness', 'speechiness', 'valence', 'liveness', 'tempo', 'danceability', 'acousticness', 'duration_ms', 'instrumentalness']
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

X = df[columns_to_scale]  # List of numeric feature columns
y = df['popularity_bin']  # Numerical bins for popularity

# Assuming X and y are your features and target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit the decision tree
tree = DecisionTreeClassifier(max_depth=20, random_state=42)  # max_depth is optional
tree.fit(X_train, y_train)

# Predictions
predictions = tree.predict(X_test)

# Confusion Matrix
cm = confusion_matrix(y_test, predictions)
print("Confusion Matrix:")
print(cm)

# Accuracy
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.2f}")

# Precision, Recall, and F1 Score
report = classification_report(y_test, predictions)
print("Classification Report:")
print(report)
