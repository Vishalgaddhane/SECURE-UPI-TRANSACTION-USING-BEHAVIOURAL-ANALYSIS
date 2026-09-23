import pandas as pd

# Load processed dataset
df = pd.read_csv('processed_transactions.csv')

# 1. Average transaction amount per user
avg_amount_per_user = df.groupby('user_id_enc')['amount'].transform('mean')
df['avg_amount_per_user'] = avg_amount_per_user

# 2. Transaction count per user
txn_count_per_user = df.groupby('user_id_enc')['amount'].transform('count')
df['txn_count_per_user'] = txn_count_per_user

# 3. Amount deviation from average per user
df['amount_dev'] = df['amount'] - df['avg_amount_per_user']

# 4. Flag transactions happening between 0 to 6 AM as odd hours
df['is_odd_hour'] = df['hour'].apply(lambda x: 1 if 0 <= x <= 6 else 0)

# 5. Device risk score (Example assumptions)
device_risk_map = {
    0: 0.1,  # Android
    1: 0.2,  # iOS
    2: 0.5   # Web - assumed more risky
}
df['device_risk_score'] = df['device_enc'].map(device_risk_map)

# Save the enhanced dataset
df.to_csv('feature_engineered_dataset.csv', index=False)
print("Feature engineered dataset saved as feature_engineered_dataset.csv")
