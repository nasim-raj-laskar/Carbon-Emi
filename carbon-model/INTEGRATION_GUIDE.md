# Carbon Emission Prediction Model - Integration Guide
## Model Overview
XGBoost regression model for predicting CO2 emissions (kg) based on:
- Energy consumption (kWh)
- Transport distance (km)
- Waste produced (kg)
## Project Structure

```plaintext
carbon-model/
├── 📁 model/
│   ├── 📄 xmodel.json          # Trained XGBoost model
│   ├── 📄 xscaler.pkl          # Fitted StandardScaler
│   └── 📄 metadata.json        # Feature specifications
├── 📁 script/
│   └── 📄 Carbon-Emi-Pred.ipynb       # Model training script
├── 📁 dataset/
│   └── 📄 carbon_footprint_dataset.csv  # Training data
├── 📄 predict_emission.py      # Prediction interface
├── 📄 requirements.txt         # Python dependencies
└── 📄 test_integration.py      # Test cases
```
## Setup
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Run the Prediction Class
   ```bash
   python3 -m carbon-model.predict_emission.py
   ```
3. Run the Test Cases
   ```bash
   python3 -m carbon-model.test_integration.py
   ```

## Input Specifications

| Parameter      | Type  | Constraints | Description            |
|----------------|-------|-------------|------------------------|
| `energy_kwh`   | float | ≥ 0         | Energy consumption     |
| `transport_km` | float | ≥ 0         | Transportation distance|
| `waste_kg`     | float | ≥ 0         | Waste produced         |
## Output
- Returns float representing predicted CO2 emissions in kilograms

- Typical range: 0-5000 kg (depends on inputs)

