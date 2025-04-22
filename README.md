# 🌍 CO₂ Emission Predictor

**CO₂ Emission Predictor** is a full-stack machine learning web application that estimates carbon dioxide emissions based on user inputs. The primary goal of this project is to raise awareness about environmental sustainability by providing an accessible and interactive way to understand how different factors contribute to CO₂ emissions.

This project was developed as part of a **Hackathon**, demonstrating a practical use-case of ML models integrated into a production-ready web interface. It uses a trained **XGBoost** model on the backend and a sleek **React + Tailwind** frontend for user interaction.

---

## 🔧 Tech Stack

### 🧠 Machine Learning
- **XGBoost** – regression model to predict CO₂ emissions
- **scikit-learn** – for scaling input data
- **Joblib** – to save and load the scaler
- **Pandas/Numpy** – data preprocessing and manipulation

### 🖥️ Backend
- **Flask** – lightweight Python web framework to handle API routes
- **Flask-CORS** – to enable frontend-backend communication
- **Flask-SQLAlchemy** – optional database integration if needed for future scalability

### 🌐 Frontend
- **React** – component-based UI
- **Vite** – fast development server and bundler
- **Tailwind CSS** – modern utility-first styling
- **ESLint** – code linting and style guide enforcement

---

## 📁 Project Structure

```
HackFest-main/
│
├── .gitattributes
├── LICENSE
├── README.md                    # Project documentation
│
├── app2(Backend Server).py      # Flask backend API
├── xmodel.json                  # Trained XGBoost model
├── xscaler.pkl                  # Fitted scaler object
├── metadata.json                # Metadata for input feature ordering
│
├── index.html                   # Entry point HTML file
├── package.json                 # NPM dependencies & scripts
├── package-lock.json
├── tailwind.config.js           # Tailwind configuration
├── postcss.config.js
├── eslint.config.js             # ESLint rules
│
└── src/                         # React source code
    ├── App.jsx                  # Main React app
    ├── main.jsx                 # React entry point
    ├── assets/                  # Images or icons
    └── components/              # Reusable React components
```

---

## 🚀 Getting Started

### 1️⃣ Backend Setup

```bash
# Install dependencies
pip install flask flask_sqlalchemy flask_cors xgboost joblib pandas numpy

# Run the Flask server
python app2\(Backend\ Server\).py
```

### 2️⃣ Frontend Setup

```bash
# Install dependencies
npm install

# Run the development server
npm run dev
```

---

## 📊 How It Works

1. **User Input**: Users enter relevant data such as fuel type, distance, or engine size.
2. **Request Handling**: React sends the data to the Flask backend via HTTP POST.
3. **Model Prediction**: Flask loads the trained XGBoost model and scaler, preprocesses the data, and returns the predicted CO₂ emission.
4. **Result Display**: React updates the UI with the prediction result.

---


