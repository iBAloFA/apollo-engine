from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import numpy as np

router = APIRouter(prefix="/wattwise", tags=["WattWise"])

class HourlyConsumption(BaseModel):
    hour: int  # 0 to 23
    kwh_used: float
    grid_tariff_rate: float # Cost per kWh from national grid

class EnergyPayload(BaseModel):
    business_type: str
    hourly_data: List[HourlyConsumption]

@router.post("/optimize")
def optimize_energy_costs(payload: EnergyPayload):
    if not payload.hourly_data:
        raise HTTPException(status_code=400, detail="Hourly data list cannot be empty")
        
    # Convert incoming Pydantic payload seamlessly into a Pandas DataFrame
    data_dict = [item.model_dump() for item in payload.hourly_data]
    df = pd.DataFrame(data_dict)
    
    # Calculate current baseline costs
    df['baseline_cost'] = df['kwh_used'] * df['grid_tariff_rate']
    total_baseline_cost = df['baseline_cost'].sum()
    
    # Algorithm: Identify peak hours where grid rates are high
    # Suggest switching to alternative power (solar/generator at fixed rate of 0.15)
    alternative_rate = 0.15 
    
    df['optimized_cost'] = np.where(
        df['grid_tariff_rate'] > alternative_rate,
        df['kwh_used'] * alternative_rate,
        df['baseline_cost']
    )
    
    total_optimized_cost = df['optimized_cost'].sum()
    savings = total_baseline_cost - total_optimized_cost
    
    # Identify the absolute peak hour of stress on the system
    peak_hour = int(df.loc[df['kwh_used'].idxmax()]['hour'])
    hourly_breakdown = df[['hour', 'baseline_cost', 'optimized_cost']].to_dict(orient='records')
    
    return {
        "business_profile": payload.business_type,
        "metrics": {
            "total_baseline_cost_usd": round(float(total_baseline_cost), 2),
            "total_optimized_cost_usd": round(float(total_optimized_cost), 2),
            "projected_savings_usd": round(float(savings), 2),
            "critical_peak_hour": peak_hour
        },
        "hourly_breakdown": hourly_breakdown,
        "recommendation": f"Switch to solar storage infrastructure specifically during hour {peak_hour} to maximize margins."
    }
