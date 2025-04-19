import pytest
import numpy as np
from predict_emission import CarbonPredictor

@pytest.fixture
def predictor():
    try:
        return CarbonPredictor()
    except Exception as e:
        pytest.skip(f"Could not initialize predictor: {e}")

def test_prediction_outputs(predictor):
    assert isinstance(predictor.predict(2000, 50, 30), float)
    assert predictor.predict(0, 0, 0) == 0.0
    assert predictor.predict(1, 1, 1) < 10
    assert 300 < predictor.predict(2000, 50, 30) < 800
    assert predictor.predict(10000, 500, 200) > 1000

def test_logical_behavior(predictor):
    e1 = predictor.predict(5000, 10, 5)
    e2 = predictor.predict(100, 200, 5)
    assert e1 > e2  

def test_input_validation(predictor):
    with pytest.raises(ValueError, match="non-negative"):
        predictor.predict(-1, 50, 20)

    with pytest.raises(ValueError, match="Exactly 3 inputs required"):
        predictor.predict(1500, 50)

    with pytest.raises(ValueError, match="numeric"):
        predictor.predict("1000", 50, 20)

def test_feature_engineering(predictor):
    features = predictor._prepare_features(100, 10, 5)
    expected = np.array([[100, 10, 5, 1000, 500]])
    
    assert features.shape == (1, 5)
    assert np.allclose(features, expected)

if __name__ == "__main__":
    print("\n=== Running Prediction Demo ===")
    try:
        pred = CarbonPredictor()
        print("✅ Model loaded successfully")
        test_inputs = [
            (2000, 50, 30),
            (0, 0, 0),
            (1, 1, 1),
            (10000, 500, 200),
            (5000, 10, 5),
            (100, 200, 5)
        ]
        for case in test_inputs:
            try:
                result = pred.predict(*case)
                print(f"Input: {case} → {result:.2f} kg CO2")
            except ValueError as e:
                print(f"Invalid input {case}: {e}")
    except Exception as e:
        print(f"❌ Could not initialize predictor: {e}")
