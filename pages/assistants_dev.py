import openai
import streamlit as st
import time
import os
from modules.lottie import lottie_animation_uvodni, lottie_animation, load_lottieurl
st.set_page_config(page_title="Home page", page_icon=":speech_balloon:")

# Inicializace API key a ID. Uloženo na cloudu Streamlit v secret
openai.api_key = st.secrets["API_KEY"]
default_assistant_id = st.secrets["ASSISTANT_ID"]
client = openai

def create_new_assistant(name, instructions, model):
    """Funkce pro vytvoření nového asistenta."""
    try:
        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=[],  # Prázdné pole 'tools'
            model=model
        )
        return assistant
    except Exception as e:
        st.sidebar.error(f"Chyba při vytváření asistenta: {e}")
        return None

def initialize_session():
    """Inicializuje session state pro Streamlit aplikaci."""
    if "start_chat" not in st.session_state:
        st.session_state.start_chat = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.session_state.messages = []

def send_message_to_openai(prompt):
    """Odesílá uživatelskou zprávu do OpenAI a zpracovává odpověď."""
    current_assistant_id = st.session_state.get('assistant_id', default_assistant_id)
    start_time = time.time()

    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=current_assistant_id,
        inputs=[{"type": "chat", "message": {"role": "user", "content": prompt}}],
    )

    # Čekání na dokončení dotazu
    while run.status != 'completed':
        time.sleep(0.5)  # Čekání na aktualizaci stavu
        run = client.beta.threads.runs.retrieve(run_id=run.id)

    end_time = time.time()
    response_time = end_time - start_time

    st.write(f"Doba odezvy: {response_time:.2f} sekund")
    if run.outputs:
        for output in run.outputs:
            if output["type"] == "chat" and output["message"]["role"] == "assistant":
                st.session_state.messages.append({"role": "assistant", "content": output["message"]["content"]})
                with st.container():
                    st.markdown(f"**Assistant:** {output['message']['content']}")

def chat():
    """Zpracovává uživatelský vstup a zobrazuje zprávy."""
    prompt = st.text_input("Zadejte svou zprávu:")
    if prompt:
        send_message_to_openai(prompt)
        st.text_input("Zadejte svou zprávu:", value="", key="new")  # Reset input field

# Vytvoření sidebar formuláře pro nového asistenta
with st.sidebar.form("create_assistant_form"):
    st.write("Vytvořte nového asistenta")
    assistant_name = st.text_input("Název asistenta")
    assistant_instructions = st.text_area("Instrukce", height=100)
    assistant_model = st.selectbox(
        "Model",
        ['gpt-4-1106-preview', 'gpt-4-0125-preview', 'gpt-4-preview', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-0125'],
        index=0
    )
    submit_button = st.form_submit_button("Vytvořit asistenta")

    if submit_button and assistant_name and assistant_instructions:
        new_assistant = create_new_assistant(assistant_name, assistant_instructions, assistant_model)
        if new_assistant:
            st.sidebar.success(f"Asistent '{assistant_name}' byl úspěšně vytvořen!")
            st.session_state.assistant_id = new_assistant.id
        else:
            st.sidebar.error("Asistenta se nepodařilo vytvořit.")

# Nastavení Streamlit
st.title("😊💡Home page!🔍")

initialize_session()
chat()
