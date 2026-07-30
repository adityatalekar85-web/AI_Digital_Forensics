import random
import pandas as pd
from datetime import datetime, timedelta

# ----------------------------
# Sample Data
# ----------------------------

usernames = [
    "admin","rahul","aditya","komal","amit","priya","john","alice",
    "bob","sneha","guest","test","rohit","pooja","vijay","anita"
]

countries = [
    "India","USA","Germany","Russia","China",
    "Brazil","Nigeria","Japan","Australia","UK"
]

devices = [
    "Laptop","Desktop","Mobile"
]

os_list = [
    "Windows","Linux","Ubuntu","Android","macOS"
]

browsers = [
    "Chrome","Edge","Firefox","Safari"
]

attack_types = [
    "Safe",
    "Brute Force",
    "Phishing",
    "Malware",
    "Credential Stuffing"
]

# ----------------------------
# Generate Dataset
# ----------------------------

rows = []

start_time = datetime(2026, 1, 1, 8, 0, 0)

for i in range(1, 1001):

    timestamp = start_time + timedelta(minutes=random.randint(1, 50000))

    failed_attempts = random.randint(0, 8)

    if failed_attempts >= 4:
        login_status = "Failed"
        threat = "Threat"
        risk = random.randint(70, 100)
        attack = random.choice(attack_types[1:])
    else:
        login_status = "Success"
        threat = "Safe"
        risk = random.randint(1, 40)
        attack = "Safe"

    rows.append({
        "Log_ID": i,
        "Timestamp": timestamp,
        "Username": random.choice(usernames),
        "IP_Address": f"192.168.{random.randint(0,255)}.{random.randint(1,254)}",
        "Country": random.choice(countries),
        "Login_Status": login_status,
        "Failed_Attempts": failed_attempts,
        "Device": random.choice(devices),
        "OS": random.choice(os_list),
        "Browser": random.choice(browsers),
        "Risk_Score": risk,
        "Attack_Type": attack,
        "Threat_Label": threat
    })

# ----------------------------
# Save CSV
# ----------------------------

df = pd.DataFrame(rows)

df.to_csv("datasets/sample_logs.csv", index=False)

print("✅ Dataset Generated Successfully")
print(df.head())