import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "https://diet-rag.onrender.com"

# Function to get recipe recommendations
def get_recipe_recommendation(query):
    try:
        response = requests.get(f"{BACKEND_URL}/get_ai_recipe/?query={query}")
        if response.status_code == 200:
            return response.json()["AI_Response"]
        else:
            return f"Failed to get recipe: {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit App
def main():
    st.title("🍽️ Diet Recipe Chatbot")

    # Chat Interface
    st.header("Chat with the Bot")
    st.write("Ask me for recipe recommendations based on your preferences!")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What recipe are you looking for?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        bot_response = get_recipe_recommendation(prompt)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)

# Run the app
if __name__ == "__main__":
    main()
