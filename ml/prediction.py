import joblib

model = joblib.load(
    "ml/models/model.pkl"
)


def predict_crop(
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    ph,
    rainfall
):

    prediction = model.predict([
        [
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall
        ]
    ])

    return prediction[0]