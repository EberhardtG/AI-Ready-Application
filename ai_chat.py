"""
WHY / DESIGN — ai_chat.py

Purpose:
This module provides the AI assistant functionality for the Streamlit frontend.
It handles both real OpenAI streaming responses and a mock fallback mode used
during development or when API access is unavailable. The goal is to keep AI
logic isolated from the main UI while ensuring a smooth, crash‑free chat
experience.

Design Choices:
- Dual Streaming Modes:
  The app supports real OpenAI streaming for production use and a mock streaming
  generator for offline development. Both produce token‑by‑token output so the
  UI behaves consistently regardless of backend availability.

- Safe API Initialization:
  The OpenAI client is created inside a try/except block. If no API key is found,
  the module automatically switches to mock mode without breaking the UI.

- Context + System Prompt Injection:
  The assistant receives a system prompt and optional technical/task contexts.
  These are injected as system messages, allowing the user to shape the AI’s
  behavior dynamically without modifying backend code.

- Robust Error Handling:
  All OpenAI calls are wrapped in try/except blocks. Any failure—rate limits,
  invalid keys, network errors, or streaming interruptions—triggers an automatic
  fallback to mock mode. This prevents crashes and keeps the chat responsive.

- Streamlit Session State:
  Chat history is stored in st.session_state so messages persist across reruns.
  This enables a stable conversational interface within Streamlit’s reactive
  execution model.

Outcome:
The result is a modular, resilient AI chat component that supports real‑time
streaming, customizable prompts, safe fallbacks, and a clean integration with
the Streamlit UI. It enhances the Task Manager app without introducing instability
or backend dependencies.
"""




import streamlit as st
import time
from openai import OpenAI

# Load API key from Streamlit secrets
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    client = None
    st.warning("No OpenAI API key found. Mock mode only.")


# ----------------------------------------------------
# MOCK STREAMING RESPONSE
# ----------------------------------------------------
def mock_stream(prompt, contexts):
    context_str = ", ".join(contexts) if contexts else "general knowledge"
    text = (
        f"Using my {context_str} background, here's my take on '{prompt}': "
        f"This would be a real AI response in production."
    )

    for word in text.split():
        yield word + " "
        time.sleep(0.03)


# ----------------------------------------------------
# REAL OPENAI STREAMING RESPONSE
# ----------------------------------------------------
def openai_stream(system_prompt, contexts, user_message, model="gpt-4o-mini"):
    context_str = ", ".join(contexts) if contexts else "general knowledge"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Additional context: {context_str}"},
        {"role": "user", "content": user_message}
    ]

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )

        partial = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.get("content", "")
            partial += delta
            yield partial

    except Exception as e:
        # Fallback to mock mode on ANY OpenAI failure
        yield f"⚠️ OpenAI unavailable — switching to mock mode.\nReason: {str(e)}\n"
        yield from mock_stream(user_message, contexts)

# ----------------------------------------------------
# AI CHAT UI (CALLED FROM app.py)
# ----------------------------------------------------
def ai_chat_ui(system_prompt, contexts, model, use_real_api):
    st.subheader("AI Assistant")

    # Initialize chat history
    if "ai_messages" not in st.session_state:
        st.session_state["ai_messages"] = []

    # Render previous messages
    for msg in st.session_state["ai_messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Handle new input
    if prompt := st.chat_input("Ask the AI anything..."):
        st.session_state["ai_messages"].append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            if use_real_api:
                try:
                    response = st.write_stream(
                        openai_stream(system_prompt, contexts, prompt, model)
                    )
                except Exception as e:
                    st.warning(f"⚠️ OpenAI failed — switching to mock mode.\nReason: {str(e)}")
                    response = st.write_stream(
                        mock_stream(prompt, contexts)
                    )
            else:
                response = st.write_stream(
                    mock_stream(prompt, contexts)
                )


        st.session_state["ai_messages"].append({"role": "assistant", "content": response})
        st.rerun()
