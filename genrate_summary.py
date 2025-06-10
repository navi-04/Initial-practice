import os
import re
import pandas as pd

def extract_info_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        username_match = re.search(r'GitHub Username\s*[:=]\s*(.+)', content, re.IGNORECASE)
        whatsapp_match = re.search(r'WhatsApp Number\s*[:=]\s*(.+)', content, re.IGNORECASE)

        return {
            "filename": os.path.basename(filepath),
            "github": username_match.group(1).strip() if username_match else "Not found",
            "whatsapp": whatsapp_match.group(1).strip() if whatsapp_match else "Not found"
        }

    except Exception as e:
        return {
            "filename": os.path.basename(filepath),
            "github": "Error",
            "whatsapp": str(e)
        }

def find_all_py_files(root_dir):
    py_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py") and file != os.path.basename(__file__):
                py_files.append(os.path.join(root, file))
    return py_files

def generate_summary():
    print("🔎 Scanning .py files...")
    data = []

    for filepath in find_all_py_files("."):
        data.append(extract_info_from_file(filepath))

    df = pd.DataFrame(data)

    # Save as summary.csv
    df.to_csv("summary.csv", index=False)

    # Save as readable summary.txt
    with open("summary.txt", "w", encoding='utf-8') as f:
        f.write(df.to_string(index=False))

    print("✅ summary.txt and summary.csv generated successfully.")

if __name__ == "__main__":
    generate_summary()

