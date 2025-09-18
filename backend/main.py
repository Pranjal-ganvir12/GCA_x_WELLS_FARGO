from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import date, timedelta
import pandas as pd
import random

app = FastAPI(title="Wells Fargo Emergency Cushion API with Data")


df = pd.read_csv("/Users/pranjalganvir/Documents/GitHub/GCA_x_WELLS_FARGO/backend/data/unexpected_expenses.csv")
latest = df.iloc[-1]  # most recent year

# ----------------------
# Data Models
# ----------------------
class ApplyRequest(BaseModel):
    offer_id: int
    plan: str

class DisburseRequest(BaseModel):
    loan_id: int

# Mock loan offers
offers = [
    {"id": 1, "amount": 150, "fee": 9, "total": 159, "plan": "3 weekly payments"},
    {"id": 2, "amount": 300, "fee": 18, "total": 318, "plan": "6 weekly payments"},
    {"id": 3, "amount": 600, "fee": 30, "total": 630, "plan": "income-linked"},
]

# ----------------------
# Endpoints
# ----------------------

@app.get("/precheck")
def precheck(age_group: str = Query("All adults")):
    """
    Eligibility check using dataset.
    Example: /precheck?age_group=30-44
    """
    if age_group not in df.columns:
        return {
            "error": f"Invalid age_group. Must be one of: {list(df.columns[1:])}"
        }

    prob = latest[age_group]
    eligible = random.random() < (prob / 100.0)
    return {
        "year": latest["Year"],
        "group": age_group,
        "probability_percent": prob,
        "eligible": eligible,
        "message": f"{prob}% of {age_group} could cover a $400 expense in {latest['Year']}"
    }

@app.get("/offers")
def get_offers():
    """
    Return available loan offers
    """
    return {"offers": offers}

@app.post("/apply")
def apply(req: ApplyRequest):
    """
    Apply for a loan offer
    """
    return {
        "approved": True,
        "loan_id": 1001,
        "offer_id": req.offer_id,
        "plan": req.plan,
        "message": "Application approved instantly"
    }

@app.post("/disburse")
def disburse(req: DisburseRequest):
    """
    Simulate instant disbursement
    """
    return {
        "status": "funded",
        "loan_id": req.loan_id,
        "card": {"last4": "5678", "network": "Visa"},
        "eta": "instant"
    }

@app.get("/repayments/{loan_id}")
def repayment_plan(loan_id: int):
    """
    Generate a simple repayment schedule
    """
    today = date.today()
    schedule = [
        {"date": str(today + timedelta(days=7 * i)), "amount": 106, "status": "upcoming"}
        for i in range(1, 4)
    ]
    return {"loan_id": loan_id, "schedule": schedule}

@app.post("/repayments/{loan_id}/grace")
def grace_request(loan_id: int):
    """
    Request a 1-week grace period
    """
    new_due_date = date.today() + timedelta(days=7)
    return {
        "loan_id": loan_id,
        "grace_granted": True,
        "new_due_date": str(new_due_date),
    }
