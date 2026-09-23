import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib

# Load dataset
df = pd.read_csv('behavioral_deviation_dataset.csv')

features = ['amount', 'hour', 'user_id_enc', 'merchant_enc', 'transaction_type_enc',
            'location_enc', 'device_enc', 'avg_amount_per_user', 'txn_count_per_user',
            'amount_dev', 'is_odd_hour', 'device_risk_score',
            'amount_deviation_score', 'hour_deviation_score']

X = df[features]
y = df['is_fraud']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model (XGBoost recommended)
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb.fit(X_train, y_train)

# Save model to 'saved_models' folder
joblib.dump(xgb, 'saved_models/xgb_fraud_model.pkl')
print("Model saved as saved_models/xgb_fraud_model.pkl")
