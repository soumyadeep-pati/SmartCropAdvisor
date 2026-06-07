import joblib
import pandas as pd

model = joblib.load("ml/models/model.pkl")


def predict_crop(
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    ph,
    rainfall
):

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