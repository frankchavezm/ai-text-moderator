import streamlit as st
import matplotlib.pyplot as plt
import base64
from gradio_client import Client
from io import BytesIO

# Initialize Gradio clients
client = Client("duchaba/Friendly_Text_Moderation")

# Streamlit UI
st.title("Friendly Text Moderation")

# Section 1: Check text toxicity
st.subheader("Check Text Toxicity")
user_input = st.text_area("Enter text to analyze", "Hello!!")
safer_threshold = st.slider("Select safer threshold", 0.0, 1.0, 0.02, 0.01)

if st.button("Analyze Toxicity"):
    try:
        # Call API and get the result
        result_t = client.predict(msg=user_input, safer=safer_threshold, api_name="/fetch_toxicity_level")
        result = result_t[0]
        # Debug: Show the entire result to understand its structure
        #st.write(type(result))
        st.write("API Result:", result)
        
        # Check if the response contains a toxicity score
        toxicity_score = None
    
        if isinstance(result, dict):
            if "toxicity" in result:
                toxicity_score = result["toxicity"]
            elif "plot" in result and result["type"] == "matplotlib":
                # The API returned a plot, let's display it
                st.write("The API returned a Matplotlib plot instead of a numeric toxicity score.")
                img_data = result["plot"].split(",")[1]  # Extract base64 image data
                img_bytes = base64.b64decode(img_data)
                st.image(img_bytes, caption="Toxicity Analysis Plot", use_column_width=True)
            else:
                st.error("Unexpected API response format.")

        if toxicity_score is not None:
            # Display toxicity score
            st.success(f"Toxicity Score: {toxicity_score}")

            # Plot the toxicity level using Matplotlib
            fig, ax = plt.subplots()
            ax.bar(["Toxicity"], [toxicity_score], color=["red" if toxicity_score > 0.5 else "green"])
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
st.sidebar.info("This is a simple web app using Streamlit to call Friendly Text Moderation APIs and visualize toxicity levels.")
