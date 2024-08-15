import streamlit as st
import anthropic

api_key = st.secrets ["claude_api_key"]

# Function to generate a meal plan using Claude.ai based on sugar levels and dietary preferences
def generate_meal_plan(api_key, fasting, pre_meal, post_meal, dietary_pref):
    # Initialize the Anthropics client with the provided API key
    client = anthropic.Anthropic(api_key=api_key)

    # Prepare the input message with user data
    user_input = (
        f"My fasting sugar level is {fasting} mg/dL, "
        f"my pre-meal sugar level is {pre_meal} mg/dL, "
        f"and my post-meal sugar level is {post_meal} mg/dL. "
        f"My dietary preference is {dietary_pref}. "
        "Please provide a personalized meal plan considering these details."
    )

    # Create the message to send to Claude.ai
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=250,
        temperature=0.7,
        system="You are a world-class nutritionist. Generate a personalized meal plan based on the user's sugar levels and dietary preferences.",
        messages=[
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": user_input
                }
            }
        ]
    )

    # Extract and return the relevant text from the response
    return message.get('content', 'No response received')

# Streamlit app setup
st.title("GlucoGuide")

# App description
st.write("""
### Your Personalized Diabetes Management Companion

GlucoGuide is designed to help diabetic patients manage their blood sugar levels through personalized meal plans. 
By entering your fasting, pre-meal, and post-meal sugar levels, along with your dietary preferences, 
you can receive a tailored meal plan to support your journey to better health.
""")

# Sidebar inputs
st.sidebar.header("Enter Your Details")

fasting_sugar = st.sidebar.number_input("Fasting Sugar Level (mg/dL)", min_value=0, max_value=300, value=100)
pre_meal_sugar = st.sidebar.number_input("Pre-meal Sugar Level (mg/dL)", min_value=0, max_value=300, value=100)
post_meal_sugar = st.sidebar.number_input("Post-meal Sugar Level (mg/dL)", min_value=0, max_value=400, value=140)
dietary_preference = st.sidebar.selectbox("Dietary Preference", ("None", "Vegetarian", "Vegan", "Keto"))

# Generate meal plan when the user submits the information
if st.sidebar.button("Get Meal Plan"):
    if api_key:
        meal_plan = generate_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preference)
        st.subheader("Your Personalized Meal Plan")
        st.markDown(meal_plan)
    