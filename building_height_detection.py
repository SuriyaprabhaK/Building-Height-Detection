# -*- coding: utf-8 -*-
"""building height detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ckw1SRBzb6HrCcP6imA1cgdPLqc-4Mu8
"""

import os
HOME = os.getcwd()
print(HOME)

# Pip install method (recommended)

!pip install ultralytics==8.0.196

from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()

from ultralytics import YOLO

from IPython.display import display, Image

# Commented out IPython magic to ensure Python compatibility.
!mkdir {HOME}/datasets
# %cd {HOME}/datasets

!pip install roboflow
!pip install roboflow

# from roboflow import Roboflow
# rf = Roboflow(api_key="yy4yNFaODSlGo8Xe9QvI")
# project = rf.workspace("guy").project("city-6415d")
# dataset = project.version(5).download("yolov8")

!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="Y0kwapaVxCxO3gu3wAc7")
project = rf.workspace("suriya-sipom").project("building-xvagu")
dataset = project.version(1).download("yolov8")

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}

!yolo task=detect mode=train model=yolov8s.pt data={dataset.location}/data.yaml epochs=25 imgsz=800 plots=True

!ls {HOME}/runs/detect/train/

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/PR_curve.png',width=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/results.png', width=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
Image(filename=f'{HOME}/runs/detect/train/val_batch0_pred.jpg', width=600)

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Example dataset
data = {
    'Building_ID': [1, 2, 3, 4, 5],
    'Number_of_Floors': [10, 8, 15, 12, 6],
    'Area_Square_Meters': [500, 400, 750, 600, 300],
    'Location': ['City A', 'City B', 'City C', 'City A', 'City B'],
    'Height_Meters': [30, 25, 45, 35, 20]
}

df = pd.DataFrame(data)

# Features (X) and target variable (y)
X = df[['Number_of_Floors', 'Area_Square_Meters']]
y = df['Height_Meters']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Regressor with hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf_model_tuned = RandomForestRegressor()

# Grid search with cross-validation
grid_search = GridSearchCV(rf_model_tuned, param_grid, cv=4, scoring='neg_mean_absolute_error')
grid_search.fit(X_train, y_train)

# Best hyperparameters
best_params = grid_search.best_params_
print(f'Best Hyperparameters: {best_params}')

# Evaluate the model with the best hyperparameters on the test set
tuned_rf_predictions = grid_search.predict(X_test)
tuned_rf_mae = mean_absolute_error(y_test, tuned_rf_predictions)
print(f'Mean Absolute Error (Tuned Random Forest): {tuned_rf_mae}')

# Predict the height of a new building using the tuned model
new_building_features = pd.DataFrame({'Number_of_Floors': [8], 'Area_Square_Meters': [450]})
tuned_rf_predicted_height = grid_search.predict(new_building_features)
print(f'Predicted Height (Tuned Random Forest) for the new building: {tuned_rf_predicted_height[0]}')



















