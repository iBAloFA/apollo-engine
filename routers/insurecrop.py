from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np

router = APIRouter(prefix="/api/v1/insurecrop", tags=["InsureCrop"])

class RiskPayload(BaseModel):
    crop_type: str
    historical_rainfall_mm: float
    soil_moisture_percentage: float
    insured_value_usd: float

@router.post("/assess-risk")
def assess_agricultural_risk(payload: RiskPayload):
    # Set ideal environmental baselines for software checks
    ideal_rainfall = 800.0  # mm per season
    
    # Calculate variation distance from ideal conditions using absolute values
    rainfall_deficit = abs(ideal_rainfall - payload.historical_rainfall_mm)
    
    # Formulaic risk calculation algorithm 
    # High variance or bone-dry soil increases the mathematical risk scale
    base_risk = (rainfall_deficit / ideal_rainfall) * 0.6
    soil_risk = (100 - payload.soil_moisture_percentage) / 100 * 0.4
    
    # Bound the risk factor between 5% and 95% safely using numpy clip
    calculated_risk_factor = np.clip(base_risk + soil_risk, 0.05, 0.95)
    
    # Calculate annual insurance premium based on risk weight
    insurance_premium = payload.insured_value_usd * calculated_risk_factor
    
    # Determine credit-eligibility status based on safety boundaries
    approved_for_loan = True if calculated_risk_factor < 0.65 else False
    
    return {
        "crop_evaluation": payload.crop_type,
        "risk_profile": {
            "calculated_risk_index": round(float(calculated_risk_factor), 2),
            "risk_tier": "HIGH" if calculated_risk_factor > 0.60 else "MODERATE" if calculated_risk_factor > 0.30 else "LOW"
        },
        "financial_underwriting": {
            "suggested_annual_premium_usd": round(float(insurance_premium), 2),
            "micro_credit_eligibility": approved_for_loan
        }
    }
