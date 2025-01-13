# backend/load_data.py

import json
import argparse
from database.db_utils import get_connection, init_db

def load_json_data(file_path):
    """
    Load JSON file, each record should contain { "textA": "...", "textB": "..." }
    Write to annotation_data table.
    """
    # 确保先初始化数据库
    init_db()

    conn = get_connection()
    cur = conn.cursor()

    with open(file_path, 'r', encoding='utf-8') as f:
        data_list = json.load(f)

    for item in data_list:
        textA = item["textA"]
        textB = item["textB"]

        cur.execute("""
            INSERT INTO annotation_data (textA, textB)
            VALUES (?, ?)
        """, (textA, textB))
    
    conn.commit()
    conn.close()

    print(f"Successfully loaded {len(data_list)} records into the database!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True, help='Path to JSON file')
    args = parser.parse_args()

    load_json_data(args.file)
