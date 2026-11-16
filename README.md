# Beijing Air Quality Analytics (2013–2017)

## Project Overview

This project focuses on analyzing air pollution patterns and meteorological conditions across 12 monitoring stations in Beijing, China, from March 2013 to February 2017.

Using the Beijing Multi-Site Air Quality Dataset, this project explores temporal pollution trends, compares PM2.5 concentrations across monitoring stations, and investigates the relationship between wind speed and PM2.5 concentrations.

The analysis involves data wrangling, exploratory data analysis (EDA), statistical correlation analysis, and interactive data visualization using Python.

An interactive dashboard was also developed using Streamlit to allow users to explore air quality conditions through customizable filters and visualizations.

## Business Questions

This project aims to answer the following three business questions:

1. **Monthly Pollution Trends:** How do monthly average PM2.5 and PM10 concentrations change across all 12 monitoring stations in Beijing during March 2013 – February 2017?

2. **Station Comparison:** Which monitoring stations recorded the highest and lowest average PM2.5 concentrations throughout the observation period?

3. **Wind Speed and Air Pollution:** How do PM2.5 concentrations vary across different wind speed categories, and what patterns can be observed across the 12 monitoring stations?

## Dataset

The dataset used in this project is the Beijing Multi-Site Air Quality Dataset, provided through Dicoding learning materials.

- **Dataset Name:** Beijing Multi-Site Air Quality Dataset
- **Source:** Dicoding (Google Drive)
- **Observation Period:** March 2013 – February 2017
- **Monitoring Stations:** 12 stations
- **Total Observations:** 420,768 records
- **Total Columns:** 19

### Dataset Source

[Download Beijing Air Quality Dataset](https://drive.google.com/file/d/1RhU3gJlkteaAQfyn9XOVAz7a5o1-etgr/view)

## Data Analysis Process

### 1. Data Gathering

- Imported the original CSV files from all 12 monitoring stations.
- Combined individual station datasets into one DataFrame.
- Created a datetime column by combining year, month, day, and hour.
- Prepared the consolidated dataset for further analysis.

### 2. Data Assessing

Several data quality issues were identified:

- **Missing Values:** 74,027 missing values were found across the dataset.
- **Potential Outliers:** Several numerical variables contained observations outside the IQR-based boundaries.
- **Duplicate Records:** No duplicate rows or duplicate station timestamps were identified.
- **Invalid Values:** No negative pollutant concentrations, negative wind speeds, or invalid datetime records were identified.

### 3. Data Cleaning

The following cleaning procedures were performed:

- Applied time-based interpolation to fill missing values within short gaps of up to three consecutive hours.
- Preserved longer missing gaps to avoid introducing potentially misleading values.
- Retained potential outliers because extreme environmental observations may represent genuine atmospheric conditions.
- Preserved the original observations and all 12 monitoring stations.

After cleaning, 25,026 missing values were successfully interpolated, while 49,001 missing values remained.

### 4. Exploratory Data Analysis (EDA)

The exploratory analysis focused on three main areas:

- **Temporal Analysis:** Examined monthly average PM2.5 and PM10 concentrations across the observation period.
- **Spatial Comparison by Station:** Compared average PM2.5 concentrations across all 12 monitoring stations.
- **Wind Speed Analysis:** Applied quartile-based binning to categorize wind speeds into Low, Moderate, High, and Very High groups, then compared their average PM2.5 concentrations.

### 5. Advanced Analysis

Pearson and Spearman correlation analyses were conducted to investigate relationships between air pollutants and meteorological variables.

- **Pearson Correlation:** Measures the strength and direction of linear relationships.
- **Spearman Correlation:** Measures the strength and direction of monotonic relationships.

Heatmaps were generated to visualize the correlation coefficients and identify relevant patterns.

### 6. Visualization and Explanatory Analysis

The project uses several visualizations to communicate the findings:

- Monthly PM2.5 and PM10 trend line chart.
- Average PM2.5 concentration comparison across monitoring stations.
- Average PM2.5 concentration by wind speed category.
- Pearson correlation heatmap.
- Spearman correlation heatmap.

## Key Findings

### 1. Monthly Pollution Trends

- The highest monthly average PM2.5 concentration was recorded in December 2015 at approximately **149.95 µg/m³**.
- The lowest monthly average PM2.5 concentration was recorded in February 2016 at approximately **42.85 µg/m³**.
- PM10 followed a similar pattern, reaching its highest monthly average in December 2015 at approximately **159.76 µg/m³** and its lowest in February 2016 at approximately **57.13 µg/m³**.

### 2. PM2.5 Concentration Across Monitoring Stations

- **Dongsi** recorded the highest average PM2.5 concentration at approximately **86.07 µg/m³**.
- **Dingling** recorded the lowest average PM2.5 concentration at approximately **66.00 µg/m³**.
- The comparison indicates differences in air pollution concentrations across monitoring locations.

### 3. Wind Speed and PM2.5 Relationship

The analysis revealed a decreasing pattern in average PM2.5 concentrations as wind speed categories increased.

| Wind Category | Average PM2.5 (µg/m³) |
|---|---:|
| Low | 102.35 |
| Moderate | 93.36 |
| High | 75.12 |
| Very High | 45.08 |

This pattern suggests that higher wind speeds are associated with lower PM2.5 concentrations in the analyzed observations.

### 4. Correlation Analysis

- PM10 showed a strong positive Spearman correlation with PM2.5, approximately **0.89**.
- Wind speed (WSPM) showed a negative Spearman correlation with PM2.5, approximately **-0.33**.

These findings describe statistical associations and do not establish causal relationships.

## Conclusion and Recommendations

Based on the analysis, several conclusions can be drawn:

1. Air pollution concentrations varied considerably throughout the observation period, with December 2015 recording the highest monthly average concentrations for both PM2.5 and PM10.
2. Pollution levels differed across monitoring stations, with Dongsi showing the highest average PM2.5 concentration and Dingling showing the lowest.
3. Higher wind speed categories were associated with lower average PM2.5 concentrations.
4. PM2.5 and PM10 exhibited a strong positive correlation, indicating that their concentrations tended to increase and decrease together.

### Recommended Action Items

- Prioritize air quality monitoring and pollution mitigation efforts in locations with consistently higher PM2.5 concentrations.
- Pay particular attention to periods with elevated monthly pollution levels.
- Incorporate meteorological conditions, especially wind speed, into air quality monitoring and forecasting considerations.
- Continue collecting air quality observations to support more comprehensive environmental assessments.

## Dashboard

An interactive dashboard was developed using Streamlit and Plotly.

Dashboard features include:

- Interactive date range filtering.
- Monitoring station selection.
- Air quality overview with KPI metrics.
- Monthly PM2.5 and PM10 trend visualization.
- PM2.5 comparison across monitoring stations.
- Wind speed and PM2.5 analysis.
- Pearson and Spearman correlation heatmaps.

## Technologies and Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Jupyter Notebook

## Project Structure

```text
submission/
│
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
│
├── data/
│   ├── [original station CSV files]
│
├── notebook/
│   └── notebook.ipynb
│
├── README.md
├── requirements.txt
└── url.txt
```

## How to Run the Dashboard Locally

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd submission
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit Dashboard

```bash
streamlit run dashboard/dashboard.py
```

The dashboard will automatically open in your default web browser.

If it does not open automatically, access it through:

```text
http://localhost:8501
```

## Author

Data Analysis Project – Dicoding

**Project:** Beijing Air Quality Analytics (2013–2017)