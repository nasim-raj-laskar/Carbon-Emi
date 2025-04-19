from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import joblib
import pandas as pd
from datetime import datetime

   
model = joblib.load("decision_tree_model.pkl")

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
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
        energy = float(data.get("energy_kwh", 0))
        transport = float(data.get("transport_km", 0))
        waste = float(data.get("waste_kg", 0))

       
        input_features = pd.DataFrame([{
            "energy_kwh": energy,
            "transport_km": transport,
            "waste_kg": waste
        }])

        prediction = round(model.predict(input_features)[0], 2)

    
        new_entry = Prediction(
            energy_kwh=energy,
            transport_km=transport,
            waste_kg=waste,
            predicted_emission=prediction
        )
        db.session.add(new_entry)
        db.session.commit()  

        return jsonify({
            "predicted_emission_kg": prediction
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/allpredictions", methods=["GET"])
def get_prediction():
    all_pred = Prediction.query.order_by(Prediction.timestamp.desc()).all()
    results = [
        {
            "id": pred.id,
            "energy_kwh": pred.energy_kwh,
            "transport_km": pred.transport_km,
            "waste_kg": pred.waste_kg,
            "predicted_emission": pred.predicted_emission,
            "timestamp": pred.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for pred in all_pred
    ]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
