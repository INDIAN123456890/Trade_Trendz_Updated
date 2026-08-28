import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import warnings

warnings.filterwarnings("ignore")
sns.set(color_codes=True)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Trade Trendz",
    page_icon="📈",
    layout="wide"
)

st.header("📈 TRADE TRENDZ 📉")

st.markdown(
    "<style>div.block-container{padding-top:3rem;}</style>",
    unsafe_allow_html=True
)

st.title("Google Stock Market Analysis")


# =========================================================
# DATA PREPROCESSING
# =========================================================

def preprocess_data(df):

    preprocessing_report = []

    # -----------------------------------------------------
    # 1. Remove completely empty rows
    # -----------------------------------------------------

    initial_rows = len(df)

    df = df.dropna(how="all").copy()

    removed_empty_rows = initial_rows - len(df)

    if removed_empty_rows > 0:
        preprocessing_report.append(
            f"Removed {removed_empty_rows} completely empty rows."
        )


    # -----------------------------------------------------
    # 2. Remove duplicate rows
    # -----------------------------------------------------

    duplicate_rows = df.duplicated().sum()

    if duplicate_rows > 0:

        df = df.drop_duplicates().copy()

        preprocessing_report.append(
            f"Removed {duplicate_rows} duplicate rows."
        )
    else:

        preprocessing_report.append(
            "No duplicate rows found."
        )


    # -----------------------------------------------------
    # 3. Check Date column
    # -----------------------------------------------------

    if "Date" not in df.columns:

        st.error(
            "Invalid dataset: 'Date' column is missing."
        )

        return None, preprocessing_report

    # Convert Date to datetime.
    # Invalid dates become NaT.

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )


    # -----------------------------------------------------
    # 4. Remove invalid/missing dates
    # -----------------------------------------------------

    invalid_dates = df["Date"].isna().sum()

    if invalid_dates > 0:

        df = df.dropna(subset=["Date"]).copy()

        preprocessing_report.append(
            f"Removed {invalid_dates} rows with "
            f"invalid or missing Date values."
        )
    else:

        preprocessing_report.append(
            "Date column validated successfully."
        )


    # -----------------------------------------------------
    # 5. Expected numerical columns
    # -----------------------------------------------------

    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume"
    ]


    # -----------------------------------------------------
    # 6. Convert numerical columns
    # -----------------------------------------------------

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )


    # -----------------------------------------------------
    # 7. Replace invalid price values
    # -----------------------------------------------------

    price_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close"
    ]

    for column in price_columns:

        if column in df.columns:

            invalid_values = (
                df[column].notna()
                & (df[column] <= 0)
            ).sum()

            if invalid_values > 0:

                df.loc[
                    df[column] <= 0,
                    column
                ] = pd.NA

                preprocessing_report.append(
                    f"{column}: replaced {invalid_values} "
                    f"invalid non-positive values with missing values."
                )


    # -----------------------------------------------------
    # 8. Validate Volume
    # -----------------------------------------------------

    if "Volume" in df.columns:

        invalid_volume = (
            df["Volume"].notna()
            & (df["Volume"] <= 0)
        ).sum()

        if invalid_volume > 0:

            df.loc[
                df["Volume"] <= 0,
                "Volume"
            ] = pd.NA

            preprocessing_report.append(
                f"Volume: replaced {invalid_volume} "
                f"invalid non-positive values with missing values."
            )


    # -----------------------------------------------------
    # 9. Validate OHLC relationships
    # -----------------------------------------------------

    required_ohlc_columns = [
        "Open",
        "High",
        "Low",
        "Close"
    ]

    if all(
        column in df.columns
        for column in required_ohlc_columns
    ):

        invalid_high = (
            (df["High"] < df["Open"])
            | (df["High"] < df["Close"])
            | (df["High"] < df["Low"])
        )

        invalid_low = (
            (df["Low"] > df["Open"])
            | (df["Low"] > df["Close"])
            | (df["Low"] > df["High"])
        )

        invalid_ohlc_rows = (
            invalid_high | invalid_low
        )

        invalid_count = invalid_ohlc_rows.sum()

        if invalid_count > 0:

            # The application cannot determine which
            # individual OHLC value is incorrect.
            # Therefore, mark the OHLC values as missing
            # and handle them through mean imputation.

            df.loc[
                invalid_ohlc_rows,
                ["Open", "High", "Low", "Close"]
            ] = pd.NA

            preprocessing_report.append(
                f"Found {invalid_count} rows with invalid "
                f"OHLC relationships. Their OHLC values "
                f"were marked as missing."
            )

        else:

            preprocessing_report.append(
                "OHLC relationships validated successfully."
            )


    # -----------------------------------------------------
    # 10. Replace missing numerical values with mean
    # -----------------------------------------------------

    for column in numeric_columns:

        if column in df.columns:

            missing_values = df[column].isna().sum()

            if missing_values > 0:

                column_mean = df[column].mean()

                if pd.notna(column_mean):

                    df[column] = df[column].fillna(
                        column_mean
                    )

                    preprocessing_report.append(
                        f"{column}: replaced {missing_values} "
                        f"missing/invalid values with mean "
                        f"({column_mean:.2f})."
                    )


    # -----------------------------------------------------
    # 11. Sort data chronologically
    # -----------------------------------------------------

    df = df.sort_values(
        by="Date"
    ).reset_index(drop=True)

    preprocessing_report.append(
        "Dataset sorted chronologically by Date."
    )


    # -----------------------------------------------------
    # 12. Final validation
    # -----------------------------------------------------

    remaining_missing = int(
        df.isna().sum().sum()
    )

    if remaining_missing == 0:

        preprocessing_report.append(
            "Final validation passed: no missing values remain."
        )

    else:

        preprocessing_report.append(
            f"Final validation: {remaining_missing} "
            f"missing values remain."
        )


    return df, preprocessing_report


# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "📁 Upload a file",
    type=["csv", "xlsx", "xls"]
)


if uploaded_file is not None:

    # =====================================================
    # READ DATASET
    # =====================================================

    try:

        filename = uploaded_file.name

        if filename.lower().endswith(".csv"):

            df = pd.read_csv(
                uploaded_file,
                encoding="ISO-8859-1"
            )

        elif filename.lower().endswith(
            (".xlsx", ".xls")
        ):

            df = pd.read_excel(
                uploaded_file
            )

        else:

            st.error("Unsupported file format.")
            st.stop()


        st.success(
            f"Successfully uploaded: {filename}"
        )


    except Exception as e:

        st.error(
            f"Unable to read the uploaded file: {e}"
        )

        st.stop()


    # =====================================================
    # RAW DATA
    # =====================================================

    with st.expander("🔍 View Raw Data"):

        st.dataframe(
            df,
            use_container_width=True
        )


    # =====================================================
    # PREPROCESSING
    # =====================================================

    st.subheader("🧹 Data Preprocessing")

    cleaned_df, preprocessing_report = preprocess_data(
        df
    )

    if cleaned_df is None:
        st.stop()


    # =====================================================
    # PREPROCESSING REPORT
    # =====================================================

    with st.expander(
        "📋 View Preprocessing Report",
        expanded=True
    ):

        for report in preprocessing_report:

            st.write("✓", report)


    # =====================================================
    # CLEANED DATA
    # =====================================================

    st.subheader("✅ Cleaned Dataset")

    st.dataframe(
        cleaned_df,
        use_container_width=True
    )


    # =====================================================
    # DATASET SUMMARY
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Rows",
            cleaned_df.shape[0]
        )

    with col2:

        st.metric(
            "Columns",
            cleaned_df.shape[1]
        )

    with col3:

        st.metric(
            "Missing Values",
            int(cleaned_df.isna().sum().sum())
        )

    with col4:

        st.metric(
            "Duplicate Rows",
            int(cleaned_df.duplicated().sum())
        )


    # =====================================================
    # DATE FILTER
    # =====================================================

    start_date = cleaned_df["Date"].min()
    end_date = cleaned_df["Date"].max()

    col1, col2 = st.columns(2)

    with col1:

        date1 = pd.to_datetime(
            st.date_input(
                "Start Date",
                start_date
            )
        )

    with col2:

        date2 = pd.to_datetime(
            st.date_input(
                "End Date",
                end_date
            )
        )


    # Validate selected dates

    if date1 > date2:

        st.error(
            "Start Date cannot be later than End Date."
        )

        st.stop()


    # Filter data

    df = cleaned_df[
        (cleaned_df["Date"] >= date1)
        & (cleaned_df["Date"] <= date2)
    ].copy()


    # =====================================================
    # NUMERICAL COLUMNS
    # =====================================================

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    numeric_cols = numeric_df.columns.tolist()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Display Settings:")

chart_select = st.sidebar.selectbox(
    "Select the chart type:",
    [
        "None",
        "Scatter Plot",
        "Line Plot",
        "Histogram Plots",
        "Box Plot",
        "Funnel",
        "ECDF Plot"
    ]
)


# =========================================================
# SCATTER PLOT
# =========================================================

if (
    uploaded_file is not None
    and chart_select == "Scatter Plot"
):

    st.sidebar.subheader(
        "Scatter Plot Settings"
    )

    feature_selection = st.sidebar.multiselect(
        "Features to plot",
        options=numeric_cols
    )

    if feature_selection:

        fig = px.scatter(
            df,
            x="Date",
            y=feature_selection,
            title="Stock Price Scatter Plot"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Select at least one numerical feature."
        )


# =========================================================
# LINE PLOT
# =========================================================

if (
    uploaded_file is not None
    and chart_select == "Line Plot"
):

    st.sidebar.subheader(
        "Line Plot Settings"
    )

    feature_selection = st.sidebar.multiselect(
        "Features to plot",
        options=numeric_cols
    )

    if feature_selection:

        fig = px.line(
            df,
            x="Date",
            y=feature_selection,
            title="Stock Market Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Select at least one numerical feature."
        )


# =========================================================
# HISTOGRAM
# =========================================================

if (
    uploaded_file is not None
    and chart_select == "Histogram Plots"
):

    st.sidebar.subheader(
        "Histogram Settings"
    )

    feature_selection = st.sidebar.multiselect(
        "Features to plot",
        options=numeric_cols
    )

    if feature_selection:

        fig = px.histogram(
            df,
            x=feature_selection,
            title="Stock Data Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Select at least one numerical feature."
        )


# =========================================================
# BOX PLOT
# =========================================================

if (
    uploaded_file is not None
    and chart_select == "Box Plot"
):

    st.sidebar.subheader(
        "Box Plot Settings"
    )

    feature_selection = st.sidebar.multiselect(
        "Features to plot",
        options=numeric_cols
    )

    if feature_selection:

        fig = px.box(
            df,
            y=feature_selection,
            title="Stock Data Box Plot"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Select at least one numerical feature."
        )


# =========================================================
# FUNNEL
# =========================================================

if (
    uploaded_file is not None
    and chart_select == "Funnel"
):

    st.sidebar.subheader(
        "Funnel Settings"
    )

    feature_selection = st.sidebar.multiselect(
        "Features to plot",
        options=numeric_cols
    )

    if feature_selection:

        # Funnel charts are not naturally suited
        # for time-series stock data, but this keeps
        # the original project functionality.

        funnel_df = df[
            ["Date"] + feature_selection
        ].copy()

        selected_column = feature_selection[0]

        fig = px.funnel(
            funnel_df,
            y="Date",
            x=selected_column,
            title="Funnel Plot"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Select at least one numerical feature."
        )


# =========================================================
# ECDF PLOT
# =========================================================

if (
    uploaded_file is not None
    and chart_select == "ECDF Plot"
):

    st.sidebar.subheader(
        "ECDF Settings"
    )

    feature_selection = st.sidebar.multiselect(
        "Features to plot",
        options=numeric_cols
    )

    if feature_selection:

        fig = px.ecdf(
            df,
            y=feature_selection,
            title="Empirical Cumulative Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Select at least one numerical feature."
        )