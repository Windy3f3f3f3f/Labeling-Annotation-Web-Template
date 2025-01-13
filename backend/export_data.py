# backend/export_data.py

import json
import argparse
from datetime import datetime
from database.db_utils import get_connection

def export_annotation_results(output_file=None):
    """
    Export annotation results from database to a JSON file.
    
    Args:
        output_file (str, optional): Path to output JSON file. 
            If not provided, will generate a filename with timestamp.
    
    Returns:
        str: Path to the exported file
    """
    # Generate default filename if not provided
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"annotation_results_{timestamp}.json"
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Query to join annotation_data with annotation_result
    query = """
    SELECT 
        d.id as data_id,
        d.textA,
        d.textB,
        r.username,
        r.score,
        r.timestamp
    FROM annotation_data d
    LEFT JOIN annotation_result r ON d.id = r.data_id
    ORDER BY d.id, r.timestamp
    """
    
    cur.execute(query)
    rows = cur.fetchall()
    
    # Process the results
    results = {}
    for row in rows:
        data_id = row['data_id']
        if data_id not in results:
            results[data_id] = {
                'data_id': data_id,
                'textA': row['textA'],
                'textB': row['textB'],
                'annotations': []
            }
        
        # Only add annotation if it exists (handle NULL case from LEFT JOIN)
        if row['username']:
            results[data_id]['annotations'].append({
                'username': row['username'],
                'score': row['score'],
                'timestamp': row['timestamp']
            })
    
    # Convert to list for final JSON
    final_results = list(results.values())
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    
    conn.close()
    
    print(f"Successfully exported {len(final_results)} records to {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Export annotation results to JSON')
    parser.add_argument('--output', '-o', type=str, help='Output JSON file path')
    args = parser.parse_args()
    
    export_annotation_results(args.output)

if __name__ == "__main__":
    main() 
