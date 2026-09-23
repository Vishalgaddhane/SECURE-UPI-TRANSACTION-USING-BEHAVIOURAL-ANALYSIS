from flask import Flask, request, jsonify
import joblib
import pandas as pd
import shap
import numpy as np
from datetime import datetime

app = Flask(__name__)

model = joblib.load('saved_models/xgb_fraud_model.pkl')

le_user = joblib.load('saved_encoders/le_user.pkl')
le_merchant = joblib.load('saved_encoders/le_merchant.pkl')
le_txn_type = joblib.load('saved_encoders/le_txn_type.pkl')
le_location = joblib.load('saved_encoders/le_location.pkl')
le_device = joblib.load('saved_encoders/le_device.pkl')

user_profiles = pd.read_csv('user_behavior_profiles.csv').set_index('user_id_enc')

DEVICE_RISK_MAP = {
    'Android': 0.1,
    'iOS': 0.2,
    'Web': 0.5,
}
DEFAULT_DEVICE_RISK = 0.3

NEW_USER_LOW_MAX = 5000
NEW_USER_MEDIUM_MAX = 20000
NEW_USER_LOW_SCORE = 15.0
NEW_USER_MEDIUM_SCORE = 50.0
NEW_USER_HIGH_SCORE = 85.0

FEATURES = ['amount', 'hour', 'user_id_enc', 'merchant_enc', 'transaction_type_enc',
            'location_enc', 'device_enc', 'avg_amount_per_user', 'txn_count_per_user',
            'amount_dev', 'is_odd_hour', 'device_risk_score',
            'amount_deviation_score', 'hour_deviation_score']

explainer = shap.TreeExplainer(model)


def safe_encode(encoder, value):
    try:
        return int(encoder.transform([value])[0])
    except ValueError:
        return -1


def safe_model_input(encoded_value):
    return encoded_value if encoded_value != -1 else 0


def get_user_profile(user_id_enc):
    if user_id_enc in user_profiles.index:
        row = user_profiles.loc[user_id_enc]
    else:
        row = user_profiles.loc[-1]
    return float(row['avg_amount']), float(row['txn_count']), float(row['avg_hour'])


def hour_deviation(txn_hour, avg_hour):
    diff = abs(txn_hour - avg_hour)
    return min(diff, 24 - diff)


def risk_level_for_score(risk_score):
    if risk_score < 30:
        return 'Low'
    elif risk_score < 70:
        return 'Medium'
    else:
        return 'High'


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    try:
        user_id = data['user_id']
        amount = float(data['amount'])
        merchant = data['merchant']
        transaction_type = data['transaction_type']
        location = data['location']
        device_info = data['device_info']

        if 'hour' in data:
            hour = int(data['hour'])
        else:
            timestamp = pd.to_datetime(data['timestamp'])
            hour = timestamp.hour

        user_id_enc_raw = safe_encode(le_user, user_id)
        merchant_enc_raw = safe_encode(le_merchant, merchant)
        transaction_type_enc_raw = safe_encode(le_txn_type, transaction_type)
        location_enc_raw = safe_encode(le_location, location)
        device_enc_raw = safe_encode(le_device, device_info)

        is_known_user = user_id_enc_raw != -1

        avg_amount, txn_count, avg_hour = get_user_profile(user_id_enc_raw)

        avg_amount_per_user = avg_amount
        txn_count_per_user = txn_count
        amount_dev = amount - avg_amount_per_user
        is_odd_hour = 1 if 0 <= hour <= 6 else 0
        device_risk_score = DEVICE_RISK_MAP.get(device_info, DEFAULT_DEVICE_RISK)
        amount_deviation_score = abs(amount - avg_amount)
        hour_deviation_score = hour_deviation(hour, avg_hour)

        feature_row = {
            'amount': amount,
            'hour': hour,
            'user_id_enc': safe_model_input(user_id_enc_raw),
            'merchant_enc': safe_model_input(merchant_enc_raw),
            'transaction_type_enc': safe_model_input(transaction_type_enc_raw),
            'location_enc': safe_model_input(location_enc_raw),
            'device_enc': safe_model_input(device_enc_raw),
            'avg_amount_per_user': avg_amount_per_user,
            'txn_count_per_user': txn_count_per_user,
            'amount_dev': amount_dev,
            'is_odd_hour': is_odd_hour,
            'device_risk_score': device_risk_score,
            'amount_deviation_score': amount_deviation_score,
            'hour_deviation_score': hour_deviation_score,
        }

        input_df = pd.DataFrame([feature_row], columns=FEATURES)

        fraud_prob = float(model.predict_proba(input_df)[:, 1][0])
        risk_score = fraud_prob * 100

        if not is_known_user:
            if amount < NEW_USER_LOW_MAX:
                risk_score = NEW_USER_LOW_SCORE
            elif amount <= NEW_USER_MEDIUM_MAX:
                risk_score = NEW_USER_MEDIUM_SCORE
            else:
                risk_score = NEW_USER_HIGH_SCORE
            fraud_prob = risk_score / 100

        risk_level = risk_level_for_score(risk_score)

        shap_values = explainer.shap_values(input_df)
        shap_dict = {feature: float(np.abs(shap_values[0][i]))
                     for i, feature in enumerate(FEATURES)}
        top_features = sorted(shap_dict.items(), key=lambda x: x[1], reverse=True)[:3]
        explanation = {k: v for k, v in top_features}

        response = {
            'fraud_probability': fraud_prob,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'is_flagged': risk_level in ('Medium', 'High'),
            'is_known_user': is_known_user,
            'explanation': explanation
        }

        return jsonify(response)

    except KeyError as e:
        return jsonify({'error': f'Missing required field: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(port=5000, debug=True)