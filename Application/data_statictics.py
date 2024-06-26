from typing import List, Dict, Tuple


# Count users
def count_unique_users(data: List[Dict]) -> int:
    unique_users = {entry['userid'] for entry in data if 'userid' in entry}
    return len(unique_users)

# Count bets
def count_bets(data: List[Dict]) -> int:
    total_bets = 0
    for entry in data:
        if 'bet' in entry and isinstance(entry['bet'], list):
            total_bets += len(entry['bet'])
    return total_bets

# Get date range of a dataset
def get_date_range(data: List[Dict]) -> Tuple[str, str]:
    dates = [entry['time'] for entry in data if 'time' in entry]
    if not dates:
        return None, None
    min_date = {"From": min(dates)}
    max_date = {"To": max(dates)}
    return min_date, max_date
