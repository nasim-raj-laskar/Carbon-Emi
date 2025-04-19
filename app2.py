from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import joblib
import numpy as np
import json
from datetime import datetime


model = joblib.load("xmodel.pkl")
scaler = joblib.load("xscaler.pkl")

with open("metadata.json") as f:
    metadata = json.load(f)

feature_order = metadata["feature_order"]
interaction_terms = metadata.get("interaction_terms", {})


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictionsNew.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    energy_kwh = db.Column(db.Float, nullable=False)
    transport_km = db.Column(db.Float, nullable=False)
    waste_kg = db.Column(db.Float, nullable=False)
    predicted_emission = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        
        input_values = {feat: float(data.get(feat, 0)) for feat in feature_order}
        features = [input_values[feat] for feat in feature_order]


        for key, expr in interaction_terms.items():
            var1, _, var2 = expr.split()
            interaction = input_values[var1] * input_values[var2]
            features.append(interaction)

        scaled_input = scaler.transform([features])
        prediction = model.predict(scaled_input)[0]

       
        new_pred = Prediction(
            energy_kwh=input_values["energy_kwh"],
            transport_km=input_values["transport_km"],
            waste_kg=input_values["waste_kg"],
            predicted_emission=float(prediction)
        )
        db.session.add(new_pred)
        db.session.commit()

        
        return jsonify({"predicted_emission_kg": round(float(prediction), 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/allpredictions", methods=["GET"])
def get_predictions():
    all_preds = Prediction.query.all()
    results = [
        {
            "id": pred.id,
            "energy_kwh": pred.energy_kwh,
            "transport_km": pred.transport_km,
            "waste_kg": pred.waste_kg,
            "predicted_emission": pred.predicted_emission,
            "timestamp": pred.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for pred in all_preds
    ]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
