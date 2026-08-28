import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
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
    else:
        preprocessing_report.append(
            "No completely empty rows found."
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
    # 3. Validate Date column
    # -----------------------------------------------------

    if "Date" not in df.columns:

        st.error(
            "Invalid dataset: 'Date' column is missing."
        )

        return None, preprocessing_report


    # Convert Date column

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )


    # -----------------------------------------------------
    # 4. Handle invalid dates
    # -----------------------------------------------------

    invalid_dates = df["Date"].isna().sum()

    if invalid_dates > 0:

        df = df.dropna(
            subset=["Date"]
        ).copy()

        preprocessing_report.append(
            f"Removed {invalid_dates} rows containing "
            f"invalid or missing dates."
        )

    else:

        preprocessing_report.append(
            "Date column validated successfully."
        )


    # -----------------------------------------------------
    # 5. Numerical columns
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
    # 7. Validate stock prices
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
                f"invalid values with missing values."
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
    # 10. Mean imputation
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

            else:

                preprocessing_report.append(
                    f"{column}: no missing values found."
                )


    # -----------------------------------------------------
    # 11. Sort chronologically
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
    "📁 Upload a stock market dataset",
    type=["csv", "xlsx", "xls"]
)


if uploaded_file is not None:

    # =====================================================
    # READ FILE
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
        expanded=False
    ):

        for report in preprocessing_report:

            st.write("✓", report)


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
    # SIDEBAR
    # =====================================================

    st.sidebar.title("⚙️ Analysis Settings")


    # -----------------------------------------------------
    # Chart Selection
    # -----------------------------------------------------

    st.sidebar.subheader("📊 Chart Type")

    chart_select = st.sidebar.selectbox(
        "Select visualization",
        [
            "None",
            "Line Plot",
            "Scatter Plot",
            "Histogram",
            "Box Plot",
            "Candlestick",
            "Area Chart",
            "Volume Chart",
            "Daily Returns",
            "Moving Average",
            "Bollinger Bands",
            "Correlation Heatmap",
            "ECDF Plot",
            "Funnel Plot"
        ]
    )


    # =====================================================
    # DYNAMIC DATE RANGE
    # =====================================================

    st.sidebar.subheader("📅 Time Range")

    min_date = cleaned_df["Date"].min().date()
    max_date = cleaned_df["Date"].max().date()


    # The allowed range comes directly from
    # the uploaded dataset.

    selected_dates = st.sidebar.date_input(
        "Select analysis period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )


    # Handle the case where only one date is selected

    if isinstance(selected_dates, tuple):

        if len(selected_dates) == 2:

            date1 = pd.to_datetime(
                selected_dates[0]
            )

            date2 = pd.to_datetime(
                selected_dates[1]
            )

        else:

            date1 = pd.to_datetime(
                selected_dates[0]
            )

            date2 = date1

    else:

        date1 = pd.to_datetime(
            selected_dates
        )

        date2 = date1


    # -----------------------------------------------------
    # Filter dataset according to selected dates
    # -----------------------------------------------------

    df = cleaned_df[
        (cleaned_df["Date"] >= date1)
        & (cleaned_df["Date"] <= date2)
    ].copy()


    # =====================================================
    # RESAMPLING / FREQUENCY
    # =====================================================

    st.sidebar.subheader("🗓️ Analysis Frequency")

    frequency = st.sidebar.selectbox(
        "Data frequency",
        [
            "Original",
            "Daily",
            "Weekly",
            "Monthly"
        ]
    )


    # =====================================================
    # FEATURE SELECTION
    # =====================================================

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    st.sidebar.subheader("📌 Features")

    if chart_select in [
        "Line Plot",
        "Scatter Plot",
        "Histogram",
        "Box Plot",
        "Candlestick",
        "Area Chart",
        "Volume Chart",
        "Daily Returns",
        "Moving Average",
        "Bollinger Bands",
        "Correlation Heatmap",
        "ECDF Plot",
        "Funnel Plot"
    ]:
        feature_selection = st.sidebar.multiselect(
            "Select numerical features",
            options=numeric_cols,
            default=(
                ["Close"]
                if "Close" in numeric_cols
                else numeric_cols[:1]
            )
        )
    else:
        feature_selection = []


    # =====================================================
    # MOVING AVERAGE SETTINGS
    # =====================================================

    st.sidebar.subheader("📈 Technical Analysis")

    moving_average = st.sidebar.selectbox(
        "Moving Average",
        [
            "None",
            "7 Days",
            "20 Days",
            "50 Days",
            "100 Days",
            "200 Days"
        ]
    )


    # =====================================================
    # DISPLAY SETTINGS
    # =====================================================

    st.sidebar.subheader("🎨 Display Settings")

    show_markers = st.sidebar.checkbox(
        "Show markers",
        value=False
    )

    log_scale = st.sidebar.checkbox(
        "Logarithmic Y-axis",
        value=False
    )

    chart_height = st.sidebar.slider(
        "Chart height",
        min_value=400,
        max_value=900,
        value=600,
        step=50
    )


    # =====================================================
    # RESAMPLING
    # =====================================================

    analysis_df = df.copy()

    if frequency != "Original":

        analysis_df = (
            analysis_df
            .set_index("Date")
            .resample(
                {
                    "Daily": "D",
                    "Weekly": "W",
                    "Monthly": "ME"
                }[frequency]
            )
            .agg({
                column: "mean"
                for column in numeric_cols
            })
            .dropna(how="all")
            .reset_index()
        )


    # =====================================================
    # MOVING AVERAGE
    # =====================================================

    if moving_average != "None" and "Close" in analysis_df.columns:

        window = int(
            moving_average.split()[0]
        )

        analysis_df["Moving Average"] = (
            analysis_df["Close"]
            .rolling(window=window)
            .mean()
        )


    # =====================================================
    # LINE PLOT
    # =====================================================

    if chart_select == "Line Plot":

        if feature_selection:

            fig = px.line(
                analysis_df,
                x="Date",
                y=feature_selection,
                title="Stock Market Trend"
            )

            if log_scale:
                fig.update_yaxes(
                    type="log"
                )

            fig.update_layout(
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Select at least one numerical feature."
            )


    # =====================================================
    # SCATTER PLOT
    # =====================================================

    elif chart_select == "Scatter Plot":

        if len(feature_selection) >= 1:

            x_feature = st.sidebar.selectbox(
                "X-axis",
                numeric_cols,
                index=(
                    numeric_cols.index("Close")
                    if "Close" in numeric_cols
                    else 0
                )
            )

            y_feature = st.sidebar.selectbox(
                "Y-axis",
                numeric_cols,
                index=(
                    numeric_cols.index("Volume")
                    if "Volume" in numeric_cols
                    else min(1, len(numeric_cols) - 1)
                )
            )

            fig = px.scatter(
                analysis_df,
                x=x_feature,
                y=y_feature,
                title=f"{y_feature} vs {x_feature}"
            )

            fig.update_layout(
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Select numerical features."
            )


    # =====================================================
    # HISTOGRAM
    # =====================================================

    elif chart_select == "Histogram":

        if feature_selection:

            fig = px.histogram(
                analysis_df,
                x=feature_selection,
                title="Stock Data Distribution"
            )

            fig.update_layout(
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Select at least one feature."
            )


    # =====================================================
    # BOX PLOT
    # =====================================================

    elif chart_select == "Box Plot":

        if feature_selection:

            fig = px.box(
                analysis_df,
                y=feature_selection,
                title="Stock Data Distribution"
            )

            fig.update_layout(
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Select at least one feature."
            )


    # =====================================================
    # CANDLESTICK
    # =====================================================

    elif chart_select == "Candlestick":

        required_columns = [
            "Open",
            "High",
            "Low",
            "Close"
        ]

        if all(
            column in analysis_df.columns
            for column in required_columns
        ):

            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=analysis_df["Date"],
                        open=analysis_df["Open"],
                        high=analysis_df["High"],
                        low=analysis_df["Low"],
                        close=analysis_df["Close"]
                    )
                ]
            )

            fig.update_layout(
                title="Stock Price Candlestick Chart",
                height=chart_height,
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.error(
                "Candlestick chart requires "
                "Open, High, Low and Close columns."
            )


    # =====================================================
    # AREA CHART
    # =====================================================

    elif chart_select == "Area Chart":

        if feature_selection:

            fig = px.area(
                analysis_df,
                x="Date",
                y=feature_selection,
                title="Stock Area Chart"
            )

            fig.update_layout(
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Select at least one feature."
            )


    # =====================================================
    # VOLUME CHART
    # =====================================================

    elif chart_select == "Volume Chart":

        if "Volume" in analysis_df.columns:

            fig = px.bar(
                analysis_df,
                x="Date",
                y="Volume",
                title="Trading Volume"
            )

            fig.update_layout(
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.error(
                "The dataset does not contain a Volume column."
            )


    # =====================================================
    # DAILY RETURNS
    # =====================================================

    elif chart_select == "Daily Returns":

        if "Close" in analysis_df.columns:

            returns_df = analysis_df.copy()

            returns_df["Daily Return (%)"] = (
                returns_df["Close"]
                .pct_change()
                * 100
            )

            fig = px.line(
                returns_df,
                x="Date",
                y="Daily Return (%)",
                title="Daily Stock Returns"
            )

            fig.add_hline(
                y=0,
                line_dash="dash"
            )

            fig.update_layout(
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.error(
                "Close column is required for return analysis."
            )


    # =====================================================
    # MOVING AVERAGE
    # =====================================================

    elif chart_select == "Moving Average":

        if "Close" in analysis_df.columns:

            window = st.sidebar.slider(
                "Moving Average Window",
                min_value=2,
                max_value=200,
                value=20
            )

            ma_df = analysis_df.copy()

            ma_df["Moving Average"] = (
                ma_df["Close"]
                .rolling(window)
                .mean()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=ma_df["Date"],
                    y=ma_df["Close"],
                    mode="lines",
                    name="Close"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=ma_df["Date"],
                    y=ma_df["Moving Average"],
                    mode="lines",
                    name=f"{window}-Period MA"
                )
            )

            fig.update_layout(
                title="Closing Price vs Moving Average",
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.error(
                "Close column is required."
            )


    # =====================================================
    # BOLLINGER BANDS
    # =====================================================

    elif chart_select == "Bollinger Bands":

        if "Close" in analysis_df.columns:

            window = st.sidebar.slider(
                "Bollinger Band Window",
                min_value=5,
                max_value=100,
                value=20
            )

            bb_df = analysis_df.copy()

            bb_df["Middle Band"] = (
                bb_df["Close"]
                .rolling(window)
                .mean()
            )

            rolling_std = (
                bb_df["Close"]
                .rolling(window)
                .std()
            )

            bb_df["Upper Band"] = (
                bb_df["Middle Band"]
                + (2 * rolling_std)
            )

            bb_df["Lower Band"] = (
                bb_df["Middle Band"]
                - (2 * rolling_std)
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=bb_df["Date"],
                    y=bb_df["Close"],
                    mode="lines",
                    name="Close"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=bb_df["Date"],
                    y=bb_df["Upper Band"],
                    mode="lines",
                    name="Upper Band"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=bb_df["Date"],
                    y=bb_df["Lower Band"],
                    mode="lines",
                    name="Lower Band"
                )
            )

            fig.update_layout(
                title="Bollinger Bands",
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.error(
                "Close column is required."
            )


    # =====================================================
    # CORRELATION HEATMAP
    # =====================================================

    elif chart_select == "Correlation Heatmap":

        if len(numeric_cols) >= 2:

            correlation = analysis_df[
                numeric_cols
            ].corr()

            fig = px.imshow(
                correlation,
                text_auto=True,
                title="Correlation Heatmap",
                aspect="auto"
            )

            fig.update_layout(
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "At least two numerical columns are required."
            )


    # =====================================================
    # ECDF
    # =====================================================

    elif chart_select == "ECDF Plot":

        if feature_selection:

            fig = px.ecdf(
                analysis_df,
                y=feature_selection,
                title="Empirical Cumulative Distribution"
            )

            fig.update_layout(
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Select at least one feature."
            )


    # =====================================================
    # FUNNEL
    # =====================================================

    elif chart_select == "Funnel Plot":

        if feature_selection:

            selected_column = feature_selection[0]

            funnel_df = analysis_df[
                ["Date", selected_column]
            ].copy()

            fig = px.funnel(
                funnel_df,
                y="Date",
                x=selected_column,
                title="Funnel Plot"
            )

            fig.update_layout(
                height=chart_height
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Select a numerical feature."
            )


# =========================================================
# NO FILE MESSAGE
# =========================================================

else:

    st.info(
        "👆 Upload a CSV or Excel stock-market dataset "
        "to begin analysis."
    )
