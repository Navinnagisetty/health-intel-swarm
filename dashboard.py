import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv

# --- 1. LOAD SECRETS ---
load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    st.error("🚨 API Key missing! Please create a .env file with GOOGLE_API_KEY=your_key")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="HealthIntel Pro", layout="wide", page_icon="🏥")
st.title("🏥 HealthIntel: Analytics Swarm")

# --- 3. LOAD DATA ---
import pathlib
BASE_DIR = pathlib.Path(__file__).parent
data_file = BASE_DIR / 'data' / 'enriched_providers.csv'

if data_file.exists():
    df = pd.read_csv(data_file)
else:
    df = pd.DataFrame()

# --- 4. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive", "🕵️‍♂️ Fraud Hunter", "🤖 AI Analyst", "💰 ROI Strategy"])

# TAB 1: EXECUTIVE
with tab1:
    st.header("Financial Performance")
    if not df.empty:
        max_rev = int(df['Total_Revenue'].max())
        min_rev = st.sidebar.slider("Revenue Filter ($)", 0, max_rev, 0, 10000)
        filtered = df[df['Total_Revenue'] > min_rev]
        st.dataframe(filtered, height=300)
    else:
        st.warning("Run detect_anomalies.py first.")

# TAB 2: FRAUD HUNTER
with tab2:
    st.header("Anomaly Detection")
    if not df.empty:
        suspicious = df[df['Z_Score'] > 3].sort_values(by='Z_Score', ascending=False)
        st.error(f"🚨 {len(suspicious)} High Risk Providers")
        st.dataframe(suspicious[['State_Full', 'Z_Score', 'Total_Revenue']])

# TAB 3: AI ANALYST (Lightweight Version)
with tab3:
    st.header("Chat with Data")
    q = st.text_input("Ask a question (e.g., 'Who is the top biller in California?'):")

    if q and st.button("🚀 Ask AI"):
        with st.spinner('Thinking...'):
            try:
                llm = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0)
                agent = create_pandas_dataframe_agent(
                    llm,
                    df,
                    verbose=True,
                    allow_dangerous_code=True,
                    handle_parsing_errors=True
                )
                response = agent.invoke({"input": q})
                st.write(response['output'])
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ Speed Limit Hit (Free Tier). Please wait 1 minute and try again.")
                else:
                    st.error(f"Error: {e}")

# TAB 4: ROI STRATEGY
with tab4:
    st.header("📈 Profit Optimization Model")
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            audit_cost = st.slider("Cost per Audit ($)", 0, 5000, 1000)
        with col2:
            recovery_rate = st.slider("Recovery Rate (%)", 0, 100, 20) / 100
        
        strat_df = df.sort_values(by='Z_Score', ascending=False).reset_index(drop=True)
        strat_df['Net_Profit'] = (strat_df['Total_Revenue'] * recovery_rate) - audit_cost
        strat_df['Cumulative_Profit'] = strat_df['Net_Profit'].cumsum()
        
        peak_idx = strat_df['Cumulative_Profit'].idxmax()
        peak_val = strat_df['Cumulative_Profit'].max()
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(strat_df.index, strat_df['Cumulative_Profit'], color='green', label='Profit Curve')
        ax.axvline(peak_idx, color='red', linestyle='--', label='Stop Auditing Here')
        ax.scatter(peak_idx, peak_val, color='red', s=100)
        ax.set_title(f"Max Profit: ${peak_val:,.0f} (Audit Top {peak_idx} Providers)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        st.pyplot(fig)
        st.success(f"Strategy: Stop auditing after the top {peak_idx} riskiest providers.")
# --- Download Section ---
    st.sidebar.markdown("---")
    csv_data = df.to_csv(index=False).encode('utf-8')
    
    st.sidebar.download_button(
        label="📥 Download Full Report",
        data=csv_data,
        file_name='health_intel_report.csv',
        mime='text/csv',
        help="Click to download the analyzed data as a CSV file."
    )