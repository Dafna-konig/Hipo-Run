import json
import os

SAVE_FILE = os.path.join(os.path.dirname(__file__), "highscore.json")


def load_save_data():
    """Load high score, max eggs, and unlocked mini IDs from file."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                high_score = int(data.get("high_score", 0))
                max_eggs = int(data.get("max_eggs", 0))
                unlocked_raw = data.get("unlocked_minis", [])
                unlocked_set = {int(x) for x in unlocked_raw if 1 <= int(x) <= 24}
                return high_score, max_eggs, unlocked_set
        except Exception:
            return 0, 0, set()
    return 0, 0, set()


def load_high_score():
    high_score, max_eggs, _ = load_save_data()
    return high_score, max_eggs


def save_high_score(score, eggs):
    try:
        current_high, current_eggs, unlocked_set = load_save_data()
        score_int = int(score)
        eggs_int = int(eggs)
        is_new_record = score_int > current_high
        new_high = max(current_high, score_int)
        new_eggs = max(current_eggs, eggs_int)

        data = {
            "high_score": new_high,
            "max_eggs": new_eggs,
            "unlocked_minis": sorted(list(unlocked_set))
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return new_high, is_new_record
    except Exception:
        return int(score), False


def get_unlocked_minis():
    _, _, unlocked = load_save_data()
    return unlocked


def unlock_minis(new_indices):
    """
    Given a list or set of 1-based mini IDs, save any newly unlocked ones.
    Returns (newly_unlocked_list, all_unlocked_set).
    """
    try:
        current_high, current_eggs, unlocked_set = load_save_data()
        newly_unlocked = []
        for idx in new_indices:
            idx = int(idx)
            if 1 <= idx <= 24 and idx not in unlocked_set:
                unlocked_set.add(idx)
                newly_unlocked.append(idx)

        data = {
            "high_score": current_high,
            "max_eggs": current_eggs,
            "unlocked_minis": sorted(list(unlocked_set))
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return newly_unlocked, unlocked_set
    except Exception:
        return [], set(new_indices)
