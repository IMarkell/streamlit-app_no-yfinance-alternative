import streamlit as st
import pandas as pd

# Initialize session state for user responses
if 'responses' not in st.session_state:
    st.session_state.responses = ['', '', '', '', '']

# Function to display each question and get user response
def display_question(question, index):
    options = ['Very uncomfortable', 'uncomfortable', 'Neutral', 'comfortable', 'very comfortable']
    current_selection_index = options.index(st.session_state.responses[index]) if st.session_state.responses[index] else 2
    st.session_state.responses[index] = st.radio(question, options, index=current_selection_index)

# List of assessment questions
questions = [
    "1. How would you feel if your investment portfolio lost 20% of value in a year?",
    "2. How comfortable are you with delaying financial rewards today in exchange for potentially greater rewards in the future?",
    "3. How comfortable are you with keeping an investment even when the market is experiencing volatility?",
    "4. How would you feel if you had a 50/50 chance of doubling your money or losing it all?",
    "5. How comfortable are you making financial decisions when the outcome is uncertain?"
]

# Risk profiles
risk_profiles = {
    'Low': {
        'goal': 'Preserve capital and achieve a modest return.',
        'allocation': '20% Stocks, 80% Bonds',
        'rationale': 'Low-risk tolerance, focusing on capital preservation.',
        'summary': 'Invest primarily in bonds and stable assets.',
        'stock_criteria': {
            'volatility_threshold': 0.01,
            'avg_return_threshold': 0.0005,
            'min_price_change_percent': 2
        },
        'recommended_investments': [
            {'ticker': 'BND', 'name': 'Vanguard Total Bond Market ETF', 'description': 'Broad bond market exposure for stability'},
            {'ticker': 'AGG', 'name': 'iShares Core U.S. Aggregate Bond ETF', 'description': 'Investment-grade bonds with low volatility'},
            {'ticker': 'KO', 'name': 'Coca-Cola', 'description': 'Dividend-paying defensive stock'},
            {'ticker': 'PG', 'name': 'Procter & Gamble', 'description': 'Stable consumer staples with consistent dividends'},
            {'ticker': 'JNJ', 'name': 'Johnson & Johnson', 'description': 'Healthcare leader with strong dividend history'},
        ]
    },
    'Medium': {
        'goal': 'Achieve balanced growth while managing risk.',
        'allocation': '50% Stocks, 50% Bonds',
        'rationale': 'Moderate risk tolerance, seeks growth with some safety.',
        'summary': 'Mix of stocks and bonds for balanced portfolio.',
        'stock_criteria': {
            'volatility_threshold': 0.02,
            'avg_return_threshold': 0.001,
            'min_price_change_percent': 5
        },
        'recommended_investments': [
            {'ticker': 'VOO', 'name': 'Vanguard S&P 500 ETF', 'description': 'Diversified large-cap stock exposure'},
            {'ticker': 'VTI', 'name': 'Vanguard Total Stock Market ETF', 'description': 'Complete U.S. stock market coverage'},
            {'ticker': 'BND', 'name': 'Vanguard Total Bond Market ETF', 'description': 'Balanced bond allocation'},
            {'ticker': 'MSFT', 'name': 'Microsoft', 'description': 'Tech leader with strong fundamentals'},
            {'ticker': 'AAPL', 'name': 'Apple', 'description': 'Established tech company with solid growth'},
        ]
    },
    'High': {
        'goal': 'Maximize growth potential and returns.',
        'allocation': '80% Stocks, 20% Bonds',
        'rationale': 'High-risk tolerance, accepting volatility for higher returns.',
        'summary': 'Aggressive approach with a focus on stock investments.',
        'stock_criteria': {
            'volatility_threshold': 0.03,
            'avg_return_threshold': 0.0015,
            'min_price_change_percent': 10
        },
        'recommended_investments': [
            {'ticker': 'QQQ', 'name': 'Invesco QQQ Trust', 'description': 'Growth-focused tech-heavy index'},
            {'ticker': 'VUG', 'name': 'Vanguard U.S. Growth ETF', 'description': 'High-growth stocks with higher volatility'},
            {'ticker': 'TSLA', 'name': 'Tesla', 'description': 'High-growth tech company with significant upside potential'},
            {'ticker': 'NVDA', 'name': 'NVIDIA', 'description': 'AI and semiconductor leader with strong growth'},
            {'ticker': 'AMD', 'name': 'Advanced Micro Devices', 'description': 'Semiconductor company with high growth potential'},
        ]
    }
}

# Score mapping
score_for_option = {
    'Very uncomfortable': 0,
    'uncomfortable': 1,
    'Neutral': 2,
    'comfortable': 3,
    'very comfortable': 4
}

# Calculate total score
total_score = sum(score_for_option.get(r, 0) for r in st.session_state.responses)

# Determine risk profile
if total_score <= 6:
    profile = 'Low'
elif total_score <= 13:
    profile = 'Medium'
else:
    profile = 'High'

# Streamlit UI
st.title('📊 Risk Tolerance Assessment')
tab1, tab2, tab3 = st.tabs(["📋 Assessment", "📈 Results", "🔍 Stock Analyzer"])

# TAB 1
with tab1:
    st.header("Answer the Following Questions")
    for i, question in enumerate(questions):
        display_question(question, i)
    st.info(f"Current Score: **{total_score}/20**")

# TAB 2
with tab2:
    st.header(f"Your Risk Profile: {profile}")
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Risk Score", f"{total_score}/20")
    col2.metric("🎯 Profile", profile)
    col3.metric("💼 Allocation", risk_profiles[profile]['allocation'])

    st.write(f"**Goal:** {risk_profiles[profile]['goal']}")
    st.write(f"**Recommended Asset Allocation:** {risk_profiles[profile]['allocation']}")
    st.write(f"**Rationale:** {risk_profiles[profile]['rationale']}")
    st.write(f"**Summary:** {risk_profiles[profile]['summary']}")

    st.subheader(f"📈 Recommended Investments for {profile} Risk Profile")
    st.table(pd.DataFrame(risk_profiles[profile]['recommended_investments']))

# TAB 3 — STOCK ANALYZER (Stooq Data)
with tab3:
    st.header("🔍 Stock Investment Recommendation")
    stock_ticker = st.text_input("Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL):").upper()

    if stock_ticker:
        try:
            url = f"https://stooq.com/q/d/l/?s={stock_ticker.lower()}.us&i=d"
            stock_data = pd.read_csv(url)

            if stock_data.empty:
                st.warning("No data found. Check the ticker symbol.")
            else:
                stock_data['Date'] = pd.to_datetime(stock_data['Date'])
                stock_data = stock_data.sort_values('Date')
                stock_data.set_index('Date', inplace=True)

                close_prices = stock_data['Close']
                stock_data['Daily Return'] = close_prices.pct_change()

                volatility = stock_data['Daily Return'].std()
                avg_daily_return = stock_data['Daily Return'].mean()
                price_change_percent = ((close_prices.iloc[-1] - close_prices.iloc[0]) / close_prices.iloc[0]) * 100

                col1, col2, col3 = st.columns(3)
                col1.metric("Daily Volatility", f"{volatility:.4f}")
                col2.metric("Avg Daily Return", f"{avg_daily_return:.4f}")
                col3.metric("1-Year Change", f"{price_change_percent:.2f}%")

                criteria = risk_profiles[profile]['stock_criteria']
                checks = []

                st.write("---")

                if volatility <= criteria['volatility_threshold']:
                    st.write(f"✅ Volatility is acceptable.")
                    checks.append(True)
                else:
                    st.write(f"❌ Volatility exceeds your risk tolerance.")
                    checks.append(False)

                if avg_daily_return >= criteria['avg_return_threshold']:
                    st.write(f"✅ Average return meets expectations.")
                    checks.append(True)
                else:
                    st.write(f"❌ Average return is too low.")
                    checks.append(False)

                if price_change_percent >= criteria['min_price_change_percent']:
                    st.write(f"✅ Price growth meets expectations.")
                    checks.append(True)
                else:
                    st.write(f"❌ Price growth is below expectations.")
                    checks.append(False)

                st.write("---")

                if all(checks):
                    st.success(f"**Recommendation: Consider Investing in {stock_ticker}.**")
                else:
                    st.error(f"**Recommendation: {stock_ticker} does not meet your risk criteria.**")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
