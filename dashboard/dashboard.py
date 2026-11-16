
# ============================================================
# BEIJING AIR QUALITY ANALYTICS DASHBOARD
# ============================================================

# 1. Import Libraries
import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path


# ============================================================
# 2. Page Configuration
# ============================================================

st.set_page_config(
    page_title="Beijing Air Quality Dashboard",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 3. Load Dataset
# ============================================================

DATA_PATH = Path(__file__).parent / "main_data.csv"


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    data["datetime"] = pd.to_datetime(data["datetime"])

    return data


try:
    df = load_data()

except FileNotFoundError:
    st.error("Dataset main_data.csv tidak ditemukan.")
    st.stop()

except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca dataset: {e}")
    st.stop()


# ============================================================
# 4. Dashboard Header
# ============================================================

st.title("🌫️ Beijing Air Quality Analytics")

st.markdown(
    """
    Interactive dashboard for exploring air pollution
    patterns and meteorological conditions across
    12 monitoring stations in Beijing.

    **Observation Period:** March 2013 – February 2017
    """
)

st.divider()



# ============================================================
# 5. SIDEBAR FILTERS
# ============================================================

st.sidebar.title("Dashboard Filters")

st.sidebar.markdown(
    "Customize the data displayed in the dashboard."
)

# Date filter
min_date = df["datetime"].min().date()
max_date = df["datetime"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Station filter
available_stations = sorted(
    df["station"].unique().tolist()
)

selected_stations = st.sidebar.multiselect(
    "Select Monitoring Stations",
    options=available_stations,
    default=available_stations
)

# Apply filters
if len(selected_dates) == 2 and selected_stations:

    start_date, end_date = selected_dates

    filtered_df = df[
        (df["datetime"].dt.date >= start_date) &
        (df["datetime"].dt.date <= end_date) &
        (df["station"].isin(selected_stations))
    ].copy()

else:
    filtered_df = pd.DataFrame()

st.sidebar.divider()

st.sidebar.caption(
    "Beijing Air Quality Analytics | 2013–2017"
)


# ============================================================
# 6. FILTERED DATA OVERVIEW
# ============================================================

st.subheader("Air Quality Overview")

if filtered_df.empty:

    st.warning(
        "No data available for the selected filters. "
        "Please adjust your date range or station selection."
    )
    st.stop()

# Calculate metrics
total_observations = len(filtered_df)

total_stations = filtered_df["station"].nunique()

avg_pm25 = filtered_df["PM2.5"].mean()

avg_pm10 = filtered_df["PM10"].mean()

# Display KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Observations",
        value=f"{total_observations:,}"
    )

with col2:
    st.metric(
        label="Monitoring Stations",
        value=total_stations
    )

with col3:
    st.metric(
        label="Average PM2.5 (µg/m³)",
        value=f"{avg_pm25:.2f}"
    )

with col4:
    st.metric(
        label="Average PM10 (µg/m³)",
        value=f"{avg_pm10:.2f}"
    )

st.divider()


# ============================================================
# 7. FILTERED DATA PREVIEW
# ============================================================

with st.expander("View Filtered Dataset"):

    st.write(
        f"Displaying {len(filtered_df):,} observations."
    )

    st.dataframe(
        filtered_df.head(10),
        use_container_width=True
    )


# ============================================================
# 8. MONTHLY POLLUTION TRENDS
# ============================================================

st.subheader("Monthly Pollution Trends")

st.markdown(
    """
    Explore monthly changes in PM2.5 and PM10 concentrations
    across the selected monitoring stations.
    """
)

# Aggregate monthly pollutant concentrations
monthly_data = (
    filtered_df
    .set_index("datetime")
    .resample("MS")[["PM2.5", "PM10"]]
    .mean()
    .reset_index()
)

# Convert data into long format
monthly_long = monthly_data.melt(
    id_vars="datetime",
    value_vars=["PM2.5", "PM10"],
    var_name="Pollutant",
    value_name="Average Concentration"
)

# Create interactive line chart
fig_monthly = px.line(
    monthly_long,
    x="datetime",
    y="Average Concentration",
    color="Pollutant",
    markers=True,
    title="Monthly Average PM2.5 and PM10 Concentrations",
    labels={
        "datetime": "Month",
        "Average Concentration": "Concentration (µg/m³)",
        "Pollutant": "Pollutant"
    },
    color_discrete_map={
        "PM2.5": "#3B82F6",
        "PM10": "#F97316"
    }
)

fig_monthly.update_layout(
    template="plotly_white",
    hovermode="x unified",
    legend_title="Pollutant",
    height=480
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# ============================================================
# 9. STATION COMPARISON
# ============================================================

st.divider()

st.subheader("PM2.5 Concentration by Monitoring Station")

st.markdown(
    """
    Compare average PM2.5 concentrations across
    the selected monitoring stations.
    """
)

# Calculate average PM2.5 for each station
station_data = (
    filtered_df
    .groupby("station", as_index=False)
    .agg(
        PM25_mean=("PM2.5", "mean"),
        Observation_Count=("PM2.5", "count")
    )
    .sort_values("PM25_mean", ascending=True)
)

# Create horizontal bar chart
fig_station = px.bar(
    station_data,
    x="PM25_mean",
    y="station",
    orientation="h",
    text="PM25_mean",
    color="PM25_mean",
    color_continuous_scale="Blues",
    title="Average PM2.5 Concentration Across Monitoring Stations",
    labels={
        "PM25_mean": "Average PM2.5 (µg/m³)",
        "station": "Monitoring Station"
    },
    hover_data={
        "PM25_mean": ":.2f",
        "Observation_Count": ":,",
        "station": True
    }
)

fig_station.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig_station.update_layout(
    template="plotly_white",
    height=550,
    coloraxis_showscale=False,
    xaxis_title="Average PM2.5 Concentration (µg/m³)",
    yaxis_title="Monitoring Station"
)

st.plotly_chart(
    fig_station,
    use_container_width=True
)


# ============================================================
# 10. HIGHEST AND LOWEST PM2.5 STATIONS
# ============================================================

if not station_data.empty:

    highest_station = station_data.loc[
        station_data["PM25_mean"].idxmax()
    ]

    lowest_station = station_data.loc[
        station_data["PM25_mean"].idxmin()
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Highest PM2.5 Station",
            value=highest_station["station"]
    )
    st.caption(
            f'Average concentration: {highest_station["PM25_mean"]:.2f} µg/m³'
    )

    with col2:
        st.metric(
            label="Lowest PM2.5 Station",
            value=lowest_station["station"]
        )
        st.caption(
            f'Average concentration: {lowest_station["PM25_mean"]:.2f} µg/m³'
        )
        

# ============================================================
# 11. WIND SPEED AND PM2.5 ANALYSIS
# ============================================================

st.divider()

st.subheader("Wind Speed & PM2.5 Analysis")

st.markdown(
    """
    Explore the relationship between wind speed categories
    and average PM2.5 concentrations across selected stations.
    """
)

# Prepare wind analysis dataset
wind_df = filtered_df.dropna(
    subset=["WSPM", "PM2.5"]
).copy()

if not wind_df.empty:

    # Calculate quartile boundaries
    wind_bins = (
        wind_df["WSPM"]
        .quantile([0, 0.25, 0.50, 0.75, 1.00])
        .unique()
    )

    wind_bins = sorted(wind_bins)

    # Create category labels
    wind_labels = [
        "Low",
        "Moderate",
        "High",
        "Very High"
    ][:len(wind_bins) - 1]

    # Apply quartile-based binning
    wind_df["Wind_Category"] = pd.cut(
        wind_df["WSPM"],
        bins=wind_bins,
        labels=wind_labels,
        include_lowest=True
    )

    # Aggregate PM2.5 by wind category
    wind_summary = (
        wind_df
        .groupby("Wind_Category", observed=False)
        .agg(
            PM25_mean=("PM2.5", "mean"),
            Observation_Count=("PM2.5", "count"),
            Wind_Speed_Mean=("WSPM", "mean")
        )
        .reset_index()
        .dropna(subset=["PM25_mean"])
    )

    # Create interactive bar chart
    fig_wind = px.bar(
        wind_summary,
        x="Wind_Category",
        y="PM25_mean",
        text="PM25_mean",
        color="Wind_Category",
        title="Average PM2.5 Concentration by Wind Speed Category",
        labels={
            "Wind_Category": "Wind Speed Category",
            "PM25_mean": "Average PM2.5 Concentration (µg/m³)"
        },
        hover_data={
            "PM25_mean": ":.2f",
            "Observation_Count": ":,",
            "Wind_Speed_Mean": ":.2f"
        },
        category_orders={
            "Wind_Category": [
                "Low", "Moderate", "High", "Very High"
            ]
        },
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig_wind.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_wind.update_layout(
        template="plotly_white",
        height=480,
        showlegend=False
    )

    st.plotly_chart(
        fig_wind,
        use_container_width=True
    )

    # Display summary table
    with st.expander("View Wind Speed Analysis Details"):
        st.dataframe(
            wind_summary,
            use_container_width=True,
            hide_index=True
        )

else:
    st.warning("No wind speed data available for the selected filters.")


# ============================================================
# 12. CORRELATION ANALYSIS
# ============================================================

st.divider()

st.subheader("Correlation Analysis")

st.markdown(
    """
    Examine the relationships between air pollutants
    and meteorological variables using Pearson and
    Spearman correlation methods.
    """
)

# Define variables for correlation analysis
correlation_columns = [
    "PM2.5", "PM10", "SO2", "NO2", "CO", "O3",
    "TEMP", "PRES", "DEWP", "RAIN", "WSPM"
]

# Calculate Pearson and Spearman correlation
pearson_corr = filtered_df[
    correlation_columns
].corr(method="pearson")

spearman_corr = filtered_df[
    correlation_columns
].corr(method="spearman")

# Create two tabs for correlation methods
tab1, tab2 = st.tabs([
    "Pearson Correlation",
    "Spearman Correlation"
])

# Pearson Heatmap
with tab1:

    st.markdown(
        "**Pearson Correlation Heatmap**"
    )

    st.caption(
        "Measures the strength and direction of linear relationships."
    )

    fig_pearson = px.imshow(
        pearson_corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Pearson Correlation of Air Quality and Meteorological Variables"
    )

    fig_pearson.update_layout(
        template="plotly_white",
        height=750
    )

    st.plotly_chart(
        fig_pearson,
        use_container_width=True
    )

# Spearman Heatmap
with tab2:

    st.markdown(
        "**Spearman Correlation Heatmap**"
    )

    st.caption(
        "Measures the strength and direction of monotonic relationships."
    )

    fig_spearman = px.imshow(
        spearman_corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Spearman Correlation of Air Quality and Meteorological Variables"
    )

    fig_spearman.update_layout(
        template="plotly_white",
        height=750
    )

    st.plotly_chart(
        fig_spearman,
        use_container_width=True
    )

# Display correlation with PM2.5
st.divider()

st.markdown("### Correlation with PM2.5")

col1, col2 = st.columns(2)

with col1:

    st.markdown("**Pearson Correlation**")

    pearson_pm25 = (
        pearson_corr["PM2.5"]
        .drop("PM2.5")
        .sort_values(ascending=False)
        .to_frame("Correlation")
    )

    st.dataframe(
        pearson_pm25.style.format("{:.3f}"),
        use_container_width=True
    )

with col2:

    st.markdown("**Spearman Correlation**")

    spearman_pm25 = (
        spearman_corr["PM2.5"]
        .drop("PM2.5")
        .sort_values(ascending=False)
        .to_frame("Correlation")
    )

    st.dataframe(
        spearman_pm25.style.format("{:.3f}"),
        use_container_width=True
    )


# ============================================================
# 13. KEY FINDINGS & INSIGHTS
# ============================================================

st.divider()

st.subheader("Key Findings & Insights")

st.markdown(
    """
    Summary of the main findings from the air quality
    and meteorological analysis based on the selected filters.
    """
)

# ------------------------------------------------------------
# 1. Monthly PM2.5 Analysis
# ------------------------------------------------------------

monthly_pm25 = monthly_data.dropna(
    subset=["PM2.5"]
)

if not monthly_pm25.empty:

    highest_month = monthly_pm25.loc[
        monthly_pm25["PM2.5"].idxmax()
    ]

    lowest_month = monthly_pm25.loc[
        monthly_pm25["PM2.5"].idxmin()
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Highest Monthly PM2.5**")

        st.metric(
            label=pd.to_datetime(
                highest_month["datetime"]
            ).strftime("%B %Y"),
            value=f'{highest_month["PM2.5"]:.2f} µg/m³'
        )

    with col2:
        st.markdown("**Lowest Monthly PM2.5**")

        st.metric(
            label=pd.to_datetime(
                lowest_month["datetime"]
            ).strftime("%B %Y"),
            value=f'{lowest_month["PM2.5"]:.2f} µg/m³'
        )

    st.caption(
        "Monthly averages are calculated from the selected "
        "date range and monitoring stations."
    )

# ------------------------------------------------------------
# 2. Correlation Insights
# ------------------------------------------------------------

st.markdown("### Pollutant Correlation Insights")

pm25_correlations = (
    pearson_corr["PM2.5"]
    .drop("PM2.5")
    .dropna()
)

if not pm25_correlations.empty:

    strongest_positive = pm25_correlations.idxmax()
    strongest_negative = pm25_correlations.idxmin()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Strongest Positive Correlation**")

        st.metric(
            label=strongest_positive,
            value=f"{pm25_correlations.max():.3f}"
        )

    with col2:
        st.markdown("**Strongest Negative Correlation**")

        st.metric(
            label=strongest_negative,
            value=f"{pm25_correlations.min():.3f}"
        )

# ------------------------------------------------------------
# 3. Wind Speed Insights
# ------------------------------------------------------------

st.markdown("### Wind Speed Insights")

if "wind_summary" in locals() and not wind_summary.empty:

    lowest_wind_pm25 = wind_summary.loc[
        wind_summary["PM25_mean"].idxmin()
    ]

    st.info(
        f'Wind category **{lowest_wind_pm25["Wind_Category"]}** '
        f'shows the lowest average PM2.5 concentration, '
        f'with {lowest_wind_pm25["PM25_mean"]:.2f} µg/m³.'
    )

# ------------------------------------------------------------
# 4. Overall Interpretation
# ------------------------------------------------------------

st.markdown("### Overall Interpretation")

st.write(
    f"""
    Based on the selected monitoring stations and date range,
    the average PM2.5 concentration is **{avg_pm25:.2f} µg/m³**,
    while the average PM10 concentration is **{avg_pm10:.2f} µg/m³**.

    These findings provide an overview of air pollution
    conditions and their relationship with meteorological
    variables in Beijing.
    """
)
