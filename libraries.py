#Import Necessary Libraries

# Basic libraries
import pandas as pd
import numpy as np

# Machine learning libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# Utility libraries
import joblib  # For saving the model
from google.colab import drive  # For accessing Google Drive

