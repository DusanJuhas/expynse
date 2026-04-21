import re
import pdfplumber

DATE_RE = re.compile(r"^\d{1,2}\.\d{1,2}\.\d{4}")
AMOUNT_RE = re.compile(r"(-?\d{1,3}(?: \d{3})*\.\d{2})\s*CZK")

def clean_amount(value: str) -> float:
    return float(value.replace(" ", ""))

def extract_lines(pdf_path):
    i = 0
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.split("\n"):
                i = i + 1
                line = line.strip()
                print(f"{i} {line}")
                if line:
                    lines.append(line)
    return lines

def parse_transactions(pdf_path):
    lines = extract_lines(pdf_path)
    transactions = []
    current = None

    for line in lines:
        if DATE_RE.match(line):
            if current:
                transactions.append(current)

            current = {
                "date": None,
                "amount": None,
                "currency": "CZK",
                "bank_category": None,
                "transaction_type": None,
                "counter_account": None,
                "counter_name": None,
                "transaction_code": None,
                "description": ""
            }

            parts = line.split()
            current["date"] = parts[0]

            if len(parts) > 2:
                current["bank_category"] = parts[1]
                current["transaction_type"] = parts[2]

        if current:
            m = AMOUNT_RE.search(line)
            if m and current["amount"] is None:
                current["amount"] = clean_amount(m.group(1))
                continue

            if line.isdigit():
                current["transaction_code"] = line
            elif "a.s." in line or "s.r.o." in line or "BC." in line:
                current["counter_name"] = line
            else:
                if len(line) > 5:
                    current["description"] += line + " "

    if current:
        transactions.append(current)

    return transactions
