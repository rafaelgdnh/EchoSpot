import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


df = pd.read_csv('DataFrames/top500songs.csv')

# DATA PRE-PROCESSING ##

# Drops the first column by its position
df = df.drop(df.columns[0], axis=1)

# Normalization for numeric features of DataFrame
scaler = StandardScaler()
columns_to_scale = ['energy', 'loudness', 'speechiness', 'valence', 'liveness', 'tempo', 'danceability', 'acousticness', 'duration_ms', 'instrumentalness', 'popularity']
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])


# Converts string representation of list into actual list
df['market'] = df['market'].apply(ast.literal_eval)

# Initializes an empty dictionary to store market counts
market_dict = {}

# Iterates over each row and updates the dictionary with counts
for market_list in df['market']:
    for country_code in market_list:
        market_dict[country_code] = market_dict.get(country_code, 0) + 1

print(market_dict)

# Calculates market counts for each row
df['market_count'] = df['market'].apply(len)

# Drops the original 'market' column
df.drop('market', axis=1, inplace=True)


# Checks for any missing values in the DataFrame
missing_values = df.isnull().sum()
print(missing_values)


# Creates title, labels and plot for KDE of Market Count
plt.figure(figsize=(10, 6))
sns.kdeplot(df['market_count'].dropna(), bw_adjust=0.5)
plt.title('KDE of Market Count')
plt.xlabel('Market Count')
plt.ylabel('Density')

# Saves plot as .png file
plt.savefig('plotsTop/market_count_distribution.png', dpi=300)
plt.show()


# Replaces "0" with NaN
df['market_count'].replace(0, np.nan, inplace=True)

# Fills with median due to skewed KDE plot
df['market_count'].fillna(df['market_count'].median(), inplace=True)
print(df['market_count'])


# Exploratory Data Analysis (EDA) ##

# Descriptive statistics
print(df.describe())


# Defines list of numeric features
num_features = ['energy', 'loudness', 'speechiness', 'valence', 'liveness', 'tempo', 'danceability', 'acousticness', 'duration_ms', 'instrumentalness', 'popularity']

# Color palette for plotsTop
palette = sns.color_palette("hsv", len(num_features))

# Initializes matplotlib figure for KDE plot
plt.figure(figsize=(14, 8))

# Loops through features and plots KDE for each
for i, feature in enumerate(num_features):
    sns.kdeplot(df[feature], label=feature)  # Add a label for the legend

# Adds title, labels and legend to plot
plt.title('KDE of Song Features', fontsize=18)
plt.xlabel('Feature Values', fontsize=14)
plt.legend(title='Features')

# Saves figure
plt.savefig('plotsTop/feature_distributions_kde.png', dpi=300)
plt.close()


# Initializes matplotlib figure for boxplot
plt.figure(figsize=(20, 15))

# Loops through features and creates a boxplot for each one
for i, feature in enumerate(num_features):
    plt.subplot(1, len(num_features), i+1)
    sns.boxplot(y=df[feature], color=palette[i])
    plt.xlabel(feature, fontsize=14, fontweight='bold')  # Increase font size and make it bold
    plt.ylabel('')  # Remove the y-axis labels

# Adds title to plot
plt.suptitle('Boxplot Distribution for Various Song Features', fontsize=20, fontweight='bold')

plt.tight_layout()
plt.savefig('plotsTop/feature_distributions_boxplot.png', dpi=300)
plt.close()


# Initializes matplotlib figure for histograms
plt.figure(figsize=(20, 15))

# Loops through features and creates a histogram for each one
for i, feature in enumerate(num_features):
    plt.subplot(1, len(num_features), i+1)
    sns.histplot(df[feature], color=palette[i], kde=False, bins=15)
    plt.xlabel(feature, fontsize=14, fontweight='bold')  # Increase font size and make it bold

# Adds title to the plot
plt.suptitle('Histogram Distribution for Various Song Features', fontsize=20, fontweight='bold')

plt.tight_layout()
plt.savefig('plotsTop/feature_distributions_histogram.png', dpi=300)
plt.close()


# Drops 'track_id' column from DataFrame
df_without_id = df.drop(columns=['track_id'], errors='ignore')

# Calculates correlation matrix for the DataFrame without 'track_id'
corr_without_id = df_without_id.corr()

# Initializes matplotlib figure for the heatmap
plt.figure(figsize=(12, 10))

# Creates a heatmap with a title
sns.heatmap(corr_without_id, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Correlation Matrix of Song Features', fontsize=18)

plt.savefig('plotsTop/correlation_matrix_heatmap.png', dpi=300)
plt.close()


# Converts market_dict to a list of (country, count) tuples and sorts by count
market_counts = sorted(market_dict.items(), key=lambda item: item[1], reverse=True)

# Extracts top 5 and bottom 5 countries
top_5_countries = market_counts[:5]
bottom_5_countries = market_counts[-5:]

# Combines top 5 and bottom 5 for a plot
combined_countries = top_5_countries + bottom_5_countries

# Separates the country codes and counts for plotting
countries, counts = zip(*combined_countries)

# Creates horizontal bar chart
plt.figure(figsize=(10, 8))

# Sets different colors for top (green) and bottom (yellow) countries
colors = ['green' if i < 5 else '#FCD12A' for i in range(len(combined_countries))]

plt.barh(countries, counts, color=colors)
plt.xlabel('Market Count')
plt.title('Top 5 and Bottom 5 Countries by Market Count')

# Adds data labels to each bar
for index, value in enumerate(counts):
    plt.text(value, index, str(value))

plt.savefig('plotsTop/market_count_bar_chart.png', dpi=300)
plt.close()


# Extracting features for PCA
x = df.loc[:, num_features].values

# Standardizing the features
x = StandardScaler().fit_transform(x)

# PCA set to 6 principal components
pca = PCA(n_components=6)
principalComponents = pca.fit_transform(x)

# Create a DataFrame with the principal components
pca_df = pd.DataFrame(data=principalComponents, columns=['Principal Component 1', 'Principal Component 2',
                                                         "Principal Component 3", 'Principal Component 4',
                                                         "Principal Component 5", 'Principal Component 6'])

print(f"Explained variance by component: {pca.explained_variance_ratio_}")

# Calculates the PCA loadings (i.e., the weights) for each component
pca_loadings = pca.components_

# Creates a DataFrame with the loadings and the names of the original variables
pca_loadings_df = pd.DataFrame(data=pca_loadings,
                               columns=num_features,
                               index=[f'Principal Component {i+1}' for i in range(pca_loadings.shape[0])])

# Writes DataFrame to a .csv file
pca_loadings_df.to_csv('DataFrames/loadings.csv')

# Sets figure size
plt.figure(figsize=(14, 10))
sns.heatmap(pca_loadings_df, cmap='viridis', annot=True, cbar_kws={"shrink": .82})

plt.title('PCA Component Loadings', fontsize=16)
plt.xlabel('Features', fontsize=14)
plt.xticks(rotation=45, ha="right")  # Rotate feature names for better readability
plt.yticks(fontsize=10)  # Adjust as needed

plt.tight_layout()  # Adjust layout
plt.savefig('plotsTop/loadings_heatmap.png', dpi=300)
plt.close()



