# EchoSpot

EchoSpot is a Python-based project for analyzing and visualizing musical features. This repository contains code for loading and preprocessing data and generating insightful visualizations. Code for the website, EchoSpot, is also included.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Contributing](#contributing)

## Features

- **Data Preprocessing**: Clean and prepare the musical dataset.
- **PCA Analysis**: Apply PCA to reduce the dimensionality of the dataset.
- **Visualization**: Generate plots such as heatmaps and KDEs to visualize data.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/EchoSpot.git
    cd EchoSpot
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your dataset (CSV file) in the `data/` directory.

2. Run the PCA analysis script:
    ```bash
    python pca_analysis.py
    ```

3. Generate visualizations:
    ```bash
    python genreEDA.py
    ```

    or

    ```bash
    python topsongsEDA.py
    ```

## Data

The dataset used for this analysis should be in CSV format and contain the following musical features:

- energy
- loudness
- speechiness
- valence
- liveness
- tempo
- danceability
- acousticness
- duration_ms
- instrumentalness
- popularity

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch`
5. Submit a pull request.


If you'd like to read more about the analysis, check out the PDF in the repo!



   
