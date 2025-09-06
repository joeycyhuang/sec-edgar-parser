from fastapi import FastAPI
from fastapi.responses import JSONResponse

import json

app = FastAPI()

@app.get("/company/submission_history/{company_name}")
async def company_submission_history(company_name: str):
    company_name = company_name.strip().lower()
    with open(f"data/{company_name}/{company_name}_submission.json", "r") as f:
        data = json.load(f)
    return JSONResponse(content=data)