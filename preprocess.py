#Explore and Preprocess the Data
# Check for missing values
print("Missing values in each column:")
print(data.isnull().sum())

# If there are missing values, drop them
data.dropna(inplace=True)

# Display data types and summary
print(data.info())
print(data.describe())
