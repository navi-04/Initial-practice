import re
import pandas as pd

records = []
current_record = {}

with open("raw_output.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        # Detect the start of a new script's output block
        if line.startswith("===") and line.endswith("==="):
            if current_record:
                records.append(current_record)
                current_record = {}

            match = re.search(r"===\s+\./(.+?)\.py\s+===", line)
            if match:
                current_record["Filename"] = match.group(1).strip() + ".py"
            continue

        # Try to extract GitHub username
        if any(key in line.lower() for key in ["github", "username"]):
            match = re.search(r"(?:github\s*username|username)[:\-\s]*([\w\s\-.@]+)", line, re.IGNORECASE)
            if match:
                current_record["GitHub Username"] = match.group(1).strip()
                continue

        # Try to extract WhatsApp number
        if "whatsapp" in line.lower():
            match = re.search(r"whatsapp(?: number)?[:\-\s]*([0-9]{8,})", line, re.IGNORECASE)
            if match:
                current_record["WhatsApp Number"] = match.group(1).strip()
                continue

        # Fallback: if it's a name and username is missing
        if re.match(r"^[a-zA-Z][a-zA-Z\s\-.@0-9]+$", line) and "GitHub Username" not in current_record:
            current_record["GitHub Username"] = line.strip()
            continue

        # Fallback: if it's a number and WhatsApp is missing
        if re.match(r'^\d{8,}$', line) and "WhatsApp Number" not in current_record:
            current_record["WhatsApp Number"] = line.strip()

# Append last record
if current_record:
    records.append(current_record)

# Create DataFrame
df = pd.DataFrame(records)
df = df[["Filename", "GitHub Username", "WhatsApp Number"]]
df = df.fillna("")

# Save to clean CSV file
df.to_csv("organized_output.csv", index=False)

print(f"✅ Extracted {len(df)} records to organized_output.csv")
