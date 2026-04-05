import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
#import google.generativeai as genai
import OpenAI as 

# ---------------- CONFIG ----------------
API_URL = "https://financial-api-751405119196.asia-south1.run.app"

st.set_page_config(page_title="Conscious Bridge Labs", layout="centered")

# Gemini setup
#genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
#model = genai.GenerativeModel("gemini-pro")
#model = genai.GenerativeModel("gemini-1.0-pro")
# OpenAI Setup
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- BRANDING ----------------
st.markdown("""
# 🌉 Conscious Bridge Labs
### Behavioral Finance Intelligence Platform
Bridging financial behavior, emotion, and intelligence
""")

# ---------------- FUNCTIONS ----------------
def get_color(persona):
    if "At Risk" in persona:
        return "red"
    elif "Stable" in persona:
        return "green"
    elif "Drifting" in persona:
        return "orange"
    else:
        return "blue"


#def generate_ai_advice(data):
    #prompt = f"""
    #You are a financial behavior expert.

    #User Profile:
    #- Persona: {data['persona']}
    #- Financial Health: {data['financial_health']}
    #- Stress Score: {data['stress_score']}
    #- Engagement: {data['engagement_score']}
    #- Goal Alignment: {data['goal_alignment']}

    #Give personalized financial advice in 3-4 bullet points.
    #Keep it practical and human.
    #"""
def generate_ai_insight(data):
    prompt = f"""
    User financial profile:
    - Health: {data.get('financial_health')}
    - Stress: {data.get('stress_score')}
    - Engagement: {data.get('engagement_score')}
    - Goals: {data.get('goal_alignment')}

    Give a short personalized financial advice.
    """
    #response = model.generate_content("Explain financial stress simply")
    #return response.text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content



def plot_radar(data):
    labels = ["Health", "Engagement", "Stress", "Goals"]
    values = [
        data["financial_health"],
        data["engagement_score"],
        data["stress_score"],
        data["goal_alignment"]
    ]

    values += values[:1]

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    return fig


# ---------------- SIDEBAR DEMO ----------------
st.sidebar.title("Demo Mode")
demo_user = st.sidebar.selectbox("Try Sample Users", ["1", "10", "50"])

# ---------------- MAIN INPUT ----------------
customer_id = st.text_input("Enter Customer ID", demo_user)

if st.button("Analyze User"):

    with st.spinner("Fetching user data..."):

        try:
            response = requests.get(f"{API_URL}/user/{customer_id}")
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
                ### 🧬 Financial Identity: <span style='color:{color}'>{data['persona']}</span>
                """, unsafe_allow_html=True)

                # Insight
                st.markdown("### 🧠 Behavioral Insight")
                st.info(data["insight"])

                st.markdown("---")

                # Metrics
                st.markdown("### 📊 Financial Signals")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Health", round(data["financial_health"], 2))
                col2.metric("Stress", round(data["stress_score"], 2))
                col3.metric("Engagement", round(data["engagement_score"], 2))
                col4.metric("Goals", round(data["goal_alignment"], 2))

                # Radar Chart
                st.markdown("### 📈 Behavioral Radar")
                fig = plot_radar(data)
                st.pyplot(fig)

                # AI Advice
                st.markdown("### 🤖 AI Financial Coach")
                st.success(generate_ai_insight(data))

                #with st.spinner("Generating AI advice..."):
                 #   advice = generate_ai_advice(data)
                  #  st.success(advice)
                with st.spinner("Analyzing behavioral patterns..."):
                insight = generate_ai_insight(data)
                st.success(insight)

                # Explanation
                st.markdown("### 🧭 Conscious Bridge Insight Engine")
                st.write("""
                This platform analyzes users across multiple dimensions:
                - Cash-flow behavior
                - Emotional relationship with money
                - Financial resilience
                - Goal alignment
                - Engagement patterns
                """)

        except Exception as e:
            st.error(f"API Error: {e}")


# ---------------- COMPARE USERS ----------------
st.markdown("---")
st.markdown("### 🧑‍🤝‍🧑 Compare Users")

user1 = st.text_input("User 1 ID", "1")
user2 = st.text_input("User 2 ID", "2")

if st.button("Compare Users"):

    with st.spinner("Fetching comparison data..."):

        try:
            d1 = requests.get(f"{API_URL}/user/{user1}").json()
            d2 = requests.get(f"{API_URL}/user/{user2}").json()

            if "error" in d1:
                st.error(f"User {user1}: {d1['error']}")
                st.stop()

            if "error" in d2:
                st.error(f"User {user2}: {d2['error']}")
                st.stop()

            st.success("Comparison Loaded ✅")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### 👤 User {user1}")
                st.write(f"**Persona:** {d1['persona']}")
                st.metric("Health", round(d1["financial_health"], 2))
                st.metric("Stress", round(d1["stress_score"], 2))
                st.metric("Engagement", round(d1["engagement_score"], 2))
                st.metric("Goals", round(d1["goal_alignment"], 2))

            with col2:
                st.markdown(f"### 👤 User {user2}")
                st.write(f"**Persona:** {d2['persona']}")
                st.metric("Health", round(d2["financial_health"], 2))
                st.metric("Stress", round(d2["stress_score"], 2))
                st.metric("Engagement", round(d2["engagement_score"], 2))
                st.metric("Goals", round(d2["goal_alignment"], 2))

        except Exception as e:
            st.error(f"Comparison failed: {e}")
