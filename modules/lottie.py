import requests
import streamlit as st
from streamlit_lottie import st_lottie
import time

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"Chyba při načítání Lottie URL: {e}")
    except requests.exceptions.RequestException as e:
        st.error(f"Chyba požadavku: {e}")
    return None

def lottie_animation_uvodni(lottie_url, key):
    lottie_json = load_lottieurl(lottie_url)
    if lottie_json and ("lottie_loaded" not in st.session_state or not st.session_state.lottie_loaded):
        st_lottie(lottie_json, key=key, height=200, width=200)
        st.text("Načítám...")
        st.session_state.lottie_loaded = True
        with st.spinner(text='In progress'):
            time.sleep(1)

def lottie_animation(lottie_url, key):
    lottie_json = load_lottieurl(lottie_url)
    st_lottie(lottie_json, key=key, height=200, width=200)
