import streamlit as st
import pandas as pd

st.set_page_config(page_title="Risk Tolerance Assessment", layout="wide")

# ---------------------- SIMPLE BLACK & WHITE CSS ----------------------
st.markdown("""
<style>

    body {
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
    }

    .content-box {
        background-color: #FFFFFF;
        color: #000000;
        padding: 25px;
        border-radius: 6px;
        border: 1px solid #000000;
        margin-bottom: 25px;
    }

    .content-box * {
        color: #000000 !important;
        font-size: 16px;
    }

    h1, h2, h3, h4 {
        color: #000000 !important;
        font-weight: 600;
    }

    .stRadio label, .stRadio div, .stRadio p {
        color: #000000 !important;
        font-size: 16px !important;
    }

    table, th, td {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        border-color: #000000 !important;
    }

    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #000000 !important;
        font-weight: 700 !important;
    }

</style>
""", unsafe_allow_html=True)

# ---------------------- SESSION STATE ----------------------
if "responses" not in st.session_state:
    st.session_state.responses = [""] * 10

# ---------------------- QUESTION DISPLAY FUNCTION ----------------------
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

# ---------------------- QUESTIONS ----------------------
original_questions = [
    "1. How would you feel if your investment portfolio lost 20% of value in a year?",
    "2. How comfortable are you with delaying financial rewards today in exchange for potentially greater rewards in the future?",
    "3. How comfortable are you with keeping an investment even when the market is experiencing volatility?",
    "4. How would you feel if you had a 50/50 chance of doubling your money or losing it all?",
    "5. How comfortable are you making financial decisions when the outcome is uncertain?"
]

new_questions = [
    "6. How comfortable are you with investing money that you may not need access to for several years?",
    "7. How comfortable are you with the idea that taking more risk could potentially increase your long‑term wealth?",
    "8. How comfortable are you relying on a diversified portfolio rather than choosing individual 'safe' investments?",
    "9. How comfortable are you making financial decisions without having complete information or certainty about the outcome?",
    "10. How comfortable are you adjusting your investment strategy when your financial goals or market conditions change?"
]

all_questions = original_questions + new_questions

# ---------------------- SCORING ----------------------
score_for_option = {
    "Very uncomfortable": 0,
    "uncomfortable": 1,
    "Neutral": 2,
    "comfortable": 3,
    "very comfortable": 4,
}

# ---------------------- RISK PROFILES ----------------------
risk_profiles = {
    "Low": {
        "goal": "Preserve capital and achieve a modest return.",
        "allocation": "20% Stocks, 80% Bonds",
        "rationale": "Low-risk tolerance, focusing on capital preservation.",
        "summary": "Invest primarily in bonds and stable assets.",
        "persona": "Prefers stability and predictability. Dislikes volatility and values peace of mind over maximizing returns.",
        "recommended_investments": [
            {"ticker": "BND", "name": "Vanguard Total Bond Market ETF", "description": "Broad bond exposure"},
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
        "persona": "Comfortable with some ups and downs. Wants growth but also values balance and diversification.",
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
        "persona": "Focused on long‑term growth and willing to tolerate volatility. Understands that markets move in cycles.",
        "recommended_investments": [
            {"ticker": "QQQ", "name": "Invesco QQQ Trust", "description": "Tech-heavy growth ETF"},
            {"ticker": "VUG", "name": "Vanguard Growth ETF", "description": "High-growth equities"},
            {"ticker": "TSLA", "name": "Tesla", "description": "High-volatility growth stock"},
            {"ticker": "NVDA", "name": "NVIDIA", "description": "AI and semiconductor leader"},
            {"ticker": "AMD", "name": "Advanced Micro Devices", "description": "High-growth semiconductor stock"},
        ],
    },
}

# ---------------------- UI ----------------------
st.title("Risk Tolerance Assessment")

# Questionnaire Header
st.markdown("<div class='content-box'>", unsafe_allow_html=True)
st.subheader("Questionnaire")
st.write("Please answer all questions using the scale below:")
st.markdown("</div>", unsafe_allow_html=True)

# Display Questions
for i, question in enumerate(all_questions):
    st.markdown("<div class='content-box'>", unsafe_allow_html=True)
    display_question(question, i)
    st.markdown("</div>", unsafe_allow_html=True)

# Score calculation
total_score = sum(score_for_option.get(r, 0) for r in st.session_state.responses)

# Determine risk profile
if total_score <= 13:
    profile = "Low"
elif total_score <= 26:
    profile = "Medium"
else:
    profile = "High"

# ---------------------- RESULTS ----------------------
st.markdown("<div class='content-box'>", unsafe_allow_html=True)
st.subheader("Your Results")

col1, col2 = st.columns(2)
col1.metric("Risk Score", f"{total_score}/40")
col2.metric("Risk Profile", profile)

st.write(f"**Goal:** {risk_profiles[profile]['goal']}")
st.write(f"**Recommended Asset Allocation:** {risk_profiles[profile]['allocation']}")
st.write(f"**Rationale:** {risk_profiles[profile]['rationale']}")
st.write(f"**Summary:** {risk_profiles[profile]['summary']}")
st.write(f"**Persona:** {risk_profiles[profile]['persona']}")
st.markdown("</div>", unsafe_allow_html=True)

# Recommended Investments
st.markdown("<div class='content-box'>", unsafe_allow_html=True)
st.subheader(f"Example Investments for a {profile} Risk Profile")
st.table(pd.DataFrame(risk_profiles[profile]["recommended_investments"]))
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- HISTORICAL CONTEXT ----------------------
st.markdown("<div class='content-box'>", unsafe_allow_html=True)
st.subheader("Historical Market Context")
st.write("""
**Conservative Portfolios (20% stocks / 80% bonds):** Historically experience smaller drawdowns and lower volatility, often returning 3–5% annually over long periods.

**Balanced Portfolios (50% stocks / 50% bonds):** Historically return around 5–7% annually with moderate volatility, benefiting from diversification.

**Aggressive Portfolios (80% stocks / 20% bonds):** Historically return 7–10% annually over long horizons but experience larger short‑term swings.
""")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- COMPARE ALL PROFILES ----------------------
st.markdown("<div class='content-box'>", unsafe_allow_html=True)
st.subheader("Compare All Risk Profiles")

comparison_df = pd.DataFrame({
    "Risk Level": ["Low", "Medium", "High"],
    "Allocation": ["20% Stocks / 80% Bonds", "50% Stocks / 50% Bonds", "80% Stocks / 20% Bonds"],
    "Typical Volatility Range": ["5–8%", "10–12%", "15–20%"],
    "Strengths": [
        "High stability, smaller drawdowns",
        "Balanced growth and stability",
        "Higher long‑term growth potential"
    ],
    "Trade‑offs": [
        "Lower long‑term returns",
        "Moderate drawdowns",
        "Larger short‑term losses"
    ]
})

st.table(comparison_df)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- INTERACTIVE RISK SLIDER ----------------------
st.markdown("<div class='content-box'>", unsafe_allow_html=True)
st.subheader("Explore Other Risk Profiles")

st.write("Use the slider below to explore how portfolio recommendations change across different risk levels.")

risk_level_map = {0: "Low", 1: "Medium", 2: "High"}

selected_risk_index = st.slider(
    "Adjust Risk Level",
    min_value=0,
    max_value=2,
    value=0 if profile == "Low" else (1 if profile == "Medium" else 2),
    format="%d",
    label_visibility="collapsed"
)

selected_risk_profile = risk_level_map[selected_risk_index]

st.write(f"### Portfolio Suggestions for {selected_risk_profile} Risk Level")
st.write(f"**Goal:** {risk_profiles[selected_risk_profile]['goal']}")
st.write(f"**Recommended Asset Allocation:** {risk_profiles[selected_risk_profile]['allocation']}")
st.write(f"**Rationale:** {risk_profiles[selected_risk_profile]['rationale']}")
st.write(f"**Summary:** {risk_profiles[selected_risk_profile]['summary']}")
st.write(f"**Persona:** {risk_profiles[selected_risk_profile]['persona']}")

st.table(pd.DataFrame(risk_profiles[selected_risk_profile]["recommended_investments"]))
st.markdown("</div>", unsafe_allow_html=True)
