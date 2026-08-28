# 📈 Trade Trendz

**Trade Trendz** is an interactive stock market analysis and visualization application built with **Python, Pandas, Streamlit, Seaborn, and Plotly**.

The application allows users to upload stock-market datasets in **CSV, XLSX, or XLS format**, automatically preprocesses and validates the uploaded data, and provides interactive visualizations for exploring stock price and trading-volume trends.

> **Note:** The application is designed primarily around stock-market datasets containing columns such as `Date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, and `Volume`.

---

## 🚀 Live Application

**Live Demo:**
https://tradetrendz.streamlit.app/

---

# 🎯 Project Objective

Stock-market datasets can contain missing values, invalid numerical values, duplicate records, incorrectly formatted dates, or inconsistent OHLC values.

Trade Trendz introduces a preprocessing layer before visualization so that the uploaded dataset is checked and cleaned before being used for analysis.

The project focuses on:

* Data ingestion
* Data validation
* Data preprocessing
* Missing-value handling
* Data-type conversion
* Invalid-value detection
* OHLC consistency validation
* Duplicate removal
* Chronological sorting
* Interactive data visualization
* Exploratory stock-market analysis

---

# 🏗️ Application Workflow

```text
                  User
                   │
                   ▼
          Upload CSV / XLSX / XLS
                   │
                   ▼
          ┌──────────────────┐
          │ File Validation  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Data Validation  │
          └────────┬─────────┘
                   │
                   ▼
          ┌─────────────────────────┐
          │ Data Preprocessing      │
          │                         │
          │ • Remove empty rows     │
          │ • Remove duplicates     │
          │ • Validate Date         │
          │ • Convert data types    │
          │ • Handle missing values │
          │ • Validate prices       │
          │ • Validate Volume       │
          │ • Validate OHLC         │
          └────────────┬────────────┘
                       │
                       ▼
              Cleaned Dataset
                       │
                       ▼
             Chronological Sorting
                       │
                       ▼
             Date Range Filtering
                       │
                       ▼
             Interactive Analysis
                       │
                       ▼
        ┌─────────────────────────────┐
        │       Visualizations        │
        │                             │
        │ • Scatter Plot              │
        │ • Line Plot                 │
        │ • Histogram                 │
        │ • Box Plot                  │
        │ • Funnel Plot               │
        │ • ECDF Plot                 │
        └─────────────────────────────┘
```

---

# 🧹 Data Preprocessing

One of the major improvements in the project is the preprocessing and validation stage.

The application does **not directly visualize the uploaded data**. The data passes through a validation and cleaning pipeline first.

## 1. Empty Row Removal

Completely empty rows are removed from the dataset.

```python
df.dropna(how="all")
```

This prevents blank records from affecting analysis and visualizations.

---

## 2. Duplicate Detection

Duplicate rows are identified and removed.

```python
df.duplicated()
```

This prevents the same market record from being counted multiple times.

---

## 3. Date Validation

The `Date` column is converted into a proper datetime format.

```python
pd.to_datetime(
    df["Date"],
    errors="coerce"
)
```

Invalid dates are converted to `NaT` and the affected records are removed rather than inventing an artificial date.

---

## 4. Numerical Data Validation

The following stock-market columns are treated as numerical columns:

```text
Open
High
Low
Close
Adj Close
Volume
```

Values that cannot be interpreted as numbers are converted to missing values.

```python
pd.to_numeric(
    df[column],
    errors="coerce"
)
```

---

## 5. Missing-Value Handling

Missing numerical values are replaced using the **mean of their respective column**.

For example:

```text
Open:
100
102
NaN
104
```

The missing value is replaced using:

```text
Mean(Open)
```

The same approach is applied to the available numerical columns.

This provides a simple and consistent imputation strategy for the project.

---

## 6. Invalid Price Detection

Stock prices should not normally contain zero or negative values.

Therefore, the application checks:

```text
Open > 0
High > 0
Low > 0
Close > 0
Adj Close > 0
```

If an invalid non-positive value is detected, it is converted into a missing value and subsequently handled through mean imputation.

---

## 7. Volume Validation

Trading volume is expected to be positive.

The application therefore checks:

```text
Volume > 0
```

Invalid non-positive values are treated as missing and replaced using the column mean.

---

# 📊 OHLC Validation

The application also performs domain-specific validation of stock-market data.

For a valid OHLC record:

```text
High >= Open
High >= Close
High >= Low

Low <= Open
Low <= Close
Low <= High
```

For example, this would be an invalid record:

```text
Open   = 100
High   = 90
Low    = 95
Close  = 105
```

because:

```text
High < Open
High < Close
```

When an invalid OHLC relationship is detected, the OHLC values for that record are marked as missing and subsequently handled by the preprocessing stage.

This prevents obviously inconsistent stock-price records from being directly visualized.

---

# 📅 Chronological Ordering

After preprocessing, the dataset is sorted by:

```text
Date
```

This is particularly important for stock-market time-series analysis because chronological ordering allows trends to be interpreted correctly.

---

# 📋 Preprocessing Report

The application provides a preprocessing report after the dataset has been uploaded.

The report can indicate operations such as:

```text
✓ No duplicate rows found.
✓ Date column validated successfully.
✓ Open: replaced 4 missing values with mean.
✓ High: replaced 2 missing values with mean.
✓ Low: replaced 4 missing values with mean.
✓ Close: replaced 3 missing values with mean.
✓ Adj Close: replaced 2 missing values with mean.
✓ Volume: replaced 4 missing values with mean.
✓ OHLC relationships validated successfully.
✓ Dataset sorted chronologically by Date.
✓ Final validation passed: no missing values remain.
```

This makes the preprocessing process transparent instead of silently modifying the uploaded dataset.

---

# 📈 Visualizations

After preprocessing, users can select different visualization techniques from the sidebar.

## Scatter Plot

Used to examine relationships between numerical stock-market variables.

Possible variables include:

* Open
* High
* Low
* Close
* Adj Close
* Volume

The `Date` column is used as the time dimension.

---

## Line Plot

The line plot is particularly useful for analyzing stock-price movement over time.

Users can select multiple numerical features.

Example:

```text
Date → Close
Date → Open
Date → High
Date → Low
```

This helps identify trends and changes in stock prices.

---

## Histogram

Histograms are used to understand the distribution of numerical variables.

They can be used to analyze:

* Price distributions
* Trading-volume distributions
* Variability in stock-market values

---

## Box Plot

Box plots provide a compact view of:

* Median
* Quartiles
* Distribution
* Potential extreme observations

They can be used for variables such as `Close`, `Open`, or `Volume`.

---

## Funnel Plot

The application also retains a funnel visualization option from the original project.

Although funnel charts are not naturally designed for stock-market time-series analysis, the functionality is maintained as part of the project's interactive visualization options.

---

## ECDF Plot

The Empirical Cumulative Distribution Function (ECDF) provides a way to examine the cumulative distribution of numerical variables.

It can help understand how observations are distributed across different price or volume ranges.

---

# 🖥️ Application Features

### 📂 Flexible Data Upload

Supported formats:

```text
CSV
XLSX
XLS
```

### 🧹 Automated Preprocessing

The application automatically handles:

* Empty rows
* Duplicate rows
* Missing numerical values
* Invalid numerical values
* Invalid dates
* Non-positive prices
* Invalid trading volume
* Invalid OHLC relationships

### 📊 Dataset Summary

The dashboard displays:

* Number of rows
* Number of columns
* Remaining missing values
* Duplicate rows

### 📅 Date Filtering

Users can select:

```text
Start Date
End Date
```

to analyze a specific period.

### 📈 Interactive Charts

Available visualizations include:

* Scatter Plot
* Line Plot
* Histogram
* Box Plot
* Funnel Plot
* ECDF Plot

---

# 🛠️ Technology Stack

| Technology | Purpose                             |
| ---------- | ----------------------------------- |
| Python     | Core programming language           |
| Pandas     | Data manipulation and preprocessing |
| Streamlit  | Interactive web application         |
| Plotly     | Interactive visualizations          |
| Seaborn    | Visualization support               |
| OpenPyXL   | Excel file processing               |
| xlrd       | Legacy Excel file support           |

---

# 📁 Project Structure

```text
Trade_Trendz/
│
├── app.py
├── requirements.txt
├── README.md
├── GOOGL.xlsx
└── ...
```

### `app.py`

Contains the Streamlit application, preprocessing pipeline, validation logic, date filtering, and visualization functionality.

### `requirements.txt`

Contains the Python dependencies required to run the application.

### `GOOGL.xlsx`

Sample Google stock-market dataset used for testing the application.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/INDIAN123456890/Trade_Trendz.git
```

Navigate into the project directory:

```bash
cd Trade_Trendz
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application Locally

Execute:

```bash
streamlit run app.py
```

Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open the URL in your browser.

---

# ☁️ Deploying on Streamlit Community Cloud

The application can be deployed using Streamlit Community Cloud.

### Step 1

Push the project to GitHub.

Make sure the repository contains:

```text
app.py
requirements.txt
```

### Step 2

Open Streamlit Community Cloud and connect your GitHub account.

### Step 3

Select:

```text
Repository → Trade_Trendz
```

### Step 4

Set the main application file as:

```text
app.py
```

### Step 5

Deploy the application.

Streamlit Cloud will install the dependencies specified in:

```text
requirements.txt
```

and start the application.

---

# 🧪 Testing the Preprocessing

For testing, the application should be provided with datasets containing different types of problems.

### Test Case 1 — Missing Values

```text
Open = NaN
Close = NaN
Volume = NaN
```

Expected behavior:

```text
Missing values → Column mean
```

---

### Test Case 2 — Invalid Numeric Values

```text
Open = "ABC"
Close = "XYZ"
```

Expected behavior:

```text
Invalid values
      ↓
NaN
      ↓
Column mean
```

---

### Test Case 3 — Invalid Price

```text
Close = -100
```

Expected behavior:

```text
-100
 ↓
Invalid
 ↓
NaN
 ↓
Column mean
```

---

### Test Case 4 — Invalid OHLC

```text
Open  = 100
High  = 80
Low   = 90
Close = 105
```

Expected behavior:

```text
Invalid OHLC relationship
          ↓
OHLC values marked as missing
          ↓
Mean imputation
```

---

### Test Case 5 — Duplicate Records

```text
Same row appears multiple times
```

Expected behavior:

```text
Duplicate records → Removed
```

---

# ⚠️ Important Data Considerations

Mean imputation is intentionally used in this project as a straightforward preprocessing strategy.

However, for production-grade financial time-series systems, other techniques may be more appropriate depending on the analytical objective.

For example:

* Forward filling
* Backward filling
* Interpolation
* Rolling statistics
* Time-series-specific imputation

Similarly, extreme stock-price movements should **not automatically be treated as errors**. A large price movement can represent a genuine market event.

Therefore, this project focuses on detecting clearly invalid or inconsistent values rather than automatically removing statistical outliers.

---

# 🔒 Data Privacy

Trade Trendz processes the uploaded dataset within the application session for analysis and visualization.

Users should avoid uploading datasets containing confidential, proprietary, or personally identifiable information.

---

# 🔮 Future Improvements

Potential improvements include:

* Candlestick charts
* Moving averages
* Technical indicators
* RSI analysis
* MACD analysis
* Bollinger Bands
* Trading-volume analysis
* Correlation analysis
* Interactive dashboards
* Stock comparison
* Automated anomaly detection
* Download cleaned dataset
* Additional preprocessing strategies
* Database integration
* Automated data ingestion from financial APIs

---

# 📌 Learning Outcomes

This project demonstrates practical understanding of:

* Python
* Pandas
* Data cleaning
* Data preprocessing
* Missing-value handling
* Data validation
* Data-type conversion
* Domain-specific validation
* Time-series data handling
* Exploratory Data Analysis
* Data visualization
* Streamlit application development
* Interactive dashboard development
* Basic deployment using Streamlit Community Cloud

---

# 👨‍💻 Author

**Sahil Salunke**

GitHub:
https://github.com/INDIAN123456890

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
