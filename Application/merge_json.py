# Import necessary modules
from typing import List, Dict
import json

# Helping function to identify unique bets
def merge_bets(existing_bets: List[Dict], new_bets: List[Dict]) -> List[Dict]:
    # Create a set of unique bets
    unique_bets = {json.dumps(bet, sort_keys=True): bet for bet in existing_bets}
    for bet in new_bets:
        bet_key = json.dumps(bet, sort_keys=True)
        if bet_key not in unique_bets:
            unique_bets[bet_key] = bet
    return list(unique_bets.values())

# Merge old and new datasets
def merge_json_data(existing_data: List[Dict], new_data: List[Dict], output_json_path: str) -> List[Dict]:
    # Combine existing and new data
    combined_data = existing_data + new_data
    # Ensure unique entries by using a set of unique keys, allowing for missing 'match_id'
    unique_entries = {}
    for entry in combined_data:
        key = (entry['userid'], entry['time'])
        if 'match_id' in entry:
            key += (entry['match_id'],)
        # Preserve the nested structure of each entry
        if key not in unique_entries:
            unique_entries[key] = entry
        else:
            # Merge bets if the entry already exists
            existing_bets = unique_entries[key].get('bet', [])
            new_bets = entry.get('bet', [])
            unique_entries[key]['bet'] = merge_bets(existing_bets, new_bets)
    # Convert back to a list
    merged_data = list(unique_entries.values())
    # Save the merged data to JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(merged_data, json_file, ensure_ascii=False, indent=2)
    return merged_data