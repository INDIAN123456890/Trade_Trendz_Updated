# 📈 Trade Trendz

> **Interactive Stock Market Analysis & Visualization Dashboard**

**Trade Trendz** is an interactive stock-market analysis application built with **Python, Pandas, Streamlit, Plotly, and Seaborn**.

The application allows users to upload their own stock-market datasets, automatically validate and preprocess the data, select a custom analysis period, and explore the data through multiple interactive visualizations and technical-analysis tools.

🔴 **Live Application:**
https://tradetrendz.streamlit.app/

🟢 **Source Code:**
https://github.com/INDIAN123456890/Trade_Trendz_Updated

---

# 🎯 Project Overview

Trade Trendz started as a simple stock-market visualization project and has been enhanced into an interactive data-analysis application.

Instead of assuming that the uploaded dataset is already clean, the application performs a preprocessing and validation stage before the data reaches the visualization layer.

The application is designed to answer questions such as:

* How has a stock's price changed over a selected period?
* How are Open, High, Low and Close prices distributed?
* What is the relationship between different numerical variables?
* How does trading volume change over time?
* What are the daily returns?
* How does the moving average compare with the closing price?
* How does price volatility behave through Bollinger Bands?
* How strongly are different numerical variables correlated?
* What happens when the analysis period or data frequency is changed?

---

# 🚀 Live Demo

### Try Trade Trendz

👉 **https://tradetrendz.streamlit.app/**

The application accepts user-uploaded:

* `.csv`
* `.xlsx`
* `.xls`

files.

Users are **not restricted to the sample Google stock dataset**. The analysis period is dynamically determined from the dates present in the uploaded dataset.

---

# 🏗️ Application Workflow

```text
                    USER
                     │
                     ▼
             Upload Dataset
              CSV / XLSX / XLS
                     │
                     ▼
            ┌─────────────────┐
            │ File Validation │
            └────────┬────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ Data Preprocessing   │
          │                      │
          │ • Empty rows         │
          │ • Duplicates         │
          │ • Date validation    │
          │ • Type conversion    │
          │ • Missing values     │
          │ • Invalid values     │
          │ • OHLC validation    │
          └──────────┬───────────┘
                     │
                     ▼
               Clean Dataset
                     │
                     ▼
             Chronological Sort
                     │
                     ▼
             Custom Date Range
                     │
                     ▼
             Analysis Frequency
                     │
                     ▼
          ┌──────────────────────┐
          │ Interactive Analysis │
          └──────────┬───────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
     Visualizations  Technical  Statistics
                     Analysis
```

---

# 🧹 Data Preprocessing & Validation

One of the major improvements in the current version is the preprocessing layer.

Uploaded data is validated before being used for analysis.

## 1. Empty Row Detection

Completely empty rows are removed.

```python
df.dropna(how="all")
```

This prevents blank records from affecting the analysis.

---

## 2. Duplicate Detection

Duplicate records are identified and removed.

This prevents the same observation from being counted multiple times.

---

## 3. Date Validation

The application checks whether a `Date` column exists and converts it to a proper datetime datatype.

```python
pd.to_datetime(
    df["Date"],
    errors="coerce"
)
```

Invalid or missing dates are removed because an artificial date should not be created for time-series analysis.

---

## 4. Numerical Data Conversion

The application attempts to convert stock-market numerical columns into numeric datatypes.

Supported columns include:

```text
Open
High
Low
Close
Adj Close
Volume
```

Invalid numerical values are converted to missing values and handled by the preprocessing pipeline.

---

# 🧮 Missing-Value Handling

Missing numerical values are replaced with the **mean of their respective column**.

For example:

```text
Open
────
100
102
NaN
104
```

The missing value is replaced by:

```text
Mean(Open)
```

This approach is applied independently to the available numerical columns.

The application also reports the preprocessing operations performed on the dataset.

---

# ⚠️ Invalid Value Detection

The application checks stock-market-specific numerical constraints.

## Price Validation

The following price columns should contain positive values:

```text
Open
High
Low
Close
Adj Close
```

Values that are zero or negative are treated as invalid.

---

## Volume Validation

Trading volume is expected to be positive.

Therefore:

```text
Volume <= 0
```

is treated as an invalid value.

---

# 📊 OHLC Validation

The application performs domain-specific validation for OHLC stock data.

For a valid stock record:

```text
High >= Open
High >= Close
High >= Low

Low <= Open
Low <= Close
Low <= High
```

For example:

```text
Open  = 100
High  = 90
Low   = 95
Close = 105
```

is inconsistent because:

```text
High < Open
High < Close
```

The application detects such records and marks the OHLC values as missing before applying the missing-value handling process.

---

# 📋 Preprocessing Report

The application provides a preprocessing report so users can understand what happened to their dataset.

Examples include:

```text
✓ No duplicate rows found.
✓ Date column validated successfully.
✓ Open: replaced missing values with mean.
✓ High: replaced missing values with mean.
✓ Close: replaced invalid values with mean.
✓ OHLC relationships validated successfully.
✓ Dataset sorted chronologically by Date.
✓ Final validation passed.
```

This makes the cleaning process transparent instead of silently modifying the dataset.

---

# 📅 Dynamic Time-Range Analysis

The application **does not use a fixed date range**.

The available date range is automatically determined from the uploaded dataset.

For example, if a dataset contains:

```text
2010 → 2015
```

the user can select any period within:

```text
2010 → 2015
```

If another dataset contains:

```text
2020 → 2025
```

the available analysis range automatically changes to:

```text
2020 → 2025
```

This makes Trade Trendz suitable for user-provided datasets rather than restricting analysis to the sample data.

Users can select:

* Start date
* End date

from the sidebar.

---

# 🗓️ Analysis Frequency

Users can also choose how the data should be analyzed.

Available options:

```text
Original
Daily
Weekly
Monthly
```

For example:

```text
Original → Raw observations

Weekly → Weekly aggregated values

Monthly → Monthly aggregated values
```

This allows users to analyze both short-term and longer-term trends.

---

# 📈 Visualizations

Trade Trendz currently provides several visualization options.

---

## 1. Line Plot

Used to analyze stock-price movement over time.

Users can select multiple numerical features such as:

```text
Open
High
Low
Close
Adj Close
Volume
```

Useful for identifying:

* Trends
* Directional movement
* Long-term patterns
* Changes between variables

---

## 2. Scatter Plot

Allows users to select their own X and Y variables.

For example:

```text
Close vs Volume
```

or:

```text
Open vs Close
```

This can be used to explore relationships between numerical variables.

---

## 3. Histogram

Histograms show the distribution of selected numerical variables.

Useful for analyzing:

* Price distributions
* Trading-volume distributions
* Data concentration
* Spread of observations

---

## 4. Box Plot

Box plots provide information about:

* Median
* Quartiles
* Distribution
* Potential extreme observations

---

## 5. Candlestick Chart

A dedicated stock-market candlestick visualization is available using:

```text
Open
High
Low
Close
```

This provides a more traditional financial-market representation of price movement.

---

## 6. Area Chart

Area charts provide another way to visualize price movement over time while emphasizing the magnitude of the selected values.

---

## 7. Volume Chart

Trading volume can be visualized separately to understand activity across the selected period.

---

## 8. Daily Returns

The application calculates percentage changes in closing price:

```text
Daily Return =
(Closeₜ / Closeₜ₋₁ - 1) × 100
```

This helps analyze daily price movement rather than absolute price.

---

## 9. Moving Average

Users can configure a moving-average window.

Examples:

```text
7-period
20-period
50-period
100-period
200-period
```

The moving average can help smooth short-term fluctuations and highlight broader trends.

---

## 10. Bollinger Bands

The application provides Bollinger Band analysis using:

```text
Middle Band = Moving Average

Upper Band =
Moving Average + 2 × Rolling Standard Deviation

Lower Band =
Moving Average - 2 × Rolling Standard Deviation
```

This provides a basic view of price volatility around a moving average.

---

## 11. Correlation Heatmap

The correlation heatmap shows relationships between numerical variables.

For example:

```text
Open
High
Low
Close
Adj Close
Volume
```

This helps identify strongly or weakly correlated variables.

---

## 12. ECDF Plot

The Empirical Cumulative Distribution Function helps understand the cumulative distribution of numerical variables.

---

## 13. Funnel Plot

The original project included a funnel visualization and this functionality has been retained.

Although funnel charts are not specifically designed for stock-market time-series data, it remains available as an additional visualization option.

---

# ⚙️ Customization Options

The sidebar provides several controls for customizing the analysis.

### Chart Selection

Users can choose from multiple visualization types.

### Date Range

Users can select their own analysis period based on the dates available in the uploaded dataset.

### Analysis Frequency

```text
Original
Daily
Weekly
Monthly
```

### Feature Selection

For applicable charts, users can select which numerical columns they want to visualize.

### Moving Average

Users can select a moving-average period.

### Chart Height

Chart height can be adjusted according to user preference.

### Markers

Users can enable or disable markers on applicable charts.

### Logarithmic Y-axis

A logarithmic Y-axis can be enabled for appropriate analyses where large differences in magnitude make a linear scale difficult to interpret.

---

# 📊 Dataset Summary

After preprocessing, the application provides a quick summary containing:

```text
Number of Rows
Number of Columns
Remaining Missing Values
Duplicate Rows
```

This provides an immediate overview of the cleaned dataset.

---

# 🛠️ Technology Stack

| Technology | Purpose                             |
| ---------- | ----------------------------------- |
| Python     | Core programming language           |
| Pandas     | Data manipulation and preprocessing |
| Streamlit  | Interactive web application         |
| Plotly     | Interactive visualizations          |
| Seaborn    | Visualization support               |
| OpenPyXL   | XLSX file processing                |
| xlrd       | XLS file support                    |

---

# 📁 Project Structure

```text
Trade_Trendz/
│
├── app.py
├── requirements.txt
├── README.md
└── GOOGL.xlsx
```

### `app.py`

Contains:

* Streamlit interface
* File upload
* Data preprocessing
* Data validation
* Missing-value handling
* OHLC validation
* Date filtering
* Frequency aggregation
* Visualization logic
* Technical-analysis calculations

### `requirements.txt`

Contains the Python dependencies required by the application.

### `GOOGL.xlsx`

Sample stock-market dataset used for testing and demonstration.

---

# 💻 Run Locally

## 1. Clone the Repository

```bash
git clone https://github.com/INDIAN123456890/Trade_Trendz.git
```

```bash
cd Trade_Trendz
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Streamlit

```bash
streamlit run app.py
```

The application will be available locally through the Streamlit URL shown in the terminal.

---

# ☁️ Deployment

Trade Trendz is deployed using **Streamlit Community Cloud**.

### Live Application

https://tradetrendz.streamlit.app/

The deployment uses:

```text
GitHub Repository
        ↓
Streamlit Community Cloud
        ↓
app.py
        ↓
requirements.txt
        ↓
Live Web Application
```

The GitHub repository serves as the source for the application code and project files.

---

# 🧪 Testing the Application

The application should be tested with datasets containing different data-quality scenarios.

### Missing Values

```text
Open = NaN
Close = NaN
Volume = NaN
```

Expected:

```text
Missing values
      ↓
Column mean
```

### Invalid Numeric Values

```text
Close = "ABC"
```

Expected:

```text
Invalid numeric value
        ↓
Missing value
        ↓
Column mean
```

### Invalid Prices

```text
Close = -100
```

Expected:

```text
Invalid price
     ↓
Missing value
     ↓
Column mean
```

### Invalid OHLC

```text
Open  = 100
High  = 80
Low   = 90
Close = 105
```

Expected:

```text
Invalid OHLC relationship
           ↓
OHLC values marked as missing
           ↓
Mean imputation
```

### Duplicate Records

Expected:

```text
Duplicate rows
      ↓
Removed
```

---

# ⚠️ Important Considerations

## Mean Imputation

Mean imputation is used because it provides a simple and transparent strategy for this project.

However, financial time-series data may require more sophisticated techniques depending on the use case, such as:

* Forward filling
* Interpolation
* Rolling statistics
* Time-series-specific imputation

---

## Outliers

Trade Trendz does **not automatically remove extreme values**.

This is intentional.

A large price movement or volume spike may represent a genuine market event rather than a data-quality problem.

Automatically removing such observations could therefore remove meaningful financial information.

---

## Technical Indicators Are Analytical Tools

Moving averages and Bollinger Bands are provided for exploratory analysis.

They should not be interpreted as guaranteed trading signals or financial advice.

---

# 🔮 Future Improvements

Possible future additions include:

* 📊 Additional technical indicators
* RSI
* MACD
* Stochastic Oscillator
* ATR
* More candlestick customization
* Stock-to-stock comparison
* Advanced volatility analysis
* Automated anomaly detection
* Interactive KPI dashboard
* Download cleaned dataset
* Export analysis reports
* Financial API integration
* Automated data ingestion
* Database integration
* Authentication
* Portfolio-level analysis

---

# 📚 Learning Outcomes

This project provided practical experience with:

* Python
* Pandas
* Data cleaning
* Data preprocessing
* Missing-value imputation
* Data validation
* Data-type conversion
* Domain-specific validation
* Time-series data
* Exploratory Data Analysis
* Statistical visualization
* Interactive visualization
* Streamlit
* Dashboard development
* Application deployment

More importantly, the project demonstrates the progression from:

```text
Raw Dataset
     ↓
Data Cleaning
     ↓
Data Validation
     ↓
Data Transformation
     ↓
Exploratory Analysis
     ↓
Visualization
     ↓
Interactive Application
     ↓
Cloud Deployment
```

---

# 👨‍💻 Author

### Sahil Salunke

GitHub:
https://github.com/INDIAN123456890

---

# ⭐ Support

If you find Trade Trendz useful or interesting, consider giving the repository a ⭐ on GitHub.

**Live Demo:**
https://tradetrendz.streamlit.app/

**Source Code:**
https://github.com/INDIAN123456890/Trade_Trendz_Updated
