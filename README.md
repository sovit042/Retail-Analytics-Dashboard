# 📊 Retail Analytics Dashboard

### Business Decision Support System using Python Analytics

This project was developed as part of a 2nd-year B.E. CSE coursework for **Data Analytics with Python**. The goal was to build a practical system that goes beyond basic visualization and helps in **understanding business performance and supporting decision-making**.

Instead of limiting the work to charts and summaries, this project focuses on identifying patterns, highlighting problem areas, and generating insights that could be useful for a retail business.

---

## 👨‍💻 Team

* **Sovit Ranjan**
* **Avnish Kumar**

---

## 🎯 Objective

The primary objective of this project is to design a **Business Decision Support System** that:

* Analyzes retail sales data
* Identifies profitable and loss-making areas
* Tracks performance across categories, regions, and time
* Provides actionable insights for better business decisions

This project reflects an attempt to apply data analytics concepts in a **real-world business context**, rather than just theoretical implementation.

---

## 🧠 Key Features

* 📦 **Category & Sub-Category Analysis**
  Understand which product segments drive profit and which lead to losses

* 🌍 **Regional Performance Insights**
  Compare sales and profitability across different regions

* 📈 **Time-Based Trend Analysis**
  Identify sales and profit trends over time

* 🚚 **Shipping Mode Analysis**
  Evaluate how shipping methods impact overall performance

* ⚠️ **Loss Detection & Risk Areas**
  Highlight sub-categories that consistently underperform

* 🔮 **Sales Forecasting (ARIMA Model)**
  Predict future sales trends using time series analysis

* 💡 **Business Insights & Recommendations**
  The dashboard includes interpreted insights instead of raw graphs

---

## 🛠️ Tech Stack

* **Python**
* **Pandas** – Data processing and analysis
* **Matplotlib** – Data visualization
* **Streamlit** – Interactive dashboard
* **Statsmodels (ARIMA)** – Time series forecasting

---

## 📂 Dataset

* Superstore dataset (`superstore.csv`)
* Source: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final?resource=download
* Contains information about sales, profit, categories, regions, and shipping details

---

## 🚀 How to Run

1. Clone the repository
2. Install required libraries (will be added in `requirements.txt`)
3. Open the project

⚠️ Important:

* Update the dataset file path in the code before running
* Example:

  ```python
  df = pd.read_csv("your_path/superstore.csv")
  ```

4. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

---

## 🧪 Note on main.py

* `main.py` is used for testing and experimentation purposes
* It does **not have any direct relation to the Streamlit dashboard (`app.py`)**
* It may contain exploratory or trial code

---

## 📌 Limitations

* Forecasting model (ARIMA) is implemented with fixed parameters and not fully optimized
* Dataset is static and does not update in real-time
* Code structure can be improved further for modularity and scalability

---

## 📈 Learning Outcomes

Through this project, we gained practical experience in:

* Data cleaning and preprocessing
* Exploratory data analysis (EDA)
* Data visualization techniques
* Basic time series forecasting
* Converting data insights into business recommendations

---

## 🔍 Future Improvements

* Improve model accuracy with better parameter tuning
* Refactor code into modular structure
* Add interactive filters and advanced UI features
* Integrate real-time or larger datasets

---

## 📎 Conclusion

This project represents an effort to bridge the gap between **data analysis and business decision-making**. It demonstrates how raw data can be transformed into meaningful insights that help in understanding performance and guiding actions.

While not a production-level system, it reflects a solid foundation in applying analytics concepts to solve practical problems.

---
