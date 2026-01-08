#Predict the Crop Based on Rainfall
# Get user input for rainfall
rainfall = float(input("Enter the rainfall value (in mm): "))

# Define default parameter values (you can modify these)
default_values = {
    'N': 50,  # Example Nitrogen value
    'P': 40,  # Example Phosphorus value
    'K': 30,  # Example Potassium value
    'temperature': 25.0,  # Example temperature in Celsius
    'humidity': 70.0,     # Example humidity in percentage
    'ph': 6.5,            # Example pH value
    'rainfall': rainfall  # Use user-input rainfall
}

# Create a DataFrame from the user inputs
input_data = pd.DataFrame([default_values])

# Predict the crop
predicted_crop = model.predict(input_data)[0]
print(f"The best crop for the given conditions is: {predicted_crop}")
