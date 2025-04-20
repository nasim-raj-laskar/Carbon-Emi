from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import json
from datetime import datetime
from xgboost import XGBRegressor

model = XGBRegressor()
model.load_model("xmodel.json")     
scaler = joblib.load("xscaler.pkl")  
with open("metadata.json", "r") as f:
    metadata = json.load(f)

feature_order     = metadata["feature_order"]
interaction_terms = metadata.get("interaction_terms", {})


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Prediction(db.Model):
    id                 = db.Column(db.Integer, primary_key=True)
    energy_kwh         = db.Column(db.Float,   nullable=False)
    transport_km       = db.Column(db.Float,   nullable=False)
    waste_kg           = db.Column(db.Float,   nullable=False)
    predicted_emission = db.Column(db.Float,   nullable=False)
    timestamp          = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        
        inputs = {feat: float(data.get(feat, 0)) for feat in feature_order}
        features = [inputs[feat] for feat in feature_order]

        
        for expr in interaction_terms.values():
            var1, _, var2 = expr.split()
            features.append(inputs[var1] * inputs[var2])

       
        X_in = scaler.transform([features])
        pred = model.predict(X_in)[0]

        
        entry = Prediction(
            energy_kwh=inputs["energy_kwh"],
            transport_km=inputs["transport_km"],
            waste_kg=inputs["waste_kg"],
            predicted_emission=float(pred)
        )
        db.session.add(entry)
        db.session.commit()

        
        return jsonify({"predicted_emission_kg": round(float(pred), 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400



@app.route("/allpredictions", methods=["GET"])
def get_all():
    rows = Prediction.query.order_by(Prediction.timestamp.desc()).all()
    return jsonify([{
        "id": pred.id,
        "energy_kwh": pred.energy_kwh,
        "transport_km": pred.transport_km,
        "waste_kg": pred.waste_kg,
        "predicted_emission": pred.predicted_emission,
        "timestamp": pred.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for pred in rows])

if __name__ == "__main__":
    app.run(debug=True)
