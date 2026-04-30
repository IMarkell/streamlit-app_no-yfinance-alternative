import streamlit as st
import pandas as pd

st.set_page_config(page_title="Risk Tolerance Assessment", page_icon="📊")

# Initialize session state for user responses
if "responses" not in st.session_state:
    st.session_state.responses = [""] * 10

# Function to display each question
def display_question(question, index):
    options = ["Very uncomfortable", "uncomfortable", "Neutral", "comfortable", "very comfortable"]
    current_selection_index = (
        options.index(st.session_state.responses[index])
        if st.session_state.responses[index]
        else 2
    )
    st.session_state.responses[index] = st.radio(
        question, options, index=current_selection_index, key=f"q_{index}"
    )

# ORIGINAL 5 QUESTIONS (unchanged)
original_questions = [
    "1. How would you feel if your investment portfolio lost 20% of value in a year?",
    "2. How comfortable are you with delaying financial rewards today in exchange for potentially greater rewards in the future?",
    "3. How comfortable are you with keeping an investment even when the market is experiencing volatility?",
    "4. How would you feel if you had a 50/50 chance of doubling your money or losing it all?",
    "5. How comfortable are you making financial decisions when the outcome is uncertain?"
]

# NEW 5 QUESTIONS (more variety)
new_questions = [
    "6. How comfortable are you with investing money that you may not need access to for several years?",
    "7. How comfortable are you with the idea that taking more risk could potentially increase your long‑term wealth?",
    "8. How comfortable are you relying on a diversified portfolio rather than choosing individual 'safe' investments?",
    "9. How comfortable are you making financial decisions without having complete information or certainty about the outcome?",
    "10. How comfortable are you adjusting your investment strategy when your financial goals or market conditions change?"
]

all_questions = original_questions + new_questions

# Score mapping
score_for_option = {
    "Very uncomfortable": 0,
    "uncomfortable": 1,
    "Neutral": 2,
    "comfortable": 3,
    "very comfortable": 4,
}

# Risk profiles
risk_profiles = {
    "Low": {
        "goal": "Preserve capital and achieve a modest return.",
        "allocation": "20% Stocks, 80% Bonds",
        "rationale": "Low-risk tolerance, focusing on capital preservation.",
        "summary": "Invest primarily in bonds and stable assets.",
        "recommended_investments": [
            {"ticker": "BND", "name": "Vanguard Total Bond Market ETF", "description": "Broad bond market exposure"},
            {"ticker": "AGG", "name": "iShares Core U.S. Aggregate Bond ETF", "description": "Investment-grade bonds"},
            {"ticker": "KO", "name": "Coca-Cola", "description": "Stable dividend stock"},
            {"ticker": "PG", "name": "Procter & Gamble", "description": "Low-volatility consumer staples"},
            {"ticker": "JNJ", "name": "Johnson & Johnson", "description": "Defensive healthcare stock"},
        ],
    },
    "Medium": {
        "goal": "Achieve balanced growth while managing risk.",
        "allocation": "50% Stocks, 50% Bonds",
        "rationale": "Moderate risk tolerance, seeks growth with some safety.",
        "summary": "Mix of stocks and bonds for balanced portfolio.",
        "recommended_investments": [
            {"ticker": "VOO", "name": "Vanguard S&P 500 ETF", "description": "Large-cap diversified exposure"},
            {"ticker": "VTI", "name": "Vanguard Total Stock Market ETF", "description": "Broad U.S. equity exposure"},
            {"ticker": "BND", "name": "Vanguard Total Bond Market ETF", "description": "Bond diversification"},
            {"ticker": "MSFT", "name": "Microsoft", "description": "Stable growth stock"},
            {"ticker": "AAPL", "name": "Apple", "description": "Large-cap growth stock"},
        ],
    },
    "High": {
        "goal": "Maximize growth potential and returns.",
        "allocation": "80% Stocks, 20% Bonds",
        "rationale": "High-risk tolerance, accepting volatility for higher returns.",
        "summary": "Aggressive approach with a focus on stock investments.",
        "recommended_investments": [
            {"ticker": "QQQ", "name": "Invesco QQQ Trust", "description": "Tech-heavy growth ETF"},
            {"ticker": "VUG", "name": "Vanguard Growth ETF", "description": "High-growth equities"},
            {"ticker": "TSLA", "name": "Tesla", "description": "High-volatility growth stock"},
            {"ticker": "NVDA", "name": "NVIDIA", "description": "AI and semiconductor leader"},
            {"ticker": "AMD", "name": "Advanced Micro Devices", "description": "High-growth semiconductor stock"},
        ],
    },
}

# UI
st.title("📊 10‑Question Risk Tolerance Assessment")
st.write("Please answer all questions using the scale below:")

for i, question in enumerate(all_questions):
    display_question(question, i)

# Calculate total score (0–40)
total_score = sum(score_for_option.get(r, 0) for r in st.session_state.responses)

# Determine risk profile
if total_score <= 13:
    profile = "Low"
elif total_score <= 26:
    profile = "Medium"
else:
    profile = "High"

st.markdown("---")
st.header("📈 Your Results")

col1, col2 = st.columns(2)
col1.metric("Risk Score", f"{total_score}/40")
col2.metric("Risk Profile", profile)

st.write(f"**Goal:** {risk_profiles[profile]['goal']}")
st.write(f"**Recommended Asset Allocation:** {risk_profiles[profile]['allocation']}")
st.write(f"**Rationale:** {risk_profiles[profile]['rationale']}")
st.write(f"**Summary:** {risk_profiles[profile]['summary']}")

st.subheader(f"💼 Example Investments for a {profile} Risk Profile")
st.table(pd.DataFrame(risk_profiles[profile]["recommended_investments"]))
