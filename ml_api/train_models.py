import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Load dataset
df = pd.read_csv('behavioral_deviation_dataset.csv')

# Select features and target
features = ['amount', 'hour', 'user_id_enc', 'merchant_enc', 'transaction_type_enc',
            'location_enc', 'device_enc', 'avg_amount_per_user', 'txn_count_per_user',
            'amount_dev', 'is_odd_hour', 'device_risk_score',
            'amount_deviation_score', 'hour_deviation_score']

X = df[features]
y = df['is_fraud']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Logistic Regression
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

print("Logistic Regression Classification Report:")
print(classification_report(y_test, y_pred_lr))

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("Random Forest Classification Report:")
print(classification_report(y_test, y_pred_rf))

# XGBoost
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)

print("XGBoost Classification Report:")
print(classification_report(y_test, y_pred_xgb))

# Isolation Forest (unsupervised anomaly detection)
# Note: We use Isolation Forest differently as it doesn’t need labels
iso_forest = IsolationForest(contamination=0.05, random_state=42)
iso_forest.fit(X_train)
# anomaly score: -1 for anomaly, 1 for normal
y_pred_iso = iso_forest.predict(X_test)
# Convert to 0 (normal), 1 (anomaly)
y_pred_iso = [0 if x == 1 else 1 for x in y_pred_iso]

print("Isolation Forest Classification Report:")
print(classification_report(y_test, y_pred_iso))
