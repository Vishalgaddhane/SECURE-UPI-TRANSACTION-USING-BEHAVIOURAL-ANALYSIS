import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

# Load dataset
df = pd.read_csv('behavioral_deviation_dataset.csv')

features = ['amount', 'hour', 'user_id_enc', 'merchant_enc', 'transaction_type_enc',
            'location_enc', 'device_enc', 'avg_amount_per_user', 'txn_count_per_user',
            'amount_dev', 'is_odd_hour', 'device_risk_score',
            'amount_deviation_score', 'hour_deviation_score']

X = df[features]
y = df['is_fraud']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply SMOTE to training data only
smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

print(f"Before SMOTE: {y_train.value_counts()}")
print(f"After SMOTE: {y_train_sm.value_counts()}")

# Train Logistic Regression on balanced data
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train_sm, y_train_sm)
y_pred_lr = lr.predict(X_test)
print("Logistic Regression Classification Report (SMOTE):")
print(classification_report(y_test, y_pred_lr))

# Train Random Forest on balanced data
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_sm, y_train_sm)
y_pred_rf = rf.predict(X_test)
print("Random Forest Classification Report (SMOTE):")
print(classification_report(y_test, y_pred_rf))

# Train XGBoost on balanced data
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb.fit(X_train_sm, y_train_sm)
y_pred_xgb = xgb.predict(X_test)
print("XGBoost Classification Report (SMOTE):")
print(classification_report(y_test, y_pred_xgb))
