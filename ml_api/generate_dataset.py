import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

NUM_SAMPLES = 6000

user_ids = [f"user_{i}" for i in range(1, 51)]

merchants = ['Amazon', 'Flipkart', 'Walmart', 'Paytm', 'Swiggy', 'Zomato']
transaction_types = ['send', 'request', 'refund']
locations = ['Pune', 'Mumbai', 'Delhi', 'Bangalore', 'Chennai']
devices = ['Android', 'iOS', 'Web']

user_profiles = {}
for uid in user_ids:
    roll = random.random()
    if roll < 0.6:
        low, high = 200, 5000
    elif roll < 0.9:
        low, high = 5000, 20000
    else:
        low, high = 15000, 60000
    user_profiles[uid] = {'low': low, 'high': high, 'mean': (low + high) / 2}


def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))


start_date = datetime.now() - timedelta(days=60)
end_date = datetime.now()

data = []

for i in range(NUM_SAMPLES):
    user = random.choice(user_ids)
    profile = user_profiles[user]

    roll = random.random()

    if roll < 0.88:
        amount = round(random.uniform(profile['low'], profile['high']), 2)
    elif roll < 0.96:
        multiplier = random.uniform(1.5, 3)
        amount = round(profile['high'] * multiplier, 2)
    else:
        multiplier = random.uniform(3, 8)
        amount = round(profile['high'] * multiplier, 2)

    amount = min(amount, 300000)

    timestamp = random_date(start_date, end_date)
    merchant = random.choice(merchants)
    txn_type = random.choice(transaction_types)
    location = random.choice(locations)
    device = random.choice(devices)

    deviation_ratio = amount / profile['mean']

    if deviation_ratio <= 1.6:
        base_fraud_prob = 0.05
    elif deviation_ratio <= 3.2:
        base_fraud_prob = 0.45
    else:
        base_fraud_prob = 0.85

    device_risk = 0.08 if device == 'Web' else 0.0
    fraud_prob = min(base_fraud_prob + device_risk, 0.97)

    is_fraud = np.random.choice([0, 1], p=[1 - fraud_prob, fraud_prob])

    data.append([i + 1, user, amount, timestamp, merchant, txn_type, location, device, is_fraud])

df = pd.DataFrame(data, columns=['transaction_id', 'user_id', 'amount', 'timestamp', 'merchant',
                                  'transaction_type', 'location', 'device_info', 'is_fraud'])

df.to_csv('synthetic_transactions.csv', index=False)
print("Synthetic dataset created: synthetic_transactions.csv")
print(f"Fraud rate: {df['is_fraud'].mean():.2%}")

tiers = {'low': 0, 'mid': 0, 'high': 0}
for p in user_profiles.values():
    if p['high'] <= 5000:
        tiers['low'] += 1
    elif p['high'] <= 20000:
        tiers['mid'] += 1
    else:
        tiers['high'] += 1
print(f"User spending tiers: {tiers}")