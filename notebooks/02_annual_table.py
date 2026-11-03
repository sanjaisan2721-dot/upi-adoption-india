import pandas as pd

tx = pd.read_csv("data/processed/phonepe_transactions.csv")
us = pd.read_csv("data/processed/phonepe_users.csv")

# Yearly transactions per state (sum of all quarters and categories)
txn = tx.groupby(["state", "year"], as_index=False)["count"].sum()
txn = txn.rename(columns={"count": "transactions"})

# How many quarters each year actually has (to spot partial years)
q = tx.groupby(["state", "year"])["quarter"].nunique().reset_index(name="quarters")
txn = txn.merge(q, on=["state", "year"])

# Registered users: take the latest quarter of each year
us = us.sort_values(["state", "year", "quarter"])
last = us.groupby(["state", "year"], as_index=False).last()
last = last[["state", "year", "registered_users"]]

annual = txn.merge(last, on=["state", "year"], how="left")
annual["txn_per_user"] = annual["transactions"] / annual["registered_users"]

annual.to_csv("data/processed/phonepe_annual.csv", index=False)
print(annual.head(10))
print(annual.groupby("year")["transactions"].sum())
print(annual["quarters"].value_counts())
