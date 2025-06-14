# 🚖 Ride-Sharing Dynamic Pricing Estimator

This project implements a dynamic pricing engine for a ride-sharing platform using machine learning. It predicts adjusted ride prices based on real-time demand-supply and ride features.

## 🔍 Overview

- 📊 Model: Trained AdaBoost Regressor with feature engineering and label encoding
- 🎯 Goal: Predict dynamic price based on rider behavior, ratings, location, booking time, and more
- 🖥️ Deployment: Interactive Streamlit app for real-time price estimation
- 📁 Files:
  - `final_ada_model.pkl`: Trained ML model
  - `dynamic_pricing_notebook.ipynb`: Full EDA, preprocessing, and model training
  - `app.py`: Streamlit application script
  - `requirements.txt`: Python dependencies

---

## 🚀 How to Run

### 1. Clone this Repository

```bash
git clone https://github.com/your-username/ride-sharing-dynamic-pricing.git
cd ride-sharing-dynamic-pricing
```

### 2. Install Dependencies
We recommend using a virtual environment.

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit App

```bash
streamlit run app.py
```
## 🧠 Model Inputs

| Feature                   | Description                                |
| ------------------------- | ------------------------------------------ |
| `Number_of_Riders`        | Total ride requests                        |
| `Number_of_Drivers`       | Available drivers                          |
| `Location_Category`       | Urban/Suburban/Rural                       |
| `Customer_Loyalty_Status` | Loyalty status (e.g., Regular/Silver/Gold) |
| `Number_of_Past_Rides`    | Past ride count                            |
| `Average_Ratings`         | Rider's average rating                     |
| `Time_of_Booking`         | Booking time (e.g., Morning/Night)         |
| `Vehicle_Type`            | Economy or Premium                         |
| `Expected_Ride_Duration`  | In minutes                                 |
| `Historical_Cost_of_Ride` | Previous ride cost                         |

## 🔁 Feature Engineering

 - Demand_Supply_Ratio = Riders / (Drivers + 1)
 - Ride_Experience_Level = Categorical bins of past rides
 - Rating_Level = Categorical bins of ratings

## ⚙️ Dynamic Pricing Logic

The prediction is adjusted based on:
- Short Rides: -10% if under 15 minutes
- Long Rides: +20% if over 45 minutes
- Evening/Night: +15% / +25% multiplier
- Premium Vehicle: +10% increase

## 🛠️ Requirements

 - Python 3.8–3.11
 - Streamlit
 - Pandas
 - Scikit-learn
 - Joblib
 - NumPy

All dependencies are listed in requirements.txt.

## 📓 Notebook

See the dynamic_pricing_notebook.ipynb for:
- Data preprocessing
- Feature engineering
- Model training
- Evaluation

## 📬 Contact
For questions or collaboration, reach out to amrisidiq@gmail.com
