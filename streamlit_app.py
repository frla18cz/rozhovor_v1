import openai
import streamlit as st
import time
import os
from modules.lottie import lottie_animation_uvodni, lottie_animation, load_lottieurl


# Inicializace api key. Uloženo na cloudu streamlit v secret
openai.api_key = st.secrets["API_KEY"]
# assistant_id = st.secrets["ASSISTANT_ID"]
# assistant_id = "asst_atZWsxED84ngEs7lXxCAKR9Q" #Pro testovací účely, light prompt
client = openai

# Funkce pro načtení seznamu asistentů
def nacist_seznam_asistentu():
    try:
        response = client.beta.assistants.list()
        asistenti_tuple = [(assistant.id, assistant.name) for assistant in response.data]
        return asistenti_tuple
    except Exception as e:
        st.error(f"Chyba při načítání asistentů: {e}")
        return []


# Nastavení Streamlit
st.set_page_config(page_title="Home page", page_icon=":speech_balloon:")
st.title("😊💡Home page!🔍")

current_directory = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(current_directory, 'img1.png')
st.image(img_path, caption='', use_column_width=True)

lottie_animation_uvodni("https://lottie.host/ae43b28d-b082-4249-bc22-144e1ceed7f7/ebUqhkyptl.json", 1)
# Definice funkce pro stránku "Databáze"

# Vytvoření rozklikávacího seznamu pro výběr asistenta
asistenti_tuple = nacist_seznam_asistentu()
if asistenti_tuple:
    vybrany_asistent = st.sidebar.selectbox('Vyberte asistenta:', asistenti_tuple, format_func=lambda x: x[1])
    assistant_id = vybrany_asistent[0]  # Aktualizujte globální proměnnou assistant_id na základě výběru
else:
    st.sidebar.error("Nepodařilo se načíst seznam asistentů.")

model_choice = st.sidebar.selectbox(
    'Vyberte model:',
    ('gpt-4-0125-preview', 'gpt-4-preview', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-0125'),
    index=3
)


def initialize_session():
    """Inicializuje session state pro Streamlit aplikaci"""
    if "start_chat" not in st.session_state:
        st.session_state.start_chat = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.session_state.messages = []

    #Automaticky spouští chat.
    # if "initial_message_sent" not in st.session_state:
    #     # Kontrola, zda už nebyla úvodní zpráva přidána
    #     if not any(message["content"] == "Zahajme hru!" for message in st.session_state.messages):
    #         send_initial_message()
    #         st.session_state.initial_message_sent = True


def send_initial_message():
    """Odesílá počáteční zprávu do chatu."""
    initial_message = "Zahajme hru!"
    st.session_state.messages = [{"role": "assistant", "content": initial_message}]
    send_message_to_openai(initial_message)


def chat():
    # if st.button("Exit Chat"):
    #     st.session_state.messages = []  # Clear the chat history
    #     st.session_state.thread_id = None
    #     js = "window.location.reload()"
    #     st.markdown(js, unsafe_allow_html=True)

    process_user_input()
    lottie_animation("https://lottie.host/2b556f4b-1b93-477e-a421-9e31f4511246/tKYol4Wo3r.json", 3)


def display_messages():
    """Zobrazuje zprávy v chatovacím rozhraní."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def process_user_input():
    """Zpracovává uživatelský vstup a odesílá jej do OpenAI."""
    prompt = st.chat_input("...")
    if prompt:
        st.write("Já😊: ", prompt)

        send_message_to_openai(prompt)


def send_message_to_openai(prompt):
    """
    Odesílá uživatelskou zprávu do OpenAI a zpracovává odpověď.

    Args:
        prompt (str): Text zprávy odeslané uživatelem.
    """
    start_time = time.time()  # Začátek měření času

    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt
    )

    # Vytvoření a spuštění dotazu pro OpenAI
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id,
    )

    # Čekání na dokončení dotazu
    while run.status != 'completed':
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )

    end_time = time.time()  # Konec měření času
    response_time = end_time - start_time  # Výpočet doby odezvy
    st.write(f"Doba odezvy: {response_time:.2f} sekund")  # Zobrazení doby odezvy

    # Čekání na dokončení dotazu
    while run.status != 'completed':
        time.sleep(0.05)
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )

    # Získání všech zpráv z vlákna
    messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id
    )

    # Zpracování a zobrazení odpovědí asistenta
    assistant_messages_for_run = [
        message for message in messages
        if message.run_id == run.id and message.role == "assistant"
    ]
    for message in assistant_messages_for_run:
        st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
        with st.chat_message("assistant"):
            st.markdown(message.content[0].text.value)


initialize_session() # Inicializace session state pro Streamlit aplikaci
chat()