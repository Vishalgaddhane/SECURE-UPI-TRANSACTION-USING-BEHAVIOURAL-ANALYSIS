import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv('synthetic_transactions.csv')

# Check missing values
print(df.isnull().sum())

# Convert timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour

# Create LabelEncoder objects
le_user = LabelEncoder()
le_merchant = LabelEncoder()
le_txn_type = LabelEncoder()
le_location = LabelEncoder()
le_device = LabelEncoder()

# Encode categorical columns
df['user_id_enc'] = le_user.fit_transform(df['user_id'])
df['merchant_enc'] = le_merchant.fit_transform(df['merchant'])
df['transaction_type_enc'] = le_txn_type.fit_transform(df['transaction_type'])
df['location_enc'] = le_location.fit_transform(df['location'])
df['device_enc'] = le_device.fit_transform(df['device_info'])

# Save processed dataset including encoded columns
df.to_csv('processed_transactions.csv', index=False)
print("Processed dataset saved as processed_transactions.csv")

import joblib
import os

os.makedirs('saved_encoders', exist_ok=True)
joblib.dump(le_user, 'saved_encoders/le_user.pkl')
joblib.dump(le_merchant, 'saved_encoders/le_merchant.pkl')
joblib.dump(le_txn_type, 'saved_encoders/le_txn_type.pkl')
joblib.dump(le_location, 'saved_encoders/le_location.pkl')
joblib.dump(le_device, 'saved_encoders/le_device.pkl')
print("Encoders saved to saved_encoders/")