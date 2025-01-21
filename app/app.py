import streamlit as st
from gradio_client import Client
import matplotlib.pyplot as plt

# Initialize Gradio clients
client = Client("duchaba/Friendly_Text_Moderation")

# Streamlit UI
st.title("Friendly Text Moderation")

# Section 1: Check toxicity level
st.subheader("Check Text Toxicity")
user_input = st.text_area("Enter text to analyze", "Hello!!")
safer_threshold = st.slider("Select safer threshold", 0.0, 1.0, 0.02, 0.01)

if st.button("Analyze Toxicity"):
    try:
        # Call API
        result = client.predict(msg=user_input, safer=safer_threshold, api_name="/fetch_toxicity_level")
        
        # Display result
        st.success(f"Toxicity Score: {result}")
        
        # Plot the toxicity level using Matplotlib
        fig, ax = plt.subplots()
        ax.bar(["Toxicity"], [result], color=["red" if result > 0.5 else "green"])
        ax.set_ylim(0, 1)
        ax.set_ylabel("Toxicity Level")
        ax.set_title("Toxicity Score Visualization")
        
        # Show the plot in Streamlit
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")

# Section 2: Fetch toxic tweets
st.subheader("Fetch Toxic Tweets")
if st.button("Get Toxic Tweets"):
    try:
        toxic_tweets = client.predict(api_name="/fetch_toxic_tweets")
        st.write("### Toxic Tweets:")
        for idx, tweet in enumerate(toxic_tweets, 1):
            st.write(f"{idx}. {tweet}")
    except Exception as e:
        st.error(f"Error: {e}")

st.sidebar.markdown("### About")
st.sidebar.info("This is a simple web app using Streamlit to call Friendly Text Moderation APIs.")

