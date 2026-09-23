import pandas as pd

# Load feature engineered dataset
df = pd.read_csv('feature_engineered_dataset.csv')

# Group by user to compute behavioral stats
user_profiles = df.groupby('user_id_enc').agg(
    avg_amount=('amount', 'mean'),
    txn_count=('amount', 'count'),
    avg_hour=('hour', 'mean')
).reset_index()

# Add a fallback profile for users not seen during training
# (used when a brand-new user_id shows up in a live transaction later)
global_profile = pd.DataFrame([{
    'user_id_enc': -1,  # -1 = sentinel value meaning "unknown user"
    'avg_amount': df['amount'].mean(),
    'txn_count': df.groupby('user_id_enc')['amount'].count().mean(),
    'avg_hour': df['hour'].mean()
}])

user_profiles = pd.concat([user_profiles, global_profile], ignore_index=True)

print(user_profiles.head())

# Save user profiles for later use
user_profiles.to_csv('user_behavior_profiles.csv', index=False)
print("User behavioral profiles saved as user_behavior_profiles.csv")