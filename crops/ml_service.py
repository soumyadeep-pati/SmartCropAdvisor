from ml.prediction import predict_crop
def generate_crop_prediction():

    crop = predict_crop(
        90,
        42,
        43,
        20,
        80,
        6.5,
        200
    )

    return crop