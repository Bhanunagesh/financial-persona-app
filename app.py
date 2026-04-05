# =========================
# Imports (ALWAYS at top)
# =========================
import streamlit as st
import requests
import matplotlib.pyplot as plt
import os

# =========================
# Page Config (ONLY ONCE)
# =========================
st.set_page_config(
    page_title="Conscious Bridge Labs",
    layout="centered"
)

# =========================
# Branding
# =========================
if os.path.exists("logo.png"):
    st.image("logo.png", width=200)

st.title("Conscious Bridge Labs")
st.caption("Bridging financial behavior, emotion, and intelligence")

# =========================
# Constants
# =========================
API_URL = "https://financial-api-751405119196.asia-south1.run.app"

# =========================
# Helper Functions
# =========================
def get_color(persona):
    if "At Risk" in persona:
        return "red"
    elif "Stable" in persona:
        return "green"
    elif "Drifting" in persona:
        return "orange"
    else:
        return "blue"


def predict_risk(data):
    score = (
        data["stress_score"] * 0.4 +
        (100 - data["financial_health"]) * 0.3 +
        (100 - data["goal_alignment"]) * 0.3
    )

    if score > 70:
        return "High Risk"
    elif score > 40:
        return "Moderate Risk"
    else:
        return "Low Risk"


def generate_advice(data):
    if data["stress_score"] > 70:
        return "You appear financially stressed. Consider reducing discretionary spending and building a safety buffer."
    
    if data["engagement_score"] < 30:
        return "You are not actively engaging with your finances. Regular tracking can significantly improve outcomes."
    
    if data["goal_alignment"] < 40:
        return "Your financial goals lack alignment. Define clear, measurable milestones."

    return "You are on a stable financial path. Consider long-term wealth creation strategies."


@st.cache_data
def fetch_user(user_id):
    url = f"{API_URL}/user/{user_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "API request failed"}

    return response.json()


# =========================
# App Title
# =========================
st.title("💰 Financial Persona Explorer")
st.caption("Understand users beyond transactions")

# =========================
# User Input
# =========================
customer_id = st.text_input("Enter Customer ID", "1")

# =========================
# Analyze Button
# =========================
if st.button("Analyze User"):

    with st.spinner("Analyzing user..."):

        data = fetch_user(customer_id)

        if "error" in data:
            st.error(data["error"])
            if "available_sample" in data:
                st.info(f"Try: {data['available_sample']}")

        else:
            st.success("Analysis Complete ✅")

            # =========================
            # Persona
            # =========================
            color = get_color(data['persona'])

            st.markdown(f"""
            ### 👤 Persona: <span style='color:{color}'>{data['persona']}</span>
            """, unsafe_allow_html=True)

            # Insight
            st.info(f"🧠 {data['insight']}")

            st.markdown("---")

            # =========================
            # Metrics
            # =========================
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("💪 Financial Health", round(data["financial_health"], 2))
            col2.metric("😰 Stress", round(data["stress_score"], 2))
            col3.metric("📱 Engagement", round(data["engagement_score"], 2))
            col4.metric("🎯 Goals", round(data["goal_alignment"], 2))

            # =========================
            # Risk Prediction
            # =========================
            risk = predict_risk(data)

            st.markdown("### ⚠️ Predicted Financial Risk")

            risk_color = (
                "red" if risk == "High Risk"
                else "orange" if risk == "Moderate Risk"
                else "green"
            )

            st.markdown(f"**Risk Level:** :{risk_color}[{risk}]")

            # =========================
            # Chart
            # =========================
            st.markdown("### 📈 Financial Profile")

            labels = ["Health", "Engagement", "Stress", "Goals"]
            values = [
                data["financial_health"],
                data["engagement_score"],
                data["stress_score"],
                data["goal_alignment"]
            ]

            fig, ax = plt.subplots()
            ax.bar(labels, values)
            st.pyplot(fig)

            # =========================
            # AI Advice
            # =========================
            st.markdown("### 🤖 AI Financial Coach")
            st.success(generate_advice(data))

            # =========================
            # Behavioral Scores
            # =========================
            st.markdown("### 📊 Behavioral Scores")

            st.progress(min(max(data["financial_health"] / 100, 0), 1))
            st.caption("Financial Health")

            st.progress(min(max(data["engagement_score"] / 100, 0), 1))
            st.caption("Engagement")

            st.progress(min(max(data["stress_score"] / 100, 0), 1))
            st.caption("Stress")

            # =========================
            # Explanation
            # =========================
            st.markdown("### 🧾 Why this persona?")
            st.write("""
            This classification is based on:
            - Cash flow stability
            - Behavioral engagement
            - Emotional indicators
            - Financial resilience
            - Goal alignment
            """)

# =========================
# Compare Users
# =========================
st.markdown("### 🧑‍🤝‍🧑 Compare Users")

user1 = st.text_input("User 1 ID", "1")
user2 = st.text_input("User 2 ID", "2")

if st.button("Compare"):

    d1 = fetch_user(user1)
    d2 = fetch_user(user2)

    if "error" not in d1 and "error" not in d2:

        st.write("### Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"User {user1}")
            st.write(d1["persona"])

        with col2:
            st.write(f"User {user2}")
            st.write(d2["persona"])
    else:
        st.error("Error fetching user data")

# =========================
# Info Section
# =========================
st.markdown("### 🧭 Conscious Bridge Insight Engine")

st.write("""
This platform analyzes users across multiple dimensions:

- Cash-flow behavior
- Emotional relationship with money
- Financial resilience
- Goal alignment
- Engagement patterns

Unlike traditional systems, this creates a **holistic financial identity**.
""")
