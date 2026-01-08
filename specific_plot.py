#Plot Parameters for a Specific Crop
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('Crop_recommendation.csv')

# Specify the crop you want to visualize
crop_name = 'mungbean'  # Replace 'mungbean' with your chosen crop

# Filter the dataset for the specified crop
crop_data = data[data['label'] == crop_name]

# Drop the 'label' column for plotting purposes
parameters = crop_data.drop(columns=['label'])

# Plot each parameter as a boxplot to observe its distribution
plt.figure(figsize=(12, 6))
sns.boxplot(data=parameters)
plt.title(f'Distribution of Parameters for {crop_name.capitalize()}')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.show()
