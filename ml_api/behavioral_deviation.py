import pandas as pd

# Load datasets
df_transactions = pd.read_csv('feature_engineered_dataset.csv')
df_profiles = pd.read_csv('user_behavior_profiles.csv')

# Merge user profiles with transactions on user_id_enc
df = pd.merge(df_transactions, df_profiles, on='user_id_enc', how='left')

# Calculate deviations:
df['amount_deviation_score'] = (df['amount'] - df['avg_amount']).abs()

# Hour deviation (absolute difference, considering 24-hour wrap)
def hour_deviation(txn_hour, avg_hour):
    diff = abs(txn_hour - avg_hour)
    return min(diff, 24 - diff)  # to handle wrap-around like 23 and 1 hour

df['hour_deviation_score'] = df.apply(lambda x: hour_deviation(x['hour'], x['avg_hour']), axis=1)

# Optional: Normalize or scale deviations if needed (for this prototype, absolute values suffice)

# Save final dataset with deviation features
df.to_csv('behavioral_deviation_dataset.csv', index=False)
print("Behavioral deviation features added and saved as behavioral_deviation_dataset.csv")

