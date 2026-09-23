import joblib
import pandas as pd

le_user = joblib.load('saved_encoders/le_user.pkl')
profiles = pd.read_csv('user_behavior_profiles.csv').set_index('user_id_enc')

# Check a few specific literal user IDs
for uid in ['user_1', 'user_4', 'user_12', 'user_30']:
    try:
        enc = le_user.transform([uid])[0]
        if enc in profiles.index:
            row = profiles.loc[enc]
            print(f"{uid} -> encoded {enc} -> avg_amount: {row['avg_amount']:.2f}, txn_count: {row['txn_count']:.0f}")
        else:
            print(f"{uid} -> encoded {enc} -> NOT FOUND in profiles (would use -1 fallback)")
    except ValueError:
        print(f"{uid} -> not seen during training at all")