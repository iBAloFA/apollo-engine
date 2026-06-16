from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np

router = APIRouter(prefix="/medipay", tags=["MediPay"])

class BillPayload(BaseModel):
    total_bill: float
    insurance_provider: str
    patient_credit_category: str  # "HIGH", "MEDIUM", "LOW"

@router.post("/analyze")
def analyze_medical_bill(payload: BillPayload):
    if payload.total_bill <= 0:
        raise HTTPException(status_code=400, detail="Bill amount must be greater than 0")
        
    # Simulated logical algorithm for insurance denial probability
    denial_risk = 0.15 if payload.insurance_provider.lower() == "premium_care" else 0.42
    
    # Financial calculation: 3-month split options using numpy
    interest_rate = 0.05 if payload.patient_credit_category == "HIGH" else 0.12
    total_repayment = payload.total_bill * (1 + interest_rate)
    monthly_installment = total_repayment / 3
    
    return {
        "insurance_denial_probability": round(denial_risk, 2),
        "financing_options": {
            "interest_applied": f"{interest_rate * 100}%",
            "total_repayment": round(total_repayment, 2),
            "three_month_split_monthly": round(monthly_installment, 2)
        }
    }
