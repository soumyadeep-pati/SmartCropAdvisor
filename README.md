# Smart Crop Advisor

An AI-powered crop recommendation system built with Django, Machine Learning, and Weather APIs.

## Features

* User Authentication
* Soil Data Management
* Real-Time Weather Integration
* Machine Learning Crop Prediction
* Prediction Confidence Score
* Prediction History
* Analytics Dashboard
* Crop Distribution Charts
* PDF Report Export

## Tech Stack

### Backend

* Django
* Python

### Machine Learning

* Scikit-Learn
* Random Forest Classifier

### Database

* SQLite

### Frontend

* Bootstrap 5
* Chart.js

### APIs

* OpenWeatherMap API

## Project Workflow

User Login
↓
Enter Soil Data
↓
Fetch Weather Data
↓
Run ML Model
↓
Recommend Crop
↓
Save Prediction
↓
Analytics Dashboard
↓
Download PDF Report

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

## Future Improvements

* Rainfall API Integration
* Email Reports
* Mobile Application
* Multi-language Support
* Deep Learning Models

## Author

Soumyadeep Pati
