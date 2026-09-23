import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt

# Load preprocessed and feature-engineered dataset
df = pd.read_csv('behavioral_deviation_dataset.csv')

features = ['amount', 'hour', 'user_id_enc', 'merchant_enc', 'transaction_type_enc',
            'location_enc', 'device_enc', 'avg_amount_per_user', 'txn_count_per_user',
            'amount_dev', 'is_odd_hour', 'device_risk_score',
            'amount_deviation_score', 'hour_deviation_score']

X = df[features]
y = df['is_fraud']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train models (using SMOTE or balanced dataset)
lr = LogisticRegression(max_iter=2000)
lr.fit(X_train, y_train)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb.fit(X_train, y_train)

models = {'Logistic Regression': lr, 'Random Forest': rf, 'XGBoost': xgb}

for name, model in models.items():
    print(f"\n=== {name} ===")
    y_pred = model.predict(X_test)
    y_score = model.predict_proba(X_test)[:,1]

    print(classification_report(y_test, y_pred))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)

    # Plot ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f"ROC curve (area = {roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.title(f"ROC Curve for {name}")
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.show()
