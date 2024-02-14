import streamlit as st
import openai

# Předpokládáme, že jste svůj OpenAI API klíč uložili do Streamlit Secrets
openai.api_key = st.secrets["openai_api_key"]


def generate_response_with_openai(context, prompt, temperature, max_tokens):
    """Generuje odpověď pomocí OpenAI API na základě zadaných parametrů."""
    full_prompt = f"{context}\n{prompt}"
    response = openai.Completion.create(
        engine="text-davinci-003",  # Můžete zvolit jiný model podle vašeho výběru
        prompt=full_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=[" Asistent 1:", " Asistent 2:"]
    )
    return response.choices[0].text.strip()


def update_conversation():
    """Aktualizuje konverzaci střídavě mezi oběma asistenty."""
    if st.session_state.conversation:  # Pokud už konverzace začala
        context = "\n".join(st.session_state.conversation)
        next_assistant_id = 1 if len(st.session_state.conversation) % 2 == 0 else 2

        if next_assistant_id == 1:
            prompt = assistant_1_prompt
            temperature = assistant_1_temperature
            max_tokens = assistant_1_max_tokens
        else:
            prompt = assistant_2_prompt
            temperature = assistant_2_temperature
            max_tokens = assistant_2_max_tokens

        new_message = generate_response_with_openai(context, prompt, temperature, max_tokens)
        st.session_state.conversation.append(new_message)


# Umožní uživatelům nastavit parametry pro každého asistenta
st.sidebar.header("Nastavení Asistentů")
assistant_1_prompt = st.sidebar.text_input("Prompt Asistenta 1", value="Asistent 1:")
assistant_2_prompt = st.sidebar.text_input("Prompt Asistenta 2", value="Asistent 2:")
assistant_1_temperature = st.sidebar.slider("Teplota Asistenta 1", min_value=0.0, max_value=1.0, value=0.7)
assistant_2_temperature = st.sidebar.slider("Teplota Asistenta 2", min_value=0.0, max_value=1.0, value=0.7)
assistant_1_max_tokens = st.sidebar.number_input("Max tokenů Asistenta 1", min_value=1, value=150)
assistant_2_max_tokens = st.sidebar.number_input("Max tokenů Asistenta 2", min_value=1, value=150)

# Inicializace nebo reset konverzace
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

st.title('Konverzace mezi dvěma asistenty s OpenAI')

if st.button('Zahájit / Resetovat konverzaci'):
    st.session_state.conversation = []
    # Po zahájení konverzace automaticky generujte první zprávu od Asistenta 1
    update_conversation()

if st.button('Pokračovat v konverzaci'):
    update_conversation()

# Zobrazení celé historie konverzace
st.write("Historie konverzace:")
for message in st.session_state.conversation:
    st.text(message)