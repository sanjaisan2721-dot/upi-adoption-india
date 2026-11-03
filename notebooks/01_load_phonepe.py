import json
import os
import pandas as pd

BASE = "data/raw/pulse/data"


def load_transactions():
    folder = BASE + "/aggregated/transaction/country/india/state"
    rows = []
    for state in os.listdir(folder):
        for year in os.listdir(folder + "/" + state):
            for file in os.listdir(folder + "/" + state + "/" + year):
                path = folder + "/" + state + "/" + year + "/" + file
                with open(path) as f:
                    data = json.load(f)
                for item in data["data"]["transactionData"]:
                    for inst in item["paymentInstruments"]:
                        rows.append({
                            "state": state,
                            "year": int(year),
                            "quarter": int(file.replace(".json", "")),
                            "category": item["name"],
                            "count": inst.get("count"),
                            "amount": inst.get("amount"),
                        })
    return pd.DataFrame(rows)


def load_users():
    folder = BASE + "/aggregated/user/country/india/state"
    rows = []
    for state in os.listdir(folder):
        for year in os.listdir(folder + "/" + state):
            for file in os.listdir(folder + "/" + state + "/" + year):
                path = folder + "/" + state + "/" + year + "/" + file
                with open(path) as f:
                    data = json.load(f)
                agg = data["data"]["aggregated"]
                registered = agg.get("registeredCount", agg.get("registeredUsers"))
                rows.append({
                    "state": state,
                    "year": int(year),
                    "quarter": int(file.replace(".json", "")),
                    "registered_users": registered,
                    "app_opens": agg.get("appOpens"),
                })
    return pd.DataFrame(rows)


tx = load_transactions()
users = load_users()

print(tx.head())
print("Transactions table size:", tx.shape)
print(users.head())
print("Users table size:", users.shape)

os.makedirs("data/processed", exist_ok=True)
tx.to_csv("data/processed/phonepe_transactions.csv", index=False)
users.to_csv("data/processed/phonepe_users.csv", index=False)
print("Saved both files in data/processed")
