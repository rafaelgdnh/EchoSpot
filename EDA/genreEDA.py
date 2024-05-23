import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
import numpy as np


df = pd.read_csv('../DataFrames/dataset.csv')

# DATA PRE-PROCESSING ##

# Drops the first column by its position
df = df.drop(df.columns[0], axis=1)

# Normalization for numeric features of DataFrame
scaler = StandardScaler()
columns_to_scale = ['energy', 'loudness', 'speechiness', 'valence', 'liveness', 'tempo', 'danceability',
                    'acousticness', 'duration_ms', 'instrumentalness', 'popularity']
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# Checks for any missing values in the DataFrame
missing_values = df.isnull().sum()
print(missing_values)


# Exploratory Data Analysis (EDA) ##

# Descriptive statistics
df.describe().to_csv("../DataFrames/B_summary_statistics.csv", float_format='%.2f')

# Re-defines list of numeric features
num_features = ['energy', 'loudness', 'speechiness', 'valence', 'liveness', 'tempo', 'danceability',
                'acousticness', 'duration_ms', 'instrumentalness', 'popularity']

# Color palette for plots
palette = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf',  # blue-teal
    '#39FF14'   # neon green
]

# Initializes matplotlib figure for KDE plot
plt.figure(figsize=(14, 8))

# Loops through features and plots KDE for each one
for i, feature in enumerate(num_features):
    sns.kdeplot(df[feature], label=feature, color=palette[i])

# Adds title, x-label and legend to plot
plt.title('KDE of Song Features', fontsize=18)
plt.xlabel('Feature Values', fontsize=14)
plt.legend(title='Features')

# Sets x-axis limit to improve readability
plt.xlim(-10, 10)

for feature in num_features:
    data = df[feature]

    # Instantiates and fits KDE model
    kde = gaussian_kde(data)

    # Computes range of data (min and max)
    min_x = data.min()
    max_x = data.max()

    # Finds mode
    x = np.linspace(min_x, max_x, 1000)
    y = kde(x)
    peak_y = y.max()
    mode_x = x[y.argmax()]

    print(f"{feature.capitalize()}:")
    print(f"  Min x: {min_x:.2f}")
    print(f"  Max x: {max_x:.2f}")
    print(f"  Peak y: {peak_y:.2f} at x (mode): {mode_x:.2f}\n")

# Saves figure
plt.savefig('../plotsGenre/full_feature_distributions_kde.png', dpi=150)
plt.close()


# Initializes matplotlib figure for boxplot
plt.figure(figsize=(20, 15))

# Loops through features and creates boxplot for each one
for i, feature in enumerate(num_features):
    plt.subplot(1, len(num_features), i+1)
    bp = sns.boxplot(y=df[feature], color=palette[i])

    # Increases median line thickness and color
    for median_line in bp.findobj(plt.Line2D):
        if median_line.get_linestyle() == '-':  # Check if line is median line
            median_line.set_color('black')  # Changes median line color to black
            median_line.set_linewidth(3)  # Increases median line thickness

    plt.xlabel(feature, fontsize=14, fontweight='bold')  # Increases font size and makes it bold
    plt.ylabel('')  # Removes y-axis labels

plt.suptitle('Boxplot Distribution for Various Song Features', fontsize=20, fontweight='bold')
plt.tight_layout()
plt.savefig('../plotsGenre/full_feature_distributions_boxplot.png', dpi=300)
plt.close()


# Initializes matplotlib figure for histograms
plt.figure(figsize=(20, 15))

# Loops through features and creates histogram for each one
for i, feature in enumerate(num_features):
    plt.subplot(1, len(num_features), i+1)
    sns.histplot(df[feature], color=palette[i], kde=False, bins=15)
    plt.xlabel(feature, fontsize=14, fontweight='bold')

plt.suptitle('Histogram Distribution for Various Song Features', fontsize=20, fontweight='bold')
plt.tight_layout()
plt.savefig('../plotsGenre/full_feature_distributions_histogram.png', dpi=300)
plt.close()


# Drops non-numeric columns from DataFrame
df_without_id = df.drop(columns=['track_id', 'artists', 'album_name', 'track_name', 'explicit', 'track_genre'],
                        errors='ignore')

# Calculates correlation matrix for DataFrame without 'track_id'
corr_without_id = df_without_id.corr()

# Initializes the matplotlib figure for the heatmap
plt.figure(figsize=(12, 10))

# Creates mask for the upper triangle
mask = np.triu(np.ones_like(corr_without_id, dtype=bool))

# Creates a heatmap
sns.heatmap(corr_without_id, annot=True, fmt=".2f", cmap='coolwarm', mask=mask, square=True)
plt.title('Correlation Matrix of Song Features', fontsize=18)
plt.savefig('../plotsGenre/full_correlation_matrix_heatmap.png', dpi=300)
plt.close()


# Extracts features for PCA
x = df.loc[:, num_features].values

# Standardizes features
x = StandardScaler().fit_transform(x)

# PCA set to 6 principal components
pca = PCA(n_components=6)
principalComponents = pca.fit_transform(x)

# Create DataFrame with principal components
pca_df = pd.DataFrame(data=principalComponents, columns=['Principal Component 1', 'Principal Component 2',
                                                         "Principal Component 3", 'Principal Component 4',
                                                         "Principal Component 5", 'Principal Component 6'])

print(f"Explained variance by component: {pca.explained_variance_ratio_}")

# Calculates PCA loadings for each component
pca_loadings = pca.components_

# Creates DataFrame with loadings and names of the original variables
pca_loadings_df = pd.DataFrame(data=pca_loadings,
                               columns=num_features,
                               index=[f'Principal Component {i+1}' for i in range(pca_loadings.shape[0])])

# Writes DataFrame to a .csv file
pca_loadings_df.to_csv('../DataFrames/full_loadings.csv')

plt.figure(figsize=(14, 10))
sns.heatmap(pca_loadings_df, cmap='viridis', annot=True, cbar_kws={"shrink": .82})
plt.title('PCA Component Loadings', fontsize=16)
plt.xlabel('Features', fontsize=14)
plt.xticks(rotation=45, ha="right")
plt.yticks(fontsize=10)
plt.tight_layout()
plt.savefig('../plotsGenre/full_loadings_heatmap.png', dpi=300)
plt.close()


# Calculates mean of numeric features by genre
genre_feature_means = df.groupby('track_genre')[num_features].mean()

# Splits genre means into 3 groups to prevent processing issues
group1 = genre_feature_means.iloc[:38, :]
group2 = genre_feature_means.iloc[38:76, :]
group3 = genre_feature_means.iloc[76:, :]

# Creates heatmap for each group and saves as .png
for i, group in enumerate([group1, group2, group3], start=1):
    plt.figure(figsize=(10, 15))
    sns.heatmap(group, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title(f'Heatmap of Numeric Features for Group {i}')
    plt.xlabel('Numeric Features')
    plt.ylabel('Genres')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f'../plotsGenre/genre_heatmap_group_{i}.png')
    plt.close()
