# 📈 Trade Trendz

> **Interactive Stock Market Analysis & Visualization Dashboard**

Trade Trendz is an interactive stock-market analysis application built with **Python, Pandas, Streamlit, Plotly, and Seaborn**.

Users can upload their own stock-market datasets, preprocess and validate the data, select a custom time period, and explore stock trends through interactive visualizations and basic technical-analysis tools.

🔴 **Live Demo:**
https://tradetrendz.streamlit.app/

🟢 **Source Code:**
https://github.com/INDIAN123456890/Trade_Trendz_Updated

---

## 🎯 Features

* 📂 Upload **CSV, XLSX, and XLS** stock-market datasets
* 🧹 Automatic data preprocessing and validation
* 🔢 Numerical type conversion
* 🧮 Mean-based missing-value handling
* 🔍 Duplicate and invalid-value detection
* 📊 OHLC data validation
* 📅 Dynamic date-range selection based on the uploaded dataset
* 🗓️ Daily, weekly, and monthly analysis
* 📈 Multiple interactive visualizations
* ⚙️ Customizable chart and analysis settings

---

## 🧹 Data Preprocessing

Before visualization, the uploaded dataset goes through a preprocessing pipeline.

The application handles:

* Completely empty rows
* Duplicate records
* Invalid dates
* Invalid numerical values
* Missing numerical values
* Non-positive stock prices
* Invalid trading volume
* Inconsistent OHLC relationships

Missing numerical values are replaced using the **mean of their respective column**.

The application also provides a preprocessing report so users can see what changes were made to their data.

---

## 📊 Visualizations

Trade Trendz currently supports:

| Visualization       | Purpose                                           |
| ------------------- | ------------------------------------------------- |
| Line Plot           | Analyze trends over time                          |
| Scatter Plot        | Explore relationships between variables           |
| Histogram           | Understand data distributions                     |
| Box Plot            | Examine distributions and extreme values          |
| Candlestick         | Visualize OHLC price movement                     |
| Area Chart          | Show price trends over time                       |
| Volume Chart        | Analyze trading activity                          |
| Daily Returns       | Analyze percentage price changes                  |
| Moving Average      | Identify smoothed price trends                    |
| Bollinger Bands     | Explore price volatility                          |
| Correlation Heatmap | Analyze relationships between numerical variables |
| ECDF                | Examine cumulative distributions                  |
| Funnel Plot         | Additional exploratory visualization              |

---

## ⚙️ Customization

The sidebar allows users to customize their analysis through options such as:

* **Chart type**
* **Date range**
* **Analysis frequency**

  * Original
  * Daily
  * Weekly
  * Monthly
* **Feature selection**
* **Moving-average period**
* **Chart height**
* **Markers**
* **Logarithmic Y-axis**

The date range is automatically determined from the uploaded dataset, so users can perform analysis on their **own timeline** rather than being restricted to a predefined period.

---

## 🏗️ Workflow

```text
Upload Dataset
      ↓
Data Validation
      ↓
Data Preprocessing
      ↓
Missing & Invalid Value Handling
      ↓
OHLC Validation
      ↓
Chronological Sorting
      ↓
Custom Date Filtering
      ↓
Frequency Selection
      ↓
Interactive Visualization
```

---

## 🛠️ Tech Stack

* **Python** – Application development
* **Pandas** – Data manipulation and preprocessing
* **Streamlit** – Interactive web application
* **Plotly** – Interactive charts
* **Seaborn** – Visualization support
* **OpenPyXL** – XLSX file handling
* **xlrd** – XLS file handling

---

## 📁 Project Structure

```text
Trade_Trendz/
│
├── app.py
├── requirements.txt
├── README.md
└── GOOGL.xlsx
```

### Main Files

**`app.py`**
Contains the Streamlit application, preprocessing pipeline, validation logic, analysis controls, and visualizations.

**`requirements.txt`**
Contains the dependencies required to run the application.

**`GOOGL.xlsx`**
Sample stock-market dataset for testing the application.

---

## 💻 Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/INDIAN123456890/Trade_Trendz_Updated.git
cd Trade_Trendz_Updated
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at the local Streamlit URL.

---

## ☁️ Deployment

Trade Trendz is deployed using **Streamlit Community Cloud**.

🔴 **Live Application:**
https://tradetrendz.streamlit.app/

The deployment uses the GitHub repository as the source and runs the Streamlit application through `app.py`.

---

## 📚 Learning Outcomes

This project helped build practical experience in:

* Data cleaning and preprocessing
* Missing-value handling
* Data validation
* Time-series analysis
* Exploratory Data Analysis
* Data visualization
* Interactive dashboard development
* Python and Pandas
* Streamlit deployment

---

## 👨‍💻 Author

**Sahil Salunke**

🔗 GitHub:
https://github.com/INDIAN123456890

---

⭐ If you find the project useful, consider giving the repository a star.
