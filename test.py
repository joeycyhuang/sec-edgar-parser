import requests
import json
import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def call_api(
        company_cik: str,
        company_name: str,
        email: str
    ) -> None:

    folder = Path(f"data/{company_name}")
    folder.mkdir(parents=True, exist_ok=True)

    submission = f"https://data.sec.gov/submissions/CIK{company_cik}.json"
    companyFacts = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{company_cik}.json"
    header = {
        "User-Agent": email,
        "Accept-Encoding": "gzip, deflate",
        "Host": "data.sec.gov"
    }

    try:
        response = requests.get(companyFacts, headers = header)
        submission = requests.get(submission, headers = header)
        with open(folder / f"{company_name}.json", "w") as f:
            json.dump(json.loads(response.text), f, indent=4)
        with open(folder / f"{company_name}_submission.json", "w") as f:
            json.dump(json.loads(submission.text), f, indent=4)
    except Exception as e:
        print(e)
        print("Error occurred when calling the API.")


if __name__ == "__main__":
    company_cik = "0001318605"
    email = os.getenv("EMAIL")
    call_api(company_cik, "Tesla", email)