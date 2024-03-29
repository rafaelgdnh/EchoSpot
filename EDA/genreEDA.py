import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('DataFrames/dataset.csv')

# DATA PRE-PROCESSING ##

# Drops the first column by its position
df = df.drop(df.columns[0], axis=1)

# Normalization for numeric features of DataFrame
scaler = StandardScaler()
columns_to_scale = ['energy', 'loudness', 'speechiness', 'valence', 'liveness', 'tempo', 'danceability', 'acousticness', 'duration_ms', 'instrumentalness', 'popularity']
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])


# Checks for any missing values in the DataFrame
missing_values = df.isnull().sum()
print(missing_values)


# Exploratory Data Analysis (EDA) ##

# Descriptive statistics
print(df.describe())


# Defines list of numeric features
num_features = ['energy', 'loudness', 'speechiness', 'valence', 'liveness', 'tempo', 'danceability', 'acousticness', 'duration_ms', 'instrumentalness', 'popularity']

# Color palette for plotsTop
palette = sns.color_palette("hsv", len(num_features))

# Initializes matplotlib figure for KDE plot
plt.figure(figsize=(14, 8))

# Loops through features and plots KDE for each one
for i, feature in enumerate(num_features):
    sns.kdeplot(df[feature], label=feature)  # Add a label for the legend

# Adds title, x-label and legend to plot
plt.title('KDE of Song Features', fontsize=18)
plt.xlabel('Feature Values', fontsize=14)
plt.legend(title='Features')

# Saves figure
plt.savefig('plotsGenre/full_feature_distributions_kde.png', dpi=300)
plt.close()


# Initializes matplotlib figure for boxplot
plt.figure(figsize=(20, 15))

# Loops through features and creates a boxplot for each one
for i, feature in enumerate(num_features):
    plt.subplot(1, len(num_features), i+1)
    sns.boxplot(y=df[feature], color=palette[i])
    plt.xlabel(feature, fontsize=14, fontweight='bold')  # Increase font size and make it bold
    plt.ylabel('')  # Remove the y-axis labels

plt.suptitle('Boxplot Distribution for Various Song Features', fontsize=20, fontweight='bold')

plt.tight_layout()
plt.savefig('plotsGenre/full_feature_distributions_boxplot.png', dpi=300)
plt.close()


# Initializes matplotlib figure for histograms
plt.figure(figsize=(20, 15))

# Loops through features and creates a histogram for each one
for i, feature in enumerate(num_features):
    plt.subplot(1, len(num_features), i+1)
    sns.histplot(df[feature], color=palette[i], kde=False, bins=15)
    plt.xlabel(feature, fontsize=14, fontweight='bold')  # Increase font size and make it bold

plt.suptitle('Histogram Distribution for Various Song Features', fontsize=20, fontweight='bold')

plt.tight_layout()
plt.savefig('plotsGenre/full_feature_distributions_histogram.png', dpi=300)
plt.close()


# Drops 'track_id' column from DataFrame
df_without_id = df.drop(columns=['track_id', 'artists', 'album_name', 'track_name', 'explicit', 'track_genre'], errors='ignore')

# Calculates correlation matrix for the DataFrame without 'track_id'
corr_without_id = df_without_id.corr()

# Initializes the matplotlib figure for the heatmap
plt.figure(figsize=(12, 10))

# Creates a heatmap
sns.heatmap(corr_without_id, annot=True, fmt=".2f", cmap='coolwarm', square=True)

plt.title('Correlation Matrix of Song Features', fontsize=18)
plt.savefig('plotsGenre/full_correlation_matrix_heatmap.png', dpi=300)
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

# Create a DataFrame with the loadings and the names of the original variables
pca_loadings_df = pd.DataFrame(data=pca_loadings,
                               columns=num_features,
                               index=[f'Principal Component {i+1}' for i in range(pca_loadings.shape[0])])

# Writes DataFrame to a .csv file
pca_loadings_df.to_csv('DataFrames/full_loadings.csv')

plt.figure(figsize=(14, 10))
sns.heatmap(pca_loadings_df, cmap='viridis', annot=True, cbar_kws={"shrink": .82})

plt.title('PCA Component Loadings', fontsize=16)
plt.xlabel('Features', fontsize=14)
plt.xticks(rotation=45, ha="right")  # Rotate feature names for better readability
plt.yticks(fontsize=10)  # Adjust as needed

plt.tight_layout()  # Adjust layout
plt.savefig('plotsGenre/full_loadings_heatmap.png', dpi=300)
plt.close()


# Calculates mean of numeric features by genre
genre_feature_means = df.groupby('track_genre')[num_features].mean()

# Split genre means into 3 groups to prevent processing issues
group1 = genre_feature_means.iloc[:38, :]
group2 = genre_feature_means.iloc[38:76, :]
group3 = genre_feature_means.iloc[76:, :]

# Creates a heatmap for each group and saves as .png
for i, group in enumerate([group1, group2, group3], start=1):
    plt.figure(figsize=(10, 15))  # Adjust the size as needed
    sns.heatmap(group, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title(f'Heatmap of Numeric Features for Group {i}')
    plt.xlabel('Numeric Features')
    plt.ylabel('Genres')
    plt.xticks(rotation=45)  # Rotate the feature names for better readability
    plt.yticks(rotation=0)  # Ensure genre names are horizontal for readability
    plt.tight_layout()  # Adjust layout
    plt.savefig(f'plotsGenre/genre_heatmap_group_{i}.png')
    plt.close()




