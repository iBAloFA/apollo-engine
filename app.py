import streamlit as st
import requests
import random

st.set_page_config(page_title="The Apollo Engine Dashboard", page_icon="🚀", layout="wide")

st.title("🚀 The Apollo Engine Control Center")
st.markdown("Interactive multi-sector FinTech, HealthTech, and Engineering optimization portal.")

# Switch this URL to your live Render backend URL once deployed!
API_BASE_URL = "https://apollo-engine-backend.onrender.com"

# Create structural tabs for clean user navigation
tab1, tab2, tab3 = st.tabs(["🏥 MediPay (HealthTech)", "⚡ WattWise (Energy)", "🌾 InsureCrop (AgriTech)"])

# ----------------- TAB 1: MEDIPAY -----------------
with tab1:
    st.header("Medical Bill Financing & Insurance Predictor")
    col1, col2 = st.columns(2)
    
    with col1:
        bill_amt = st.number_input("Total Medical Bill ($)", min_value=100.0, value=5000.0, key="mp_bill")
        provider = st.selectbox("Insurance Provider", ["Premium_Care", "Standard_Health", "Axa_Mansard", "Reliance_HMO"], key="mp_provider")
        credit_tier = st.selectbox("Patient Risk Profile", ["HIGH", "MEDIUM", "LOW"], key="mp_tier")
        
        if st.button("Analyze Medical Bill", key="mp_btn"):
            payload = {"total_bill": bill_amt, "insurance_provider": provider, "patient_credit_category": credit_tier}
            try:
                response = requests.post(f"{API_BASE_URL}/api/v1/medipay/analyze", json=payload)
                if response.status_code == 200:
                    st.session_state['medipay_res'] = response.json()
                    st.session_state['medipay_error'] = None
                else:
                    st.session_state['medipay_error'] = f"Backend Error Code {response.status_code}: {response.text}"
                    if 'medipay_res' in st.session_state: del st.session_state['medipay_res']
            except Exception as e:
                st.error(f"Cannot connect to backend server: {e}")

    with col2:
        if st.session_state.get('medipay_error'):
            st.error(st.session_state['medipay_error'])
        elif 'medipay_res' in st.session_state:
            res = st.session_state['medipay_res']
            denial_prob = res.get('insurance_denial_probability', 0)
            st.metric("Claim Denial Probability", f"{int(denial_prob * 100)}%")
            
            st.subheader("Financing Options Available:")
            financing = res.get('financing_options', {})
            st.write(f"**Interest Applied:** {financing.get('interest_applied', 'N/A')}")
            st.write(f"**Total Payback Cost:** ${financing.get('total_repayment', '0.00')}")
            st.success(f"**3-Month Installment Plan:** ${financing.get('three_month_split_monthly', '0.00')} / month")

# ----------------- TAB 2: WATTWISE -----------------
with tab2:
    st.header("Industrial Energy Infrastructure Optimization")
    if st.button("Simulate Business Energy Stream & Optimize", key="ww_btn"):
        hourly_data = []
        for h in range(24):
            kwh = random.uniform(80, 150) if 9 <= h <= 17 else random.uniform(20, 50)
            tariff = 0.28 if 9 <= h <= 17 else 0.10
            hourly_data.append({"hour": h, "kwh_used": round(kwh, 2), "grid_tariff_rate": tariff})
            
        payload = {"business_type": "Cold Storage Facility", "hourly_data": hourly_data}
        try:
            response = requests.post(f"{API_BASE_URL}/api/v1/wattwise/optimize", json=payload)
            if response.status_code == 200:
                res = response.json()
                
                # Render Core Financial Metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Baseline Grid Cost", f"${res['metrics']['total_baseline_cost_usd']}")
                c2.metric("Optimized Storage Cost", f"${res['metrics']['total_optimized_cost_usd']}")
                c3.metric("Net Financial Savings", f"${res['metrics']['projected_savings_usd']}", delta=f"${res['metrics']['projected_savings_usd']}")
                
                st.info(f"💡 **Strategic Advisory:** {res['recommendation']}")
                
                # --- VISUALIZATION LAYER ADDED HERE ---
                st.subheader("📊 24-Hour Optimization Trajectory")
                import pandas as pd
                
                # Structure incoming dictionary array back into a pandas format for graphing
                chart_df = pd.DataFrame(res['hourly_breakdown'])
                chart_df = chart_df.set_index('hour')
                
                # Rename the column handles to look ultra clean on graph labels
                chart_df.columns = ['Standard Grid Cost ($)', 'WattWise Optimized Cost ($)']
                
                # Render the high-performance native chart UI layout component
                st.line_chart(chart_df, color=["#FF4B4B", "#00F0A0"]) 
                
            else:
                st.error(f"Backend Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Connection Failed: {e}")


# ----------------- TAB 3: INSURECROP -----------------
with tab3:
    st.header("Agricultural Telemetry Risk & Micro-Credit Underwriting")
    col1_crop, col2_crop = st.columns(2)
    
    with col1_crop:
        crop = st.selectbox("Crop Category", ["Maize", "Rice", "Cassava", "Cocoa"], key="ic_crop")
        rainfall = st.slider("Seasonal Historical Rainfall (mm)", 100, 2000, 650, key="ic_rain")
        moisture = st.slider("Current Soil Hydration/Moisture Percentage", 0, 100, 35, key="ic_moist")
        valuation = st.number_input("Total Insured Crop Asset Valuation ($)", min_value=1000, value=25000, key="ic_val")
        
        if st.button("Execute Financial Underwriting", key="ic_btn"):
            payload = {"crop_type": crop, "historical_rainfall_mm": rainfall, "soil_moisture_percentage": moisture, "insured_value_usd": valuation}
            try:
                response = requests.post(f"{API_BASE_URL}/api/v1/insurecrop/assess-risk", json=payload)
                if response.status_code == 200:
                    st.session_state['crop_res'] = response.json()
                    st.session_state['crop_error'] = None
                else:
                    st.session_state['crop_error'] = f"Backend Error Code {response.status_code}: {response.text}"
                    if 'crop_res' in st.session_state: del st.session_state['crop_res']
            except Exception as e:
                st.error(f"Connection Failed: {e}")

    with col2_crop:
        if st.session_state.get('crop_error'):
            st.error(st.session_state['crop_error'])
        elif 'crop_res' in st.session_state:
            res = st.session_state['crop_res']
            risk_profile = res.get('risk_profile', {})
            risk_tier = risk_profile.get('risk_tier', 'UNKNOWN')
            risk_index = risk_profile.get('calculated_risk_index', 0.0)
            
            if risk_tier == "HIGH": st.error(f"Risk Index Tier: {risk_tier} ({risk_index})")
            elif risk_tier == "MODERATE": st.warning(f"Risk Index Tier: {risk_tier} ({risk_index})")
            else: st.success(f"Risk Index Tier: {risk_tier} ({risk_index})")
            
            underwriting = res.get('financial_underwriting', {})
            st.metric("Suggested Policy Annual Premium", f"${underwriting.get('suggested_annual_premium_usd', '0.00')}")
            
            loan_status = "APPROVED" if underwriting.get('micro_credit_eligibility') else "REJECTED (Risk Profile Bounds Breached)"
            st.write(f"**Micro-Credit Status:** `{loan_status}`")
