import streamlit as st
import requests

API_URL = "https://financial-api-751405119196.asia-south1.run.app"

st.set_page_config(page_title="Financial Persona App", layout="centered")

st.title("💰 Financial Persona Explorer")
st.caption("Understand users beyond transactions")


# Color function
def get_color(persona):
    if "At Risk" in persona:
        return "red"
    elif "Stable" in persona:
        return "green"
    elif "Drifting" in persona:
        return "orange"
    else:
        return "blue"


# Input
customer_id = st.text_input("Enter Customer ID", "1")

if st.button("Analyze User"):

    url = f"{API_URL}/user/{customer_id}"

    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            st.error(data["error"])
            if "available_sample" in data:
                st.info(f"Try: {data['available_sample']}")

        else:
            st.success("Analysis Complete ✅")

            # Persona
            color = get_color(data['persona'])

            st.markdown(f"""
            ### 👤 Persona: <span style='color:{color}'>{data['persona']}</span>
            """, unsafe_allow_html=True)

            # Insight
            st.info(f"🧠 {data['insight']}")

            st.markdown("---")

            # Metrics
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("💪 Financial Health", round(data["financial_health"], 2))
            col2.metric("😰 Stress", round(data["stress_score"], 2))
            col3.metric("📱 Engagement", round(data["engagement_score"], 2))
            col4.metric("🎯 Goals", round(data["goal_alignment"], 2))

            # Behavioral Scores
            st.markdown("### 📊 Behavioral Scores")

            st.progress(min(max(data["financial_health"] / 100, 0), 1))
            st.caption("Financial Health")

            st.progress(min(max(data["engagement_score"] / 100, 0), 1))
            st.caption("Engagement")

            st.progress(min(max(data["stress_score"] / 100, 0), 1))
            st.caption("Stress")

            # Explanation
            st.markdown("### 🧾 Why this persona?")
            st.write("""
            This classification is based on:
            - Cash flow stability
            - Behavioral engagement
            - Emotional indicators
            - Financial resilience
            - Goal alignment
            """)

    except Exception as e:
        st.error(f"API Error: {e}")
