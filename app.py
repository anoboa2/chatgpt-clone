import streamlit as st
import openai

# Configure API Credentials
openai.api_key = st.secrets["OPENAI_API_SECRET"]

# Configure which OpenAI model to use
if "openai_model" not in st.session_state:
  st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize session state
if "messages" not in st.session_state:
  st.session_state.messages = []


### Streamlit UI ###

# Populate any previous messages
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    
  # Add user message to chat history
  st.session_state.messages.append({"role": "user", "content": prompt})

  # Display user message in chat message container
  with st.chat_message("user"):
    st.markdown(prompt)
  
  # Display assistant response in chat message container
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""

    # Stream assistant responses from GPT API call
    for response in openai.ChatCompletion.create(
      model=st.session_state["openai_model"],
      messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
      stream=True,
    ):
      full_response += response.choices[0].delta.get("content", "") # type: ignore
      message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
  st.session_state.messages.append({"role": "assistant", "content": full_response})
