# 🌾 Smart Crop Advisor

An AI-powered crop recommendation system built with Django and Machine Learning.

## Live Demo

https://your-render-url.onrender.com

## Features

* User Authentication (Login/Signup)
* Soil Data Management
* Real-Time Weather Integration
* AI Crop Recommendation
* Prediction Confidence Score
* Prediction History
* Analytics Dashboard
* PDF Report Export
* Docker Support
* Cloud Deployment on Render

## Tech Stack

* Python
* Django
* Scikit-Learn
* SQLite
* Bootstrap
* OpenWeather API
* Docker
* Git & GitHub
* Render

## Screenshots

(Add screenshots here)

## Installation

```bash
git clone <repository-url>
cd SmartCropAdvisor

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

## Machine Learning

The project uses a Random Forest Classifier trained on crop recommendation data.

Input Features:

* Nitrogen
* Phosphorus
* Potassium
* Temperature
* Humidity
* pH
* Rainfall

Output:

* Recommended Crop
* Confidence Score

## Future Improvements

* Crop Disease Detection
* Fertilizer Recommendation
* Yield Prediction
* Multi-language Support
* Weather Forecast Based Recommendation
