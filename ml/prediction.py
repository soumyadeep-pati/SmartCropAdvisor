import os
import joblib
import pandas as pd

_model = None

def _get_model():
    global _model
    if _model is None:
        model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "models",
            "model.pkl"
        )
        _model = joblib.load(model_path)
    return _model


def predict_crop(
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    ph,
    rainfall
):

    model = _get_model()

    data = pd.DataFrame([{
        "N": nitrogen,
        "P": phosphorus,
        "K": potassium,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }])

    prediction = model.predict(data)

    confidence = max(
        model.predict_proba(data)[0]
    )

    return prediction[0], confidence