import json
from pathlib import Path

RULES_PATH = Path("data/category_rules.json")


def load_rules():
    if not RULES_PATH.exists():
        return []
    return json.loads(RULES_PATH.read_text())


def apply_category_rules(transaction):
    rules = load_rules()

    for rule in rules:
        field_value = transaction.get(rule["field"], "") or ""

        if any(keyword.lower() in field_value.lower() for keyword in rule["match"]):
            if "amount_lt" in rule:
                if abs(transaction["amount"]) >= rule["amount_lt"]:
                    continue

            return rule["category"]

    return None