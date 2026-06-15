import requests
import random
import time

# Change this URL to your production URL later once deployed!
BASE_URL = "http://127.0.0"

def seed_medipay():
    print("🚀 Seeding MediPay Module...")
    providers = ["Premium_Care", "Standard_Health", "Axa_Mansard", "Reliance_HMO"]
    tiers = ["HIGH", "MEDIUM", "LOW"]
    
    payload = {
        "total_bill": round(random.uniform(500, 25000), 2),
        "insurance_provider": random.choice(providers),
        "patient_credit_category": random.choice(tiers)
    }
    
    response = requests.post(f"{BASE_URL}/medipay/analyze", json=payload)
    print(f"Status Code: {response.status_code} | Result: {response.json()}\n")

def seed_wattwise():
    print("⚡ Seeding WattWise Module...")
    # Simulate a full 24-hour cycle of business energy metrics
    hourly_metrics = []
    for hour in range(24):
        # Generate peak use during business hours (9 AM to 5 PM)
        if 9 <= hour <= 17:
            kwh = random.uniform(80.0, 150.0)
            tariff = 0.28  # Expensive peak rates
        else:
            kwh = random.uniform(20.0, 50.0)
            tariff = 0.10  # Cheap off-peak rates
            
        hourly_metrics.append({"hour": hour, "kwh_used": round(kwh, 2), "grid_tariff_rate": tariff})
        
    payload = {
        "business_type": random.choice(["Manufacturing", "Data Center", "Cold Storage Warehouse"]),
        "hourly_data": hourly_metrics
    }
    
    response = requests.post(f"{BASE_URL}/wattwise/optimize", json=payload)
    print(f"Status Code: {response.status_code} | Result: {response.json()}\n")

def seed_insurecrop():
    print("🌾 Seeding InsureCrop Module...")
    crops = ["Maize", "Rice", "Cassava", "Cocoa"]
    
    payload = {
        "crop_type": random.choice(crops),
        "historical_rainfall_mm": round(random.uniform(200.0, 1400.0), 2),
        "soil_moisture_percentage": round(random.uniform(15.0, 85.0), 2),
        "insured_value_usd": round(random.uniform(5000, 75000), 2)
    }
    
    response = requests.post(f"{BASE_URL}/insurecrop/assess-risk", json=payload)
    print(f"Status Code: {response.status_code} | Result: {response.json()}\n")

if __name__ == "__main__":
    print("--- Starting The Apollo Engine Local Seeder ---\n")
    # Make sure your server (uvicorn main:app) is running in another terminal window first!
    try:
        seed_medipay()
        time.sleep(1)
        seed_wattwise()
        time.sleep(1)
        seed_insurecrop()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API. Make sure your server is running via 'uvicorn main:app --reload'")
